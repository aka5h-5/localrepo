from tree_sitter import Parser
from tree_sitter_languages import get_language
from state import AgentState


def node_text(content: str, node):
    return content[node.start_byte:node.end_byte]


def ast_analyzer(state: AgentState) -> AgentState:

    ast_summary = {
        "classes": [],
        "functions": [],
        "methods": [],
        "imports": [],
        "routes": [],
        "function_calls": [],
        "decorators": [],
        "tests": []
    }

    files = state.repository_contents or {}

    # Language selection
    if state.language == "Python":
        language_name = "python"
        valid_ext = (".py",)

    elif state.language == "JavaScript":
        language_name = "javascript"
        valid_ext = (".js", ".jsx")

    elif state.language == "TypeScript":
        language_name = "typescript"
        valid_ext = (".ts", ".tsx")

    else:
        state.ast_summary = ast_summary
        return state

    parser = Parser()
    parser.set_language(get_language(language_name))

    for path, content in files.items():

        if not path.endswith(valid_ext):
            continue

        if not content.strip():
            continue

        try:
            tree = parser.parse(bytes(content, "utf8"))
        except Exception:
            continue

        # File-based test detection
        if any(
            x in path.lower()
            for x in ["test", "spec", "__tests__"]
        ):
            ast_summary["tests"].append(path)

        stack = [tree.root_node]

        while stack:

            node = stack.pop()

            # ==========================
            # PYTHON
            # ==========================
            if state.language == "Python":

                if node.type == "class_definition":

                    name = node.child_by_field_name("name")

                    if name:
                        ast_summary["classes"].append(
                            node_text(content, name)
                        )

                elif node.type == "function_definition":

                    name = node.child_by_field_name("name")

                    if name:

                        fn_name = node_text(content, name)

                        is_method = False

                        parent = node.parent

                        if (
                            parent
                            and parent.type == "block"
                            and parent.parent
                            and parent.parent.type == "class_definition"
                        ):
                            is_method = True

                        if is_method:
                            ast_summary["methods"].append(fn_name)
                        else:
                            ast_summary["functions"].append(fn_name)

                        if fn_name.startswith("test_"):
                            ast_summary["tests"].append(fn_name)

                elif node.type in (
                    "import_statement",
                    "import_from_statement"
                ):

                    ast_summary["imports"].append(
                        node_text(content, node)
                    )

                elif node.type == "decorated_definition":

                    snippet = node_text(content, node)

                    ast_summary["decorators"].append(
                        snippet.split("\n")[0]
                    )

                    for method in [
                        "get",
                        "post",
                        "put",
                        "delete",
                        "patch"
                    ]:

                        if f".{method}(" in snippet:

                            ast_summary["routes"].append(
                                f"{method.upper()} route"
                            )

                    if "@app.route" in snippet:
                        ast_summary["routes"].append(
                            "Flask Route"
                        )

                elif node.type == "call":

                    fn = node.child_by_field_name("function")

                    if fn:
                        ast_summary["function_calls"].append(
                            node_text(content, fn)
                        )

            # ==========================
            # JAVASCRIPT / TYPESCRIPT
            # ==========================
            else:

                if node.type == "class_declaration":

                    name = node.child_by_field_name("name")

                    if name:
                        ast_summary["classes"].append(
                            node_text(content, name)
                        )

                elif node.type == "function_declaration":

                    name = node.child_by_field_name("name")

                    if name:
                        ast_summary["functions"].append(
                            node_text(content, name)
                        )

                elif node.type == "method_definition":

                    name = node.child_by_field_name("name")

                    if name:
                        ast_summary["methods"].append(
                            node_text(content, name)
                        )

                elif node.type == "import_statement":

                    ast_summary["imports"].append(
                        node_text(content, node)
                    )

                elif node.type == "lexical_declaration":

                    snippet = node_text(content, node)

                    if "=>" in snippet:
                        ast_summary["functions"].append(
                            snippet[:100]
                        )

                elif node.type == "call_expression":

                    fn = node.child_by_field_name("function")

                    if fn:
                        ast_summary["function_calls"].append(
                            node_text(content, fn)
                        )

                    snippet = node_text(content, node)

                    route_patterns = [
                        ".get(",
                        ".post(",
                        ".put(",
                        ".delete(",
                        ".patch("
                    ]

                    if any(
                        pattern in snippet
                        for pattern in route_patterns
                    ):
                        ast_summary["routes"].append(
                            snippet[:100]
                        )

                    if (
                        snippet.startswith("describe(")
                        or snippet.startswith("it(")
                        or snippet.startswith("test(")
                    ):
                        ast_summary["tests"].append(
                            snippet[:100]
                        )

            stack.extend(node.children)

    # Remove duplicates
    for key in ast_summary:
        ast_summary[key] = list(
            dict.fromkeys(ast_summary[key])
        )

    state.ast_summary = ast_summary
    return state
