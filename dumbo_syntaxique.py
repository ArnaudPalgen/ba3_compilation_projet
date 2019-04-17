import ply.yacc as yacc
import dumbo_lexical as lex
from dumbo_lexical import tokens


class Node:
    def __init__(self, p_type, children=[], value=None):
        self.p_type = p_type
        self.children = children
        self.value=value

    def is_leaf(self):
        return len(self.children) == 0
    def __str__(self):
        return self.p_type

def p_expression_programme(p):
    """programme : text
    | text programme
    | dumboBloc 
    | dumboBloc programme"""
    if len(p) == 2:
        p[0] = Node("programme", [p[1]])
    elif len(p) == 3:
        p[0] = Node("programme", [p[1], p[2]])


def p_expression_dumboBloc(p):
    """dumboBloc : start_bloc expression_list end_bloc"""
    p[0] = Node("dumbo_bloc", [p[1], p[2], p[3]])
    # p[0]=p[2]
    # meme chose que pour p_parent tp3


def p_expression_expression_list(p):
    """ expression_list : expression end_expression
                  | expression end_expression expression_list"""
    if len(p) == 3:
        p[0] = Node("expression_list", [p[1], p[2]])
    elif len(p) == 4:
        p[0] = Node("expression_list", [p[1], p[2], p[3]])


def p_expression_expression(p):
    """expression : variable assignation string_expression
         | variable assignation string_list
		 | print string_expression 
         | for variable in string_list do expression_list endfor
         | for variable in variable do expression_list endfor"""
    if len(p) == 4:
        p[0] = Node("expression", [p[1], p[2], p[3]])
    elif len(p) == 3:
        p[0] = Node("expression", [p[1], p[2]])
    elif len(p) == 8:
        p[0] = Node("expression", [p[1], p[2], p[3], p[4], p[5], p[6], p[7]])


def p_expression_string_expression(p):
    """string_expression : string
	         | variable
                 | string_expression point string_expression"""
    if len(p) == 2:
        p[0] = Node("string_expression", [p[1]])
    elif len(p) == 4:
        p[0] = Node("string_expression", [p[1], p[2], p[3]])


def p_expression_string_list(p):
    """string_list : lparent string_list_interior rparent"""
    p[0] = Node("expression_string_list", [p[1], p[2], p[3]])


def p_expression_string_list_interior(p):
    """string_list_interior : string 
                 | string virgule string_list_interior"""
    if len(p) == 2:
        p[0] = Node("string_list_interior", [p[1]])
    elif len(p) == 4:
        p[0] = Node("string_list_interior", [p[1], p[2], p[3]])


def p_expression_string(p):
    """string : STRING"""
    p[0] = Node("string", value=p[1])


def p_expression_variable(p):
    """variable : VARIABLE """
    p[0] = Node("variable", value=p[1])


def p_expression_print(p):
    """print : PRINT """
    p[0] = Node("print")


def p_expression_txt(p):
    """text : TEXT """
    p[0] = Node("text", value=p[1])


def p_expression_start_bloc(p):
    """start_bloc : START_BLOC"""
    p[0] = Node("\{\{")


def p_expression_end_bloc(p):
    """end_bloc : END_BLOC"""
    p[0] = Node("\}\}")


def p_expression_end_expression(p):
    """end_expression : END_EXPRESSION"""
    p[0] = Node(";")


def p_expression_assignation(p):
    """assignation : ASSIGNATION"""
    p[0] = Node(":=")


def p_expression_for(p):
    """for : FOR"""
    p[0] = Node("for")


def p_expression_in(p):
    """in : IN"""
    p[0] = Node("in")


def p_expression_do(p):
    """do : DO"""
    p[0] = Node("do")


def p_expression_endfor(p):
    """endfor : ENDFOR"""
    p[0] = Node("endfor")


def p_expression_pont(p):
    """point : POINT"""
    p[0] = Node("point")


def p_expression_lparent(p):
    """lparent : LPARENT"""
    p[0] = Node("lparent")


def p_expression_rparent(p):
    """rparent : RPARENT"""
    p[0] = Node("rparent")


def p_expression_virgule(p):
    """virgule : VIRGULE"""
    p[0] = Node("virgule")


def printTree(node):
    if node is not None:
        print(node, ": ", node.value)
        for child in node.children:
            printTree(child)


def p_error(p):
    print("Syntax error in line {}".format(p.lineno))
    yacc.errok()


yacc.yacc(outputdir="generated")

def analyse(file):
    f=open(file).read()
    return yacc.parse(f, debug=False)

if __name__ == "__main__":
    import sys

    input = open(sys.argv[1]).read()
    result = yacc.parse(input, debug=False)
    printTree(result)