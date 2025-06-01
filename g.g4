grammar g;

root
    : '\n'* stat ('\n'+ stat)* '\n'* EOF
    ;

stat
    : ID '=:' expr      # assignation
    | ID '=:' funcDef   # declareFunction
    | ID expr           # functionCall
    | expr              # expressio
    ;

expr
    : unaryOp expr              # unaryOperation
    | atom (binOp atom)*        # operation
    | binOp '/' atom            # fold
    ;

atom
    : ID                # variable
    | 'i.'              # iDotFunction
    | binOp             # operator
    | '(' expr ')'      # parenExpr
    | list              # llistaNumeros
    | ID expr           # functionEval
    | binToUnOp         # derivedVerbAtom
    | binOp '/'         # foldFunction
    | 'i.' expr         # generatorAtom
    ;

list
    : NUM (NUM)*        # lists
    ;

binToUnOp
    : baseBinOp ':'  // Representa funciones como +: o *:
    ;

funcDef
    : NUM binOp ']'     # funcioMonadica
    | binToUnOp         # funcioBinUn
    ;

baseBinOp
    : '+' | '-' | '*' | '%' | '|' | '^' 
    | '>' | '<' | '>=' | '<=' | '=' | '<>'
    | '*.' | '+.'
    | ',' | '{' | '#' | '@:' | 'e.' | '{.' | '}.'
    ;
    
binOp
    : baseBinOp ('~')*
    ;

unaryOp
    : '|'
    | '-.'
    | ']' ('~')*      // Although '~' won't affect the result, it is not incorrect writing it
    | '#' ('~')*      // Being # an ambigous operator, ~ transforms it from unary to binary (refelexivity of the operand)
    | baseBinOp ':'   // Binary to unary transformation
    ;

COMMENT  : 'NB.' ~[\r\n]* -> skip ;
NUM      : '_'? [0-9]+ ;
ID       : [a-zA-Z_][a-zA-Z_0-9]* ;
WS       : [ \t]+ -> skip ;