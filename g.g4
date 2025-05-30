grammar g;

root
    : '\n'* stat ('\n'+ stat)* '\n'* EOF
    ;

stat
    : ID '=:' expr      # assignacio
    | ID expr           # cridaFuncio
    | expr              # expressio
    ;

expr
    : atom (op atom)*   # operacio
    ;

atom
    : ID                # variable
    | op                # operador
    | 'i.'              # funcioI
    | '(' expr ')'      # parenExpr
    | list              # llistaNumeros
    ;

list
    : NUM (NUM)*        # llista
    ;

op
    : '+' | '-' | '*' | '%' | '|' | '^' 
    | '<' | '>' | '>=' | '<=' | '=' | '<>'
    | ',' | '{'
    ;

COMMENT : 'NB.' ~[\r\n]* -> skip ;
NUM     : '_'? [0-9]+ ;
ID      : [a-zA-Z_][a-zA-Z_0-9]* ;
WS      : [ \t]+ -> skip ;