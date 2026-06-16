from tree_sitter import Parser
from tree_sitter_languages import get_language
from state import AgentState


def ast_analyzer(state: AgentState) -> AgentState:
    ast_summary = {
        "classes": [],
        "functions": [],
        "methods": [],
        "imports": [],
        "routes": [],
        "tests": []
    }

    files = state.repository_contents or {}

    # -------------------------
    # Select grammar by language
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

    # ✅ Correct API for tree-sitter 0.20.4
    parser = Parser()
    parser.set_language(get_language(language_name))

    # -------------------------
    # Traverse repository files
    # -------------------------
    for path, content in files.items():
        if not path.endswith(valid_ext):
            continue
        if not content.strip():
            continue

        # Test detection
        if any(x in path.lower() for x in ("test", "spec", "__tests__")):
            ast_summary["tests"].append(path)

        try:
            tree = parser.parse(bytes(content, "utf8"))
        except Exception:
            continue

        stack = [tree.root_node]

        while stack:
            node = stack.pop()

            # -------- PYTHON --------
            if state.language == "Python":
                if node.type == "class_definition":
                    name = node.child_by_field_name("name")
                    if name:
                        ast_summary["classes"].append(
                            content[name.start_byte:name.end_byte]
                        )

                elif node.type == "function_definition":
                    name = node.child_by_field_name("name")
                    if name:
                        ast_summary["functions"].append(
                            content[name.start_byte:name.end_byte]
                        )

                elif node.type in ("import_statement", "import_from_statement"):
                    ast_summary["imports"].append(
                        content[node.start_byte:node.end_byte]
                    )

            # -------- JS / TS --------
            else:
                if node.type == "class_declaration":
                    name = node.child_by_field_name("name")
                    if name:
                        ast_summary["classes"].append(
                            content[name.start_byte:name.end_byte]
                        )

                elif node.type in ("function_declaration", "method_definition"):
                    name = node.child_by_field_name("name")
                    if name:
                        ast_summary["functions"].append(
                            content[name.start_byte:name.end_byte]
                        )

                elif node.type == "import_statement":
                    ast_summary["imports"].append(
                        content[node.start_byte:node.end_byte]
                    )

                # Lightweight route detection
                snippet = content[node.start_byte:node.end_byte]
                if "Route" in snippet or "app.get" in snippet:
                    ast_summary["routes"].append(snippet)

            stack.extend(node.children)

    state.ast_summary = ast_summary
    return state
