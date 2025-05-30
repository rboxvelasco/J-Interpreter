grammar g;

root
    : stat+ EOF
    ;

stat
    : ID '=:' expr      # assignacio
    | expr              # expressio
    ;

expr
    : atom (op expr)?  # operacio
    ;

atom
    : NUM              # numero
    | ID               # variable
    | '(' expr ')'     # parenExpr
    
    ;

op
    : '+'              # suma
    | '-'              # resta
    | '*'              # multiplicacio
    | '%'              # divisio
    | '|'              # modul
    | '^'              # potencia
    ;

COMMENT : 'NB.' ~[\r\n]* -> skip ;
NUM      : '_'? [0-9]+ ;

ID       : [a-zA-Z_][a-zA-Z_0-9]* ;
WS       : [ \t\r\n]+ -> skip ;
