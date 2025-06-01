NB. Assignacions i consultes a variables.
x =: 0
y =: 1 2 3
z =: y

x
y
z

NB. Operacions parentitzades amb positius i negatius. Precedència per la dreta.
_2+5*6
(_2+5)*6

2+3|7*_6-3^10%5
2+(3|7*_6)-3^10%5

NB. Operacions booleanes
4 + 1 <> 1
4 + 1 <= 3
4 + (1 < 3) + (0 = 0)

NB. Operacions amb llistes
2 * y
y * z

1 2 3 | 2
7 | 1 2 3

NB. Ús de la identitat. Declaració, consulta i crida de funcions.
] 1
] 0 1 2

list =: 0 1 2 3

mod2 =: 2 | ]
mod2
m =: mod2 list
m

eq0 =: 0 = ]
eq0 m