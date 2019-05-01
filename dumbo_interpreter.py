import copy
import sys
import os

"""
def analyseData(tree, assignation_found=False, variable_found=None, variables={}):
    if tree is not None:
        if tree.is_leaf():
            if tree.p_type == "variable":
                variables[tree.value] = []
                return (assignation_found, tree.value, variables)
            if tree.p_type == ":=":
                return (True, variable_found, variables)
            if tree.p_type == "string" and assignation_found and variable_found is not None:
                variables[variable_found].append(tree.value)
                return (assignation_found, variable_found, variables)
            if tree.p_type == ";":
                return (False, None, variables)

        else:

            for child in tree.children:
                t = analyseData(child, assignation_found,
                                variable_found, variables)
                if t is not None:
                    assignation_found, variable_found, variables = t
            return assignation_found, variable_found, variables


def analyse_template(tree, variables, treeType="", info=None, result=""):
    if tree is not None:
        if tree.is_leaf():
            if tree.p_type == "text":
                result += tree.value  # write data
                return "text", variables, info, result
            elif tree.p_type == "print":
                return "print", variables, info, result
            elif tree.p_type == "for":
                return "for", variables, info, result
            elif tree.p_type == "in":
                return "in", variables, info, result
            elif tree.p_type == "string":
                if treeType == "print":
                    result += tree.value
                    return "print", variables, info, result
                if treeType == "in":
                    variables[info].append(tree.value)
                    return "in", variables, info, result

            elif tree.p_type == "variable":
                if treeType == "for":
                    variables[tree.value] = []
                    return "for", variables, tree.value, result
                elif treeType == "print":

                    data = variables[tree.value]

                    for d in data:
                        result += d+", "
                    result = result[0:-2]
                    return "print", variables, info, result
                elif treeType == "in":
                    variables[info] = variables[tree.value]
                    return "in", variables, info, result
            elif tree.p_type == "do":
                return "do", variables, info, result
            elif tree.p_type == "expression_list":
                if treeType == "do":
                    data = variables[info]
                    for item in data:
                        variables[info] = item
                        for child in tree.children:
                            analyse_template(child, variables)
                    variables.pop(info)
                    return "expression_list", variables, None, result

        else:
            for child in tree.children:
                t = analyse_template(child, variables, treeType, info, result)
                if t is not None:
                    treeType, variables, info, result = t
            return treeType, variables, info, result
"""


def _printTree(node):
    """
    Affiche un arbre
    :param node: un noeud (qui est aussi un arbre)
    """
    if node is not None:
        print(node, ": ", node.value)
        for child in node.children:
            _printTree(child)


def _getParams():
    """
    Recupere les trois fichiers necessaire au programme. Affiche l'aide si -h ou --help est precise comme argument
    """

    if "-h" in sys.argv or "--help" in sys.argv:
        print("\nAide pour dumbo_interpreter")
        print("\nDESCRIPTION:\n   dumbo_interpreter permet de générer un fichier contenant du texte en fonction des données reçues.")
        print("\nPARAMETRES:\n   -un fichier de données,\n   -un fichier template dans lequel les données seront injetées\n   -un fichier de sortie\n")
        exit()
    else:
        if len(sys.argv) != 4:
            print("ERROR: Nombre d'arument attendu: 3 nombre donné: " +
                  str(len(sys.argv)-1))
            exit()
        else:
            if (not os.path.isfile(sys.argv[1])) or (not os.path.isfile(sys.argv[2])):
                print(
                    "ERROR: fichier de donnée ou fichier template n'est pas un fichier existant")
                exit()
            if(os.path.isfile(sys.argv[3])):
                r = input(
                    "WARNING: Le fichier de sortie existe déja et sera écrasé. Voulez-vous continuer ? [O/n] ")
                if r not in ['O', 'o']:
                    print("annulé")
                    exit()
            return sys.argv[1], sys.argv[2], sys.argv[3]


if __name__ == "__main__":
    data, template, output = _getParams()

    import dumbo_syntaxique as syn
    import dumbo_lexical as lex
    import dumbo_semantique as sem

    syntaxTree_data = syn.analyse(data)  # analyse syntaxique
    if not syn.error:
        semantiqueTree_data = sem.buildTree(
            syntaxTree_data)  # analyse semantique
        semantiqueTree_data.eval()  # execution du programme
    var = copy.deepcopy(lex.variables)

    syntaxTree_template = syn.analyse(template)
    lex.variables.update(var)
    if not syn.error:
        semantiqueTree_template = sem.buildTree(syntaxTree_template)
        result = semantiqueTree_template.eval()

        with open(output, 'w') as file:
            file.write(result)
