__author__ = 'Rohith Varma Gaddam','Pradeep'
__version__ = '1.0'
'''This file contains the evaluator which evaluates the parse tree'''
import sys
import os
currentDirectory = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(currentDirectory, '.')))
import Compiler.parse as parse

function_hash={}
class Evaluate:
    def __init__(self):
        self.variable_env = {}

    def eval_block(self,tree):
        statement =  tree[1]
        self.eval_statement(statement)
        if len(tree)==3:
            self.eval_block(tree[2])

    def eval_statement(self,tree):
        if tree[0]=='t_var':
            self.eval_declaration(tree)
        elif tree[0] == 't_initString':
            self.eval_initializationString(tree)
        elif tree[0] == 't_init':
            self.eval_initialization(tree)
        elif tree[0] == 't_assignString':
            self.eval_assignString(tree)
        elif tree[0] == 't_assign':
            self.eval_assign(tree)
        elif tree[0] == 't_print':
            self.eval_print(tree)
        elif tree[0] == 't_if':
            self.eval_if(tree)
        elif tree[0] == 't_while':
            self.eval_while(tree)
        elif tree[0] == 't_for':
            self.eval_for(tree,0)
        elif tree[0] == 't_for_range':
            self.eval_forRange(tree)
        elif tree[0] == 't_increment':
            self.eval_inc(tree)
        elif tree[0] == 't_decrement':
            self.eval_dec(tree)
        elif tree[0] == 't_funcall':
            self.eval_funcall(tree,0)



    #DECLARATION
    def eval_declaration(self,tree):
        self.variable_env[tree[1]] = None



    #INTIALIZATION
    def eval_initializationString(self,tree):
        self.variable_env[tree[1]] = tree[2][1][1:-1]

    def eval_initialization(self,tree):
        if tree[2][0] == 't_or':
            val = self.eval_or(tree[2])
        elif tree[2][0] == 'boolean':
            val = self.eval_boolean(tree[2])
        self.variable_env[tree[1]] = val

    def eval_assignString(self,tree):
        self.variable_env[tree[1]] = tree[2][1][1:-1]

    def eval_assign(self,tree):
        if tree[2][0] == 't_or':
            val = self.eval_or(tree[2])
        elif tree[2][0] == 'boolean':
            val = self.eval_boolean(tree[2])
        if tree[1] not in self.variable_env.keys():
            sys.exit("Error "+str(tree[len(tree)-1])+ ": variable "+tree[1]+" doesn't exist")
        else:
            self.variable_env[tree[1]] = val

    #IF
    def eval_if(self,tree):
        b = False
        if tree[1][0] == 't_or':
            b = self.eval_or(tree[1])
        elif tree[1][0] == 'boolean':
            b = self.eval_boolean(tree[1])
        if b:
            self.eval_block(tree[2])
        else:
            self.eval_elif(tree[3])

    def eval_elif(self,tree):
        '''elif : ELSEIF  boolean  '{'  block  '}'  elif '''
        b = False
        if tree[1][0] == 't_or':
            b = self.eval_or(tree[1])
        elif tree[1][0] == 'boolean':
            b = self.eval_boolean(tree[1])

        if tree[0] == 't_elif':
            if b:
                self.eval_block(tree[2])
            else:
                self.eval_elif(tree[3])
        elif tree[0] == 't_else':
            self.eval_block(tree[1])
        else:
            pass

    #WHILE
    def eval_while(self,tree):
        b = False
        if tree[1][0] == 't_or':
            b = self.eval_or(tree[1])
        elif tree[1][0] == 'boolean':
            b = self.eval_boolean(tree[1])
        if b:
            self.eval_block(tree[2])
            self.eval_while(tree)
            # verify the tree passed in recursion
        else:
            pass

    #FOR
    def eval_for(self,tree,flag):
        global variable_env
        if flag==0:
            self.eval_initialization(tree[1])
        b = False
        if tree[2][0] == 't_or':
            b = self.eval_or(tree[2])
        elif tree[2][0] == 'boolean':
            b = self.eval_boolean(tree[2])
        if b:
            self.eval_block(tree[4])
            # should call unary and assign
            self.eval_statement(tree[3])
            self.eval_for(tree,1)

    def eval_forRange(self,tree):
        global variable_env
        id = tree[1]
        val1 = self.eval_expression(('t_expression',tree[2]))
        val2 = self.eval_expression(('t_expression',tree[3]))
        for i in range(int(val1),int(val2)):
            self.variable_env[id] = i
            self.eval_block(tree[4])



    #UNARY
    def eval_inc(self,tree):
        val = self.eval_id(tree[1])
        if not isinstance(val,int):
            sys.exit("Error at line "+str(tree[len(tree)-1])+": "+ tree[1][1]+" is not integer and cannot perform increment")
        self.variable_env[tree[1][1]] = val+1
    def eval_dec(self,tree):
        global variable_env
        val = self.eval_id(tree[1])
        if not isinstance(val,int):
            sys.exit("Error at line "+str(tree[len(tree)-1])+": "+ tree[1][1]+" is not integer and cannot perform decrement")
        self.variable_env[tree[1][1]] = val-1


    #PRINT
    def eval_print(self,tree):
        s = self.eval_plist(tree[1])
        print(s)
    def eval_plist(self,tree):
        s = str(self.eval_pstat(tree[1]))
        if len(tree)==3:
            s+=self.eval_plist(tree[2])
        return s
    def eval_pstat(self,tree):
        if tree[0]=='t_string':
            return tree[1][1:-1]
        else:
            if tree[0] == 't_or':
                val = self.eval_or(tree)
            elif tree[0] == 'boolean':
                val = self.eval_boolean(tree)
            return val


    def eval_or(self,tree):
        if tree[1][0] == 't_or':
            val1 = self.eval_or(tree[1])
        elif tree[1][0] == 'boolean':
            val1 = self.eval_boolean(tree[1])

        if tree[2][0] == 't_and':
            val2 = self.eval_and(tree[2])
        elif tree[2][0] == 'boolterm':
            val2 = self.eval_boolterm(tree[2])
        if isinstance(val1,str) or isinstance(val2,str):
            sys.exit("Error at line "+str(tree[len(tree)-1])+": '||' operator doesn't support strings")
        return val1 or val2


    def eval_boolean(self,tree):
        if tree[1][0] == 't_and':
            val = self.eval_and(tree[1])
        elif tree[1][0] == 'boolterm':
            val = self.eval_boolterm(tree[1])
        return val

    def eval_and(self,tree):
        if tree[1][0] == 't_and':
            val1 = self.eval_and(tree[1])
        elif tree[1][0] == 'boolterm':
            val1 = self.eval_boolterm(tree[1])

        if tree[2][0] == 't_not':
            val2 = self.eval_not(tree[2])
        elif tree[2][0] == 'boolterm1':
            val2 = self.eval_boolterm1(tree[2])
        if isinstance(val1,str) or isinstance(val2,str):
            sys.exit("Error at line "+str(tree[len(tree)-1])+" :'&&' operator doesn't support strings")
        return val1 and val2


    def eval_boolterm(self,tree):
        if tree[1][0] == 't_not':
            val = self.eval_not(tree[1])
        elif tree[1][0] == 'boolterm1':
            val = self.eval_boolterm1(tree[1])
        return val

    def eval_not(self,tree):
        if tree[1][0] == 't_condition':
            val = self.eval_condition(tree[1])
        elif tree[1][0] == 't_expression':
            val = self.eval_expression(tree[1])
        elif tree[1][0] == 't_boolvalue':
            val = self.eval_boolvalue(tree[1])
        if isinstance(val,str):
            sys.exit(" Error at line "+ str(tree[len(tree)-1]) +" :'!' operator doesn't support strings ")
        return not(val)

    def eval_boolterm1(self,tree):
        global variable_env
        if tree[1][0] == 't_condition':
            val = self.eval_condition(tree[1])
        elif tree[1][0] == 't_expression':
            val = self.eval_expression(tree[1])
        elif tree[1][0] == 't_boolvalue':
            val = self.eval_boolvalue(tree[1])
        return val

    def eval_boolvalue(self,tree):
        return tree[1]

    def eval_condition(self,tree):
        if tree[1][1][0] == 't_plus':
            val1 = self.eval_plus(tree[1][1])
        elif tree[1][1][0] == 't_minus':
            val1 = self.eval_minus(tree[1][1])
        elif tree[1][1][0] == 'expression':
            val1 = self.eval_expr(tree[1][1])

        if tree[1][2][0] == 't_plus':
            val2 = self.eval_plus(tree[1][1])
        elif tree[1][2][0] == 't_minus':
            val2 = self.eval_minus(tree[1][2])
        elif tree[1][2][0] == 'expression':
            val2 = self.eval_expr(tree[1][2])

        if tree[1][0] == 't_gt':
            return val1 > val2
        elif tree[1][0] == 't_lt':
            return val1 < val2
        elif tree[1][0] == 't_gtEql':
            return val1 >= val2
        elif tree[1][0] == 't_ltEql':
            return val1 <= val2
        elif tree[1][0] == 't_notEql':
            return val1 != val2
        elif tree[1][0] == 't_bEql':
            return val1 == val2


    def eval_expression(self,tree):
        if tree[1][0]== 't_plus':
            val = self.eval_plus(tree[1])
        elif tree[1][0]== 't_minus':
            val = self.eval_minus(tree[1])
        elif tree[1][0]== 'expression':
            val = self.eval_expr(tree[1])
        return val

    def eval_plus(self,tree):
        if tree[1][0]== 't_plus':
            val1 = self.eval_plus(tree[1])
        elif tree[1][0]== 't_minus':
            val1 = self.eval_minus(tree[1])
        elif tree[1][0]== 'expression':
            val1 = self.eval_expr(tree[1])

        if tree[2][0]== 't_multi':
            val2 = self.eval_multi(tree[2])
        elif tree[2][0]== 't_div':
            val2 = self.eval_div(tree[2])
        elif tree[2][0]== 'term':
            val2 = self.eval_term(tree[2])
        if isinstance(val1,str) and isinstance(val2,str) or isinstance(val1,int) and isinstance(val2,int):
            return val1+val2
        else:
            sys.exit("Error at line "+str(tree[len(tree)-1])+" : '+' supports only both strings and both integers")

    def eval_minus(self,tree):
        if tree[1][0]== 't_plus':
            val1 = self.eval_plus(tree[1])
        elif tree[1][0]== 't_minus':
            val1 = self.eval_minus(tree[1])
        elif tree[1][0]== 'expression':
            val1 = self.eval_expr(tree[1])

        if tree[2][0]== 't_multi':
            val2 = self.eval_multi(tree[2])
        elif tree[2][0]== 't_div':
            val2 = self.eval_div(tree[2])
        elif tree[2][0]== 'term':
            val2 = self.eval_term(tree[2])
        if not(isinstance(val1,int) and isinstance(val2,int)):
            sys.exit("Error at line "+str(tree[len(tree)-1])+" : '-' supports only integers")
        return val1-val2

    def eval_expr(self,tree):
        if tree[1][0]== 't_multi':
            val = self.eval_multi(tree[1])
        elif tree[1][0]== 't_div':
            val = self.eval_div(tree[1])
        elif tree[1][0]== 'term':
            val = self.eval_term(tree[1])
        return val

    def eval_multi(self,tree):
        if tree[1][0]== 't_multi':
            val1 = self.eval_multi(tree[1])
        elif tree[1][0]== 't_div':
            val1 = self.eval_div(tree[1])
        elif tree[1][0]== 'term':
            val1 = self.eval_term(tree[1])

        if tree[2][0]== 't_mod':
            val2 = self.eval_mod(tree[2])
        elif tree[2][0]== 'factor1':
            val2 = self.eval_factor1(tree[2])
        if not(isinstance(val1,int) and isinstance(val2,int)):
            sys.exit("Error at line "+str(tree[len(tree)-1])+" : '*' supports only integers")
        return int(val1*val2)


    def eval_div(self,tree):
        if tree[1][0]== 't_multi':
            val1 = self.eval_multi(tree[1])
        elif tree[1][0]== 't_div':
            val1 = self.eval_div(tree[1])
        elif tree[1][0]== 'term':
            val1 = self.eval_term(tree[1])

        if tree[2][0]== 't_mod':
            val2 = self.eval_mod(tree[2])
        elif tree[2][0]== 'factor1':
            val2 = self.eval_factor1(tree[2])
        if not(isinstance(val1,int) and isinstance(val2,int)):
            sys.exit("Error at line "+str(tree[len(tree)-1])+" : '/' supports only integers")
        return int(val1/val2)

    def eval_term(self,tree):
        if tree[1][0]== 't_mod':
            val = self.eval_mod(tree[1])
        elif tree[1][0]== 'factor1':
            val = self.eval_factor1(tree[1])
        return val
    def eval_mod(self,tree):
        if tree[1][0]== 't_mod':
            val1 = self.eval_mod(tree[1])
        elif tree[1][0]== 'factor1':
            val1 = self.eval_factor1(tree[1])

        if tree[2][0]== 't_id':
            val2 = self.eval_id(tree[2])
        elif tree[2][0]== 't_num':
            val2 = self.eval_num(tree[2])
        elif tree[2][0]== 't_string':
            val2 = self.eval_string(tree[2])
        elif tree[2][0] == 't_para':
            val2 = self.eval_para(tree[2])
        elif tree[2][0] == 't_ternary':
            val2 = self.eval_ternary(tree[2])
        elif tree[2][0] == 't_funcall':
            val2 = self.eval_funcall(tree[2],1)
        if not(isinstance(val1,int) and isinstance(val2,int)):
            sys.exit("Error at line "+str(tree[len(tree)-1])+" : '%' supports only integers")
        return int(val1%val2)

    def eval_factor1(self,tree):
        if tree[1][0]== 't_id':
            val = self.eval_id(tree[1])
        elif tree[1][0]== 't_num':
            val = self.eval_num(tree[1])
        elif tree[1][0]== 't_string':
            val = self.eval_string(tree[1])
        elif tree[1][0] == 't_para':
            val = self.eval_para(tree[1])
        elif tree[1][0] == 't_ternary':
            val = self.eval_ternary(tree[1])
        elif tree[1][0] == 't_funcall':
            val = self.eval_funcall(tree[1],1)
        return val
    def eval_id(self,tree):
        return self.lookup(tree[1],tree[len(tree)-1])
    def eval_num(self,tree):
        return tree[1]
    def eval_string(self,tree):
        return tree[1][1:-1]

    def eval_para(self,tree):
        if tree[1][0]== 't_plus':
            val = self.eval_plus(tree[1])
        elif tree[1][0]== 't_minus':
            val = self.eval_minus(tree[1])
        elif tree[1][0]== 'expression':
            val = self.eval_expr(tree[1])
        return val

    def eval_ternary(self,tree):
        if tree[1][0] == 't_or':
            val = self.eval_or(tree[1])
        elif tree[1][0] == 'boolean':
            val = self.eval_boolean(tree[1])
        if isinstance(val,str):
            sys.exit("Error at line "+ str(tree[len(tree)-1]) +":string cannot do bool operations")
        if val:
            if tree[2][0] == 't_or':
                val1 = self.eval_or(tree[2])
            elif tree[2][0] == 'boolean':
                val1 = self.eval_boolean(tree[2])
        else:
            if tree[3][0] == 't_or':
                val1 = self.eval_or(tree[3])
            elif tree[3][0] == 'boolean':
                val1 = self.eval_boolean(tree[3])
        return val1

    def eval_funcall(self,tree,flag):
        global function_hash
        param = []
        FEval = Evaluate()
        if tree[1] in function_hash.keys():
            param = self.eval_param([],tree[2])
            if len(param) != len(function_hash[tree[1]][0]):
                sys.exit("Error at line "+str(tree[len(tree)-1])+": no of parameters should be "+str(len(function_hash[tree[1]][0])))
            else:
                for i in range(len(param)):
                    FEval.variable_env[function_hash[tree[1]][0][i]] = param[i]
                FEval.eval_block(function_hash[tree[1]][1])
        else:
            sys.exit("Error at line "+str(tree[len(tree)-1])+": no function definitions with the name "+tree[1])
        if flag == 1:
            if function_hash[tree[1]][2]!=None and function_hash[tree[1]][2][0] == 't_or':
                val = FEval.eval_or(function_hash[tree[1]][2])
            elif function_hash[tree[1]][2]!=None and function_hash[tree[1]][2][0] == 'boolean':
                val = FEval.eval_boolean(function_hash[tree[1]][2])
            else:
                sys.exit("Error at line "+str(tree[len(tree)-1])+": this function doesn't return anything")
            return val
        else:
            pass

    def eval_param(self,li,tree):
        if tree!='t_empty':
            if tree[1][0]=='t_or':
                li.append(self.eval_or(tree[1]))
            elif tree[1][0]=='boolean':
                li.append(self.eval_boolean(tree[1]))
            if tree[0]=="t_params":
               li =  self.eval_param(li,tree[2])
        else:
            return []
        return li

    def lookup(self,x,lineno):
        if x not in self.variable_env.keys():
            sys.exit("Error at line "+str(lineno)+ ": variable "+x+" doesn't exist")
        else:
            return self.variable_env[x]


def eval_program(tree):
    if tree[1]!='empty':
        eval_funcList(tree[1])

    Eval=Evaluate()
    Eval.eval_block(tree[2])

def eval_funcList(tree):
    if tree[0] == 't_functionlist':
        eval_function(tree[1])
        eval_funcList(tree[2])
    else:
        pass

def eval_function(tree):
    global function_hash
    if tree[1] not in function_hash.keys():
        args = []
        args = eval_arguments([],tree[2])
        if tree[0]=='t_defR':
            function_hash[tree[1]] = [args,tree[3],tree[4]]
        else:
            function_hash[tree[1]] = [args,tree[3],None]
    else:
        sys.exit("Error: more than one function definitions with the name "+tree[1])

def eval_arguments(li,tree):
    if tree!='t_empty':
        if tree[1] not in li:
            li.append(tree[1])
        else:
            sys.exit("Error at line "+str(tree[len(tree)-1])+" : more than one argument with same name")

        if tree[0]=="t_arguments":
           li =  eval_arguments(li,tree[2])
    else:
        return []
    return li

def main(argv):
    if argv[-4:] != ".ace":
        sys.exit("Error :please provide .ace extension file")
    data = ""
    filepath = os.path.abspath(os.path.join(currentDirectory, '..'))+"/data/"+argv
    with open(filepath, 'r') as file:
        data = file.read()
    print(data)
    builder = parse.SyntaxTree()
    builder.build(data)
    t = builder.tree
    print("Output of Program file:")
    eval_program(t)

if __name__ == "__main__":
   main(sys.argv[1])
