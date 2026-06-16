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
        "tests": [],
        "function_calls": [],
        "decorators": [],
        "interfaces": [],
        "types": [],
        "exports": []
    }

    files = state.repository_contents or {}

    # -------------------------
    # Select language
    # -------------------------
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

    # -------------------------
    # Traverse repository
    # -------------------------
    for path, content in files.items():

        if not path.endswith(valid_ext):
            continue

        if not content.strip():
            continue

        try:
            tree = parser.parse(bytes(content, "utf8"))
        except Exception:
            continue

        stack = [tree.root_node]

        while stack:

            node = stack.pop()

            # =========================================
            # PYTHON
            # =========================================
            if state.language == "Python":

                # Classes
                if node.type == "class_definition":

                    name = node.child_by_field_name("name")

                    if name:
                        ast_summary["classes"].append(
                            node_text(content, name)
                        )

                # Functions / Methods
                elif node.type == "function_definition":

                    name = node.child_by_field_name("name")

                    if name:

                        fn_name = node_text(content, name)

                        parent = node.parent

                        is_method = False

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

                        # pytest tests
                        if fn_name.startswith("test_"):
                            ast_summary["tests"].append(fn_name)

                # Imports
                elif node.type in (
                    "import_statement",
                    "import_from_statement"
                ):

                    ast_summary["imports"].append(
                        node_text(content, node)
                    )

                # Decorators
                elif node.type == "decorated_definition":

                    snippet = node_text(content, node)

                    ast_summary["decorators"].append(
                        snippet[:300]
                    )

                    # FastAPI
                    for method in [
                        "get",
                        "post",
                        "put",
                        "delete",
                        "patch"
                    ]:

                        if f".{method}(" in snippet:

                            ast_summary["routes"].append({
                                "framework": "fastapi",
                                "method": method.upper(),
                                "file": path
                            })

                    # Flask
                    if "@app.route" in snippet:

                        ast_summary["routes"].append({
                            "framework": "flask",
                            "method": "UNKNOWN",
                            "file": path
                        })

                # Function calls
                elif node.type == "call":

                    fn = node.child_by_field_name("function")

                    if fn:

                        ast_summary["function_calls"].append(
                            node_text(content, fn)
                        )

            # =========================================
            # JAVASCRIPT / TYPESCRIPT
            # =========================================
            else:

                # Classes
                if node.type == "class_declaration":

                    name = node.child_by_field_name("name")

                    if name:

                        ast_summary["classes"].append(
                            node_text(content, name)
                        )

                # Functions
                elif node.type == "function_declaration":

                    name = node.child_by_field_name("name")

                    if name:

                        ast_summary["functions"].append(
                            node_text(content, name)
                        )

                # Methods
                elif node.type == "method_definition":

                    name = node.child_by_field_name("name")

                    if name:

                        ast_summary["methods"].append(
                            node_text(content, name)
                        )

                # Imports
                elif node.type == "import_statement":

                    ast_summary["imports"].append(
                        node_text(content, node)
                    )

                # Exports
                elif node.type == "export_statement":

                    ast_summary["exports"].append(
                        node_text(content, node)
                    )

                # TypeScript Interfaces
                elif node.type == "interface_declaration":

                    name = node.child_by_field_name("name")

                    if name:

                        ast_summary["interfaces"].append(
                            node_text(content, name)
                        )

                # Type Aliases
                elif node.type == "type_alias_declaration":

                    name = node.child_by_field_name("name")

                    if name:

                        ast_summary["types"].append(
                            node_text(content, name)
                        )

                # Arrow Functions
                elif node.type == "lexical_declaration":

                    snippet = node_text(content, node)

                    if "=>" in snippet:

                        ast_summary["functions"].append(
                            snippet[:150]
                        )

                # Function calls
                elif node.type == "call_expression":

                    fn = node.child_by_field_name("function")

                    if fn:

                        ast_summary["function_calls"].append(
                            node_text(content, fn)
                        )

                    snippet = node_text(content, node)

                    # Express routes
                    for method in [
                        ".get(",
                        ".post(",
                        ".put(",
                        ".delete(",
                        ".patch("
                    ]:

                        if method in snippet:

                            ast_summary["routes"].append({
                                "framework": "express",
                                "definition": snippet[:200],
                                "file": path
                            })

                    # Jest / Vitest tests
                    if (
                        snippet.startswith("describe(")
                        or snippet.startswith("it(")
                        or snippet.startswith("test(")
                    ):
                        ast_summary["tests"].append(
                            snippet[:200]
                        )

            stack.extend(node.children)

        # File-based test detection
        lower_path = path.lower()

        if any(
            x in lower_path
            for x in [
                "test",
                "spec",
                "__tests__"
            ]
        ):
            ast_summary["tests"].append(path)

    # Remove duplicates
    for key in ast_summary:
        if isinstance(ast_summary[key], list):

            unique = []
            seen = set()

            for item in ast_summary[key]:

                item_key = str(item)

                if item_key not in seen:
                    unique.append(item)
                    seen.add(item_key)

            ast_summary[key] = unique

    state.ast_summary = ast_summary

    return state
