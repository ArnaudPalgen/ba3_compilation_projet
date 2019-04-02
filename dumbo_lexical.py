import ply.lex as lex

#TODO peut etre table des symboles
bloc_open = 0

tokens = (
    "START_BLOC",
    "END_BLOC",
    "FOR",
    "IN",
    "DO",
    "ENDFOR",
    "STRING",
    "TEXT",
    "VARIABLE",
    "INSTRUCTION",
    "END_EXPRESSION",
    "ASSIGNATION",
    "LPARENT",
    "RPARENT",
    "PONCTUATION",
)

t_ignore = " \t"


def incremente():
    global bloc_open
    bloc_open += 1


def decremente():
    global bloc_open
    bloc_open -= 1


def setType(t):
    if bloc_open == 0:
        t.type = "TEXT"


def t_FOR(t):
    r"for"
    t.value = str(t.value)
    return t


def t_IN(t):
    r"in"
    t.value = str(t.value)
    return t


def t_DO(t):
    r"do"
    t.value = str(t.value)
    return t


def t_ENDFOR(t):
    r"endfor"
    t.value = str(t.value)
    return t


def t_START_BLOC(t):
    r"\{\{"
    t.value = str(t.value)
    # bloc_open += 1
    incremente()
    return t


def t_END_BLOC(t):
    r"\}\}"
    t.value = str(t.value)
    # bloc_open -= 1
    decremente()
    return t


def t_INSTRUCTION(t):
    r"print"
    t.value = str(t.value)

    return t


def t_PONCTUATION(t):
    r"\.|,"
    t.value = str(t.value)
    return t


def t_ASSIGNATION(t):
    r":="
    t.value = str(t.value)
    return t


def t_END_EXPRESSION(t):
    r";"
    t.Value = str(t.value)
    return t


def t_LPARENT(t):
    r"\("
    t.value = str(t.value)
    return t


def t_RPARENT(t):
    r"\)"
    t.Value = str(t.value)
    return t


def t_STRING(t):
    r"\'(\w|;|&|<|>|\"|_|-|\.|\\|\/|\\n|:|,|\ )+\'"
    t.value = str(t.value)
    return t


def t_VARIABLE(t):
    r"(\w|_)+"
    t.value = str(t.value)
    setType(t)

    return t


def t_TEXT(t):
    r"(\w|;|&|<|>|\"|_|-|\.|\\|\/|\\n|:|,)+"
    t.value = str(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


if __name__ == "__main__":
    import sys

    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))
