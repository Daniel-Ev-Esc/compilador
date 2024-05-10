import ply
import ply.lex as lex

reserved = {
    'program':'PROGRAM',
    'main':'MAIN',
    'end':'END',
    'var':'VAR',
    'int':'INT',
    'float':'FLOAT',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'do':'DO',
    'print':'PRINT',
    'void':'VOID'
}

tokens = [
    'PUNTOCOMA',
    'COMA',
    'DOSPUNTOS',
    'CORCHETEIZQ',
    'CORCHETEDER',
    'IGUAL',
    'PUNTO',
    'PARENDER',
    'PARENIZQ',
    'MENORQUE',
    'MAYORQUE',
    'EXCLAMACION',
    'PLUS',
    'MINUS',
    'MULT',
    'DIV',
    'BRACKETIZQ',
    'BRACKETDER',
    'COMILLAS',
    'ID', 
    'CTE_INT',
    'CTE_FLOAT',
    'CTE_STRING'  ] + list(reserved.values())

t_PUNTOCOMA = r';'
t_COMA = r','
t_DOSPUNTOS= r':'
t_CORCHETEIZQ= r'{'
t_CORCHETEDER= r'}'
t_IGUAL = r'\='
t_PUNTO = r'\.'
t_PARENDER = r'\)'
t_PARENIZQ = r'\('
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_EXCLAMACION = '!'
t_PLUS = r'\+'
t_MINUS = r'- '
t_MULT = r'\*'
t_DIV = r'/'
t_BRACKETIZQ = r'\['
t_BRACKETDER = r'\]'
t_COMILLAS = r'“'
t_ignore  = ' \t'
t_CTE_INT = r'[0-9]+'
t_CTE_FLOAT = r'[0-9]+\.[0-9]+'
t_CTE_STRING = r'\"[a-zA-Z_0-9 ]*\"'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Buscar palabras reservadas
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    raise Exception("Caractér desconocido '%s'" % t.value[0])
    

lexer = lex.lex()