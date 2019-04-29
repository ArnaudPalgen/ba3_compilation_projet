import dumbo_syntaxique as syn


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


def printTree(node):
    if node is not None:
        print(node, ": ", node.value)
        for child in node.children:
            printTree(child)


variables = {}

if __name__ == "__main__":
    data = "exemples/data_t1.dumbo"
    template = "exemples/template1.dumbo"
    output = "out.html"

    import dumbo_semantique as sem
    syntaxTree_data = syn.analyse(data)
    semantiqueTree_data = sem.buildTree(syntaxTree_data)
    # printTree(semantiqueTree_data)
    # print("--")
    semantiqueTree_data.eval()
    print(variables)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #syntaxTree_template = syn.analyse(template)
    #semantiqueTree_template = sem.buildTree(syntaxTree_template)
    #r = semantiqueTree_template.eval()
    # print(r)
    #tree = syn.analyse(template)
    #semantique = sem.buildTree(tree)
    # printTree(semantique)
    # print(var)
