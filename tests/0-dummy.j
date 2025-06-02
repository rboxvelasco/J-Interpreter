NB. The objective of this test is to check the most basic aspects that any programming language should have.

NB. Variable assignmanet and access.
x =: 0
y =: 1 2 3
z =: y

x
y
z

NB. Parenthesized operations with positives and negatives.
NB. Right associative. Equal priority.
_2+5*6
(_2+5)*6

2+3|7*_6-3^10%5
2+(3|7*_6)-3^10%5

NB. Relational operators
4 + 1 <> 1
4 + 1 <= 3
4 + (1 < 3) + (0 = 0)

NB. Basic operations with lists.
2 * y
y * z

1 2 3 | 2
7 | 1 2 3

NB. Use of identity.
] 1
] 0 1 2

NB. Function declaration, access and invocation.
list =: 0 1 2 3

mod2 =: 2 | ]
mod2
m =: mod2 list
m

eq0 =: 0 = ]
eq0 m

square =: *:
square
square list