import os
from tree_sitter import Language, Parser

# get from env

LIB = os.environ["TREE_SITTER_LIB"]
# Language.build_library(
#     # Store the library in the `build` directory
#     TREE_SITTER_LIB,

#     # Include one or more languages
#     [
#         '/home/cong/sm/lab/tree-sitter-bash',
#     ]
# )

BASH_LANGUAGE = Language(LIB, 'bash')


def query_bash(file: str, query: str):
    parser = Parser()
    parser.set_language(BASH_LANGUAGE)
    source = open(file, 'r').read()
    tree = parser.parse(bytes(source, "utf8"))

    query = BASH_LANGUAGE.query(query)

    captures = query.captures(tree.root_node)
    return captures


def query_bash_function_line_range(p, name):
    q = "(function_definition name: (word) @func.def)"
    captures = query_bash(p, q)
    for capture in captures:
        cap = capture[0]
        kind = capture[1]
        if kind != "func.def":
            continue
        fn_name = str(cap.text, "utf8")
        if fn_name == name:
            s = cap.start_point
            e = cap.end_point
            print(s[1], e[1])