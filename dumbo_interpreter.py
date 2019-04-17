import dumbo_syntaxique as syn

def analyseData(tree, assignation_found=False, variable_found=None, variables={}):
    if tree is not None:
        if tree.is_leaf():
            if tree.p_type=="variable":
                variables[tree.value]=[]
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
                t = analyseData(child, assignation_found, variable_found, variables)
                if t is not None:
                    assignation_found, variable_found, variables =t
            return assignation_found, variable_found, variables


if __name__ == "__main__":
    data="exemples/data_t1.dumbo"
    template="exemples/template1.dumbo"
    output=""
        
    data_tree=syn.analyse(data)
    print(analyseData(data_tree)[2])
    
    #template_tree=syn.analyse(template)
