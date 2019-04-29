from dumbo_syntaxique import Node
from dumbo_interpreter import variables


def evalProgram(node):
    l = ""
    for child in node.children:
        l += child.eval()
    return l


def provisoire(node):
    # print("---v")
    # print(node)
    t1 = node.children[0].eval()
    t2 = node.children[1].eval()
    """print(t1)
    print(t2)
    print("---^")"""
    return[t1]+t2


def evalAssign(node):
    # print("here")
    print(variables)
    variables[node.children[0].eval()][1] = node.children[1].eval()
    print(variables)
    print("---")
    return ""


def evalFor(node):
    #[buildTree(tree.children[1]), liste, buildTree(tree.children[5])]
    l = ""
    list_value = None
    if node.children[1].p_type == "variable":
        list_name = node.children[1].eval()
        try:
            list_value = variables[list_name][1]
        except KeyError as identifier:
            print("ERROR: variable not defined")
            exit()
    else:
        list_value = node.children[1].eval()

    var_name = node.children[0].eval()
    var_value = None  # si la variable existe deja dans le dico, on retient sa valeur pour la remettre a la fin

    if var_name in variables:
        var_value = variables[var_name][1]

    for item in list_value:
        variables[var_name][1] = item
        l += node.children[2].eval()

    if var_value is None:
        variables.pop(var_name)
    else:
        variables[var_name][1] = var_value

    return l


def eval_integer_expression(node):
    op = node.p_type
    a = node.children[0].eval()
    b = node.children[1].eval()
    if op == "+":
        return a + b
    elif op == "-":
        return a-b
    elif op == "*":
        return a*b
    elif op == "/":
        return a/b  # TODO essayer avec b = 0


def eval_boolean_expression(node):
    #Node(tree.children[1], [buildTree(tree.children[0]), buildTree(tree.children[2])], function=eval_boolean_expression)
    op = node.p_type
    a = node.children[0].eval()
    b = node.children[1].eval()
    if op == "and":
        return a and b
    elif op == "or":
        return a or b


def eval_comparator_expression(node):
    #Node(tree.children[1], [tree.children[0], tree.children[2]], function = eval_comparator_expression)
    op = node.p_type
    a = node.children[0].eval()
    b = node.children[1].eval()

    if op == "<":
        return a < b
    elif op == ">":
        return a > b
    elif op == "=":
        return a == b
    elif op == "!=":
        return a != b


def buildTree(tree):
    if tree is None:
        return None
    elif tree.p_type == "programme":
        if len(tree.children) == 1:  # le fils est un texte ou un dumboBloc
            return buildTree(tree.children[0])
        elif len(tree.children) == 2:
            return Node("program", [buildTree(tree.children[0]), buildTree(tree.children[1])], function=evalProgram)
    elif tree.p_type == "text":  # program -> text
        return Node("text", value=tree.value)

    elif tree.p_type == "dumbo_bloc":  # program -> dumboBlock
        return buildTree(tree.children[1])

    elif tree.p_type == "expression_list":  # dumboBloc -> expression list
        if len(tree.children) == 2:  # une seul expression
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node("expression_list", [buildTree(tree.children[0]), buildTree(tree.children[2])], function=evalProgram)
    elif tree.p_type == "expression":  # expressionList -> expression
        if len(tree.children) == 2:  # c'est un print
            return Node("print", [buildTree(tree.children[1])], function=evalProgram)
        elif len(tree.children) == 3:  # c'est une assignation
            key = buildTree(tree.children[0])
            value = buildTree(tree.children[2])
            variables[key.value] = [value.p_type, None]
            return Node("assignation", [key, value], function=evalAssign)
        elif len(tree.children) == 5:  # c'est un if
            return Node("if", [buildTree(tree.children[1]), buildTree(tree.children[3])], function=lambda node: (node.children[3].eval() if node.children[1].eval() else ""))
        elif len(tree.children) == 7:  # c'est un for
            liste = buildTree(tree.children[3])

            if (liste.p_type == "variable" and variables[liste.value][0] == "string_list") or liste.p_type == "string_list":
                return Node("for", [buildTree(tree.children[1]), liste, buildTree(tree.children[5])], function=evalFor)
            else:
                print(
                    "ERREUR SEMANTIQUE: Le type attendu n'est pas correct")
                return None

    elif tree.p_type == "string_list":  # expression -> string_list
        #print("in string list:", tree)
        return buildTree(tree.children[1])

    elif tree.p_type == "string_expression":
        #print("string expression:", tree)
        if len(tree.children) == 1:
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node("concatenation", [buildTree(tree.children[0]), buildTree(tree.children[2])], function=lambda node: node.children[0].eval() + node.children[1].eval())

    elif tree.p_type == "integer_expression":
        if len(tree.children) == 1:  # juste un entier
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:  # une operation
            return Node(tree.children[1], [buildTree(tree.children[0]), buildTree(tree.children[2])], function=eval_integer_expression)

    elif tree.p_type == "string_list_interior":
        #print("string list interior:", tree)
        if len(tree.children) == 1:  # un string
            r = Node("string_list", [buildTree(
                tree.children[0])], function=lambda node: [node.children[0].eval()])
            return r
        elif len(tree.children) == 3:  # liste de string
            c1 = buildTree(tree.children[0])
            c2 = buildTree(tree.children[2])

            r2 = Node("string_list", children=[c1, c2], function=provisoire)
            return r2

    elif tree.p_type == "boolean_expression":
        if len(tree.children) == 1:
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node(tree.children[1], [buildTree(tree.children[0]), buildTree(tree.children[2])], function=eval_boolean_expression)

    elif tree.p_type == "comparator_expression":
        return Node(tree.children[1], [tree.children[0], tree.children[2]], function=eval_comparator_expression)

    elif tree.p_type == "variable":
        return Node("variable", value=tree.value)
    elif tree.p_type == "boolean":
        return Node("boolean", value=tree.value)

    elif tree.p_type == "string":
        #print("stringSe:", tree, tree.value)
        r3 = Node("string", value=tree.value)
        return r3

    elif tree.p_type == "integer":
        return Node("integer", value=tree.value)

    else:
        print("ERREUR: type inconnu ", tree.p_type)
        exit()
