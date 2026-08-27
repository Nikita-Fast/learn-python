from lark import Lark, Transformer

# 1. Define the SCPI Grammar
scpi_grammar = """
    start: command_list
    command_list: command (";" command)*
    command: [":" ] header_path [arguments]

    header_path: keyword (":" keyword)*

    // Matches SCPI style UPPERCASE short form and lowercase long form extension
    // Example: VOLTage matches VOLT or VOLTAGE
    keyword: SHORT_FORM [LONG_FORM_EXT] [INDEX]

    arguments: " " argument ("," argument)*
    ?argument: number_with_unit | NUMBER | TEXT

    number_with_unit: NUMBER UNIT
    UNIT: TEXT

    SHORT_FORM: /[A-Z]{3,4}/
    LONG_FORM_EXT: /[a-z]+/
    INDEX: /[0-9]+/
    TEXT: /[A-Za-z_]+/

    %import common.INT
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

# 2. Create the Parser
# Using the Earley parser algorithm (a robust dynamic top-down parser style)
parser = Lark(scpi_grammar, start='start', parser='earley')

# 3. Test the Parser
sample_command = ":SOURce1:VOLTage:LEVel 5.0V"

try:
    # Parse the command and generate an Abstract Syntax Tree (AST)
    parsed_tree = parser.parse(sample_command)
    print("Successfully Parsed Tree:")
    print(parsed_tree.pretty())
except Exception as e:
    print(f"Parsing error: {e}")