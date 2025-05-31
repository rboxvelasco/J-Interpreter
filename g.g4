grammar g;

root
    : '\n'* stat ('\n'+ stat)* '\n'* EOF
    ;

stat
    : ID '=:' expr      # assignacio
    | ID '=:' funcDef   # assignacioFuncio
    | ID expr           # cridaFuncio
    | expr              # expressio
    ;

expr
    : unOp? atom (binOp atom)*   # operacio
    ;

atom
    : ID                # variable
    | binOp             # operador
    | '(' expr ')'      # parenExpr
    | list              # llistaNumeros
    | ID expr           # llamadaFuncio
    ;

list
    : NUM (NUM)*        # llista
    ;

funcDef
    : NUM binOp ']'   # funcioMonadica
    ;

binOp
    : '+' | '-' | '*' | '%' | '|' | '^' 
    | '>' | '<' | '>=' | '<=' | '=' | '<>'
    | ',' | '{' | '#'
    ;

unOp
    : ']' | '#'
    ;

COMMENT  : 'NB.' ~[\r\n]* -> skip ;
NUM      : '_'? [0-9]+ ;
ID       : [a-zA-Z_][a-zA-Z_0-9]* ;
WS       : [ \t]+ -> skip ;