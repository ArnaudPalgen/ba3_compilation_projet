import ply.lex as lex


bloc_open = 0

variables = {}  # value: (type, valeur)


tokens = (
    "START_BLOC",
    "END_BLOC",
    "FOR",
    "IN",
    "DO",
    "ENDFOR",
    "INTEGER",
    "OP",
    "OP_LOGIQUE",
    "COMPARATOR",
    "IF",
    "ENDIF",
    "BOOL",
    "STRING",
    "TEXT",
    "VARIABLE",
    "PRINT",
    "END_EXPRESSION",
    "ASSIGNATION",
    "LPARENT",
    "RPARENT",
    "POINT",
    "VIRGULE",
)

states = (('inBloc', 'inclusive'),)

t_inBloc_ignore = " \t"


def t_inBloc_FOR(t):
    r"for"
    t.value = str(t.value)
    return t


def t_inBloc_IN(t):
    r"in"
    t.value = str(t.value)
    return t


def t_inBloc_DO(t):
    r"do"
    t.value = str(t.value)
    return t


def t_inBloc_OP(t):
    r"\*|/|\+|-"
    t.value = str(t.value)
    return t


def t_inBLoc_OP_LOGIQUE(t):
    r"or|and"
    t.value = str(t.value)
    return t


def t_inBloc_COMPARATOR(t):
    r">|<|=|!="
    t.value = str(t.value)
    return t


def t_inBloc_IF(t):
    r"if"
    t.value = str(t.value)
    return t


def t_inBloc_ENDIF(t):
    r"endif"
    t.value = str(t.value)
    return t


def t_inBloc_BOOL(t):
    r"true|false"
    t.value = (str(t.value) == 'true')
    return t


def t_inBloc_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_inBloc_ENDFOR(t):
    r"endfor"
    t.value = str(t.value)
    return t


def t_START_BLOC(t):
    r"\{\{"
    t.value = str(t.value)
    t.lexer.begin('inBloc')
    return t


def t_inBloc_END_BLOC(t):
    r"\}\}"
    t.value = str(t.value)
    t.lexer.begin('INITIAL')
    return t


def t_inBloc_PRINT(t):
    r"print"
    t.value = str(t.value)

    return t


def t_inBloc_POINT(t):
    r"\."
    t.value = str(t.value)
    return t


def t_inBloc_VIRGULE(t):
    r","
    t.value = str(t.value)
    return t


def t_inBloc_ASSIGNATION(t):
    r":="
    t.value = str(t.value)
    return t


def t_inBloc_END_EXPRESSION(t):
    r";"
    t.Value = str(t.value)
    return t


def t_inBloc_LPARENT(t):
    r"\("
    t.value = str(t.value)
    return t


def t_inBloc_RPARENT(t):
    r"\)"
    t.Value = str(t.value)
    return t


def t_inBloc_STRING(t):
    r"\'(\w|;|&|<|>|\"|_|-|\.|\\|\/|\\n|:|,|\ |=|\n|\t)+\'"
    t.value = str(t.value)
    return t


def t_inBloc_VARIABLE(t):
    r"(\w|_)+"
    t.value = str(t.value)
    variables[t.value] = (None, None)
    return t


def t_TEXT(t):
    r"(\w|;|&|<|>|\"|_|-|\.|\\|\/|\\n|:|,|\t|\ )+"
    t.value = str(t.value)
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

if __name__ == "__main__":
    import sys

    lexer.input(sys.stdin.read())
    for token in lexer:
        print("line %d : %s (%s) " % (token.lineno, token.type, token.value))
