import ply.lex as lex

# List of token names.   This is always required

reserved = {
    'if':'IF',
    'while':'WHILE',
    'for':'FOR',
    'in':'IN',
    'range':'RANGE',
    'var':'VARIABLE',
    'elif':'ELSEIF',
    'else':'ELSE',
    'out':'PRINT',
    'fun':'FUNCTION',
    'send':'RETURN',
    'true':'TRUE',
    'false':'FALSE'
}
tokens = [
    'NUMBER',
    'STRING',
    'ID',
    'INCRMNT',
    'DECRMNT',
    'BOOLEQL',
    'GTEQL',
    'LTEQL',
    'NOTEQL',
    'OR',
    'AND',
    'NOT',
    'IF',
    'WHILE',
    'FOR',
    'IN',
    'RANGE',
    'VARIABLE',
    'ELSEIF',
    'ELSE',
    'PRINT',
    'FUNCTION',
    'RETURN',
    'TRUE',
    'FALSE'

]

t_INCRMNT = r'\+\+'
t_DECRMNT = r'--'
t_BOOLEQL = r'=='
t_GTEQL = r'>='
t_LTEQL = r'<='
t_OR = r'\|\|'
t_AND = r'&&'
t_NOTEQL = r'!='


# A regular expression rule with some action code
def t_NUMBER(t):
    r'[-]?\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'"(.*?)"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


#literals
literals = ['+','-','*','/','(',')','{','}','>','<','=','!',',',';',':','?','%']


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t ;'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

 # Test it output
def test(data,lexer):
    tokens = []
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
          break
        tokens.append(tok.value)
        print(tok)
    return tokens

