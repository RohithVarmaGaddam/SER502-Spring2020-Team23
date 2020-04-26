from parse import SyntaxTree
import sys

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
        val = self.eval_id(tree[1],tree[len(tree)-1])
        if not isinstance(val,int):
            sys.exit("Error at line "+str(tree[len(tree)-1])+": "+ tree[1][1]+" is not integer and cannot perform increment")
        self.variable_env[tree[1][1]] = val+1
    def eval_dec(self,tree):
        global variable_env
        val = self.eval_id(tree[1],tree[len(tree)-1])
        if not isinstance(val,int):
            sys.exit("Error at line "+str(tree[len(tree)-1])+": "+ tree[1][1]+" is not integer and cannot perform decrement")
        self.variable_env[tree[1][1]] = val-1

    # insert expressions here

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
    if tree[0]!='t_empty':
        if tree[1] not in li:
            li.append(tree[1])
        else:
            sys.exit("Error at line "+str(tree[len(tree)-1])+" : more than one argument with same name")

        if tree[0]=="t_arguments":
           li =  eval_arguments(li,tree[2])
    else:
        return []
    return li

data = '''
fun factorial(n){
    var z = n-1
    var ans
    if z==1{
        ans = 1
    }
    else{
        ans = n*factorial(z)
    }
    send ans
}
var x
var y = 4/1
var k = factorial(5)
out(k)
'''
builder = SyntaxTree()
builder.build(data)

#print(builder.tree)
t = builder.tree
eval_program(t)
