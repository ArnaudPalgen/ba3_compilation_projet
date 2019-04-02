import ply.yacc as yacc
from dumbo_lexical import tokens


class Node(object):
    
    def __init__(self, t_value, t_type):
        self.t_value=t_value
        self.t_type=t_type
        self.childs=[]
    
    def addChild(self, child):
        self.childs.append(child)


#def p_expression_programme(p):
    #"""expression: TEXT
		 #| TEXT expression
		 #| dumboBloc doit-on créer un token dumboBloc?
		 #| dumboBloc expression""" 
    #p[0]=p[1]

def p_expression_txt(p):
    """expression: TEXT """

def p_expression_dumboBloc(p):
    """expression: START_BLOC expression END_BLOC"""
    p[0]=p[2]
    # meme chose que pour p_parent tp3

def p_expression_expression_list(p):
    """ expression: expression END_EXPRESSION
                  | expression END_EXPRESSION expression"""
    p[0]=?

def p_expression_expression(p):
    """expression: VARIABLE ASSIGNATION expression
		 | PRINT expression"""
    p[0]=p[2]

def p_expression_expression(p):
    """expression: FOR VARIABLE IN expression DO expression ENDFOR"""
    p[0]=?

def p_expression_string_expression(p):
    """expression: STRING
	         | VARIABLE
                 | expression POINT expression"""
    p[0]=? 

def p_expression_string_list(p):
    """expression: LPARENT expression RPARENT"""
    p[0] = p[2]

def p_expression_string_list_interior(p):
    """expression: STRING 
                 | STRING VIRGULE expression"""
    p[0]=?

def p_expression_string(p):
    """expression: STRING"""
    p[0]=p[1]

def p_expression_variable(p):
    """expression : VARIABLE """
    p[0]=p[1]

def p_error(p):
    print("Syntax error in line {}" .format(p.lineno))
    yacc.error()

yacc.yacc(outputdir="generated")

if __name__ == "__main__":
    import sys

    input = open(sys.argv[1]).read()
    result = yacc.parse(input, debug=False)
    print(input)
