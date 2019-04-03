import ply.yacc as yacc
from dumbo_lexical import tokens


class Node:
    def __init__(self, p_type, children=[]):
        self.p_type = p_type
        self.children = children

    def isLeaf(self):
        return len(self.children) == 0


firstNode = None


def p_expression_programme(p):
    """programme: TEXT
    | TEXT programme
    | dumboBloc 
    | dumboBloc programme"""
    if len(p) == 2:
        p[0] = Node("programme", [p[1]])
    elif len(p) == 3:
        p[0] = Node("programme", [p[1], p[2]])


def p_expression_txt(p):
    """expression: TEXT """
    p[0] = Node("text", [p[1]])


def p_expression_dumboBloc(p):
    """dumboBloc: START_BLOC expression END_BLOC"""
    p[0] = Node("dumbo_bloc", [p[1], p[2], p[3]])
    # p[0]=p[2]
    # meme chose que pour p_parent tp3


def p_expression_expression_list(p):
    """ expression: expression END_EXPRESSION
                  | expression END_EXPRESSION expression"""
    if len(p) == 3:
        p[0] = Node("expression_list", [p[1], p[2]])
    elif len(p) == 4:
        p[0] = Node("expression_list", [p[1], p[2], p[3]])


def p_expression_expression(p):
    """expression: VARIABLE ASSIGNATION expression
		 | PRINT expression 
         | FOR VARIABLE IN expression DO expression ENDFOR"""
    if len(p) == 4:
        p[0] = Node("expression", [p[1], p[2], p[3]])
    elif len(p) == 3:
        p[0] = Node("expression", [p[1], p[2]])
    elif len(p) == 8:
        p[0] = Node("expression", [p[1], p[2], p[3], p[4], p[5], p[6], p[7]])


def p_expression_string_expression(p):
    """expression: STRING
	         | VARIABLE
                 | expression POINT expression"""
    if len(p) == 2:
        p[0] = Node("string_expression", [p[1]])
    elif len(p) == 4:
        p[0] = Node("string_expression", [p[1], p[2], p[3]])


def p_expression_string_list(p):
    """expression: LPARENT expression RPARENT"""
    p[0] = Node("expression_string_list", [p[1], p[2], p[3]])


def p_expression_string_list_interior(p):
    """expression: STRING 
                 | STRING VIRGULE expression"""
    if len(p) == 2:
        p[0] = Node("string_list_interior", [p[1]])
    elif len(p) == 4:
        p[0] = Node("string_list_interior", [p[1], p[2], p[3]])


def p_expression_string(p):
    """expression: STRING"""
    p[0] = Node("string", [p[1]])


def p_expression_variable(p):
    """expression : VARIABLE """
    p[0] = Node("variable", [p[1]])


def p_error(p):
    print("Syntax error in line {}".format(p.lineno))
    yacc.error()


yacc.yacc(outputdir="generated")

if __name__ == "__main__":
    import sys

    input = open(sys.argv[1]).read()
    result = yacc.parse(input, debug=False)
    print(input)
