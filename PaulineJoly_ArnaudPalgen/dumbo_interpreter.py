import copy
import sys
import os

"""
Interpreteur
"""


def _printTree(node):
    """
    Affiche un arbre
    : param node: un noeud(qui est aussi un arbre)
    """
    if node is not None:
        if node.value is not None:
            print(node, ": ", node.value)
        else:
            print(node)
        for child in node.children:
            _printTree(child)


def _getParams():
    """
    Recupere les trois fichiers necessaire au programme. Affiche l'aide si - h ou - -help est precise comme argument
    : return: les trois fichiers necessaire au programme
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
    if not syn.error:  # si pas d'erreur, on peut continuer
        semantiqueTree_data = sem.buildTree(
            syntaxTree_data)  # analyse semantique
        semantiqueTree_data.eval()  # execution du programme
    # on memorise le dictionnaire des variables car il sera reinitialise a la prochaine analyse
    var = copy.deepcopy(lex.variables)

    syntaxTree_template = syn.analyse(template)
    lex.variables.update(var)  # on met a jour le dictionnaire des variables
    if not syn.error:
        semantiqueTree_template = sem.buildTree(syntaxTree_template)
        result = semantiqueTree_template.eval()

        with open(output, 'w') as file:
            file.write(result)
