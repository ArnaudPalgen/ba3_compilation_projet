from dumbo_syntaxique import Node
from dumbo_lexical import variables


def buildTree(tree):
    if tree is None:
        return None
    if tree.p_type == "programme":
        if len(tree.children) == 1:  # le fils est un texte ou un dumboBloc
            return buildTree(tree.children[0])
        elif len(tree.children) == 2:
            return Node("program", [buildTree(tree.children[0]), buildTree(tree.children[1])])
    if tree.p_type == "text":  # program -> text
        return Node("text", value=tree.value)

    if tree.p_type == "dumbo_bloc":  # program -> dumboBlock
        return buildTree(tree.children[1])

    if tree.p_type == "expression_list":  # dumboBloc -> expression list
        if len(tree.children) == 2:  # une seul expression
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node("expression_list", [buildTree(tree.children[0]), buildTree(tree.children[2])])
    if tree.p_type == "expression":  # expressionList -> expression
        if len(tree.children) == 2:
            return buildTree(tree.children[1])
        elif len(tree.children) == 3:
            key = buildTree(tree.children[0])
            value = buildTree(tree.children[2])
            variables[key.value] = (value.p_type, None)
            return Node("assignation", [key, value])
        elif len(tree.children) == 5:
            return Node("if", [buildTree(tree.children[1]), buildTree(tree.children[3])])
        elif len(tree.children) == 7:
            liste = buildTree(tree.children[3])
            if (liste.p_type == "variable" and variables[liste.value][0] == "string_list") or liste.p_type == "string_list":
                return Node("for", [buildTree(tree.children[1]), liste, buildTree(tree.children[5])])
            else:
                print(
                    "ERREUR SEMANTIQUE: Le type attendu n'est pas correct")  # todo
                return None

    if tree.p_type == "string_list":  # expression -> string_list
        return buildTree(tree.children[1])

    if tree.p_type == "string_expression":
        if len(tree.children) == 1:
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node("concatenation", [buildTree(tree.children[0]), buildTree(tree.children[2])])

    if tree.p_type == "integer_expression":
        if len(tree.children) == 1:
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node(tree.children[1], [tree.children[0], tree.children[2]])

    if tree.p_type == "string_list_interior":
        if len(tree.children) == 1:
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node("string_list", [buildTree(tree.children[0]), buildTree(tree.children[2])])

    if tree.p_type == "boolean_expression":
        if len(tree.children) == 1:
            return buildTree(tree.children[0])
        elif len(tree.children) == 3:
            return Node(tree.children[1], [buildTree(tree.children[0]), buildTree(tree.children[2])])

    if tree.p_type == "variable":
        return Node("variable", value=tree.value)
    if tree.p_type == "boolean":
        return Node("boolean", value=tree.value)

    if tree.p_type == "string":
        return Node("string", value=tree.value)

    if tree.p_type == "integer":
        return Node("integer", value=tree.value)

    else:
        print("ERREUR: type inconnu ", tree.p_type)
