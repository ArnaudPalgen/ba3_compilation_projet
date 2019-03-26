import ply.lex as lex

tokens=("START_BLOC", "END_BLOC", "STRING", "TEXT", "INSTRUCTION", "END_EXPRESSION", "ASSIGNATION", "LPARENT", "RPARENT", "PONCTUATION")

t_START_BLOC=r'\{\{'

t_END_BLOC=r'\}\}'

def t_INSTRUCTION(t):
    r'for|in|do|endfor|print'
    t.value=str(t.value)
    return t

def t_PONCTUATION(t):
    r'\.|,'
    t.value=str(t.value)
    return t

t_ASSIGNATION=r':='

t_END_EXPRESSION=r';'

t_LPARENT=r'\('

t_RPARENT=r'\)'

def t_STRING(t):
    r' \' (\w |;| &| < |> |"| −| \.| \\|\/| \n| \ p| :| , )+ \' '
    t.value=str(t.value)
    return t

def t_TEXT(t):
    r'(\w |;| &| < | > |"| −| \.| \\|\/| \n| \ p| :| , )+'
    t.value=str(t.value)
    return t

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


if __name__ == "__main__":
    import sys
    
    lexer = lex.lex()

    lexer.input(sys.stdin.read())
    for token in lexer:
        print("line %d : %s (%s) " %(token.lineno, token.type, token.value))