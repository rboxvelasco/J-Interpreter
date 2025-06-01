grammar g;

root
    : ENDL* stat (ENDL+ stat)* ENDL* EOF
    ;

stat
    : ID '=:' expr      # assignation
    | ID '=:' funcDef   # declareFunction
    | ID expr           # functionCall
    | expr              # expressio
    ;

expr
    : unaryOp expr              # unaryOperation
    | atom (binOp atom)*        # binaryOperation
    | binOp '/' atom            # fold
    ;

atom
    : ID                # variable
    | 'i.'              # iDotFunction
    | 'i:'              # iColonFunction
    | binOp             # operator
    | '(' expr ')'      # parenExpr
    | NUM (NUM)*        # list
    | ID expr           # functionEval
    | binToUnOp         # derivedVerbAtom
    | binOp '/'         # foldFunction
    | ('i.' | 'i:') expr  # generator
    ;

binToUnOp
    : baseBinOp ':'
    ;

funcDef
    : NUM binOp ']'     # monadicFunction
    | binToUnOp         # binUnFunction
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
    : '-.' | '|.' | '|'
    | '>:' | '<:'
    | ']' ('~')*      // Although '~' won't affect the result, it is not incorrect writing it
    | '#' ('~')*      // Being # an ambigous operator, ~ transforms it from unary to binary (refelexivity of the operand)
    | binToUnOp       // Binary to unary transformation
    ;

COMMENT  : 'NB.' ~[\r\n]* -> skip ;
ENDL     : [\r\n] ;
NUM      : '_'? [0-9]+ ;
ID       : [a-zA-Z_][a-zA-Z_0-9]* ;
WS       : [ \t]+ -> skip ;