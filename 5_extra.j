+ /\ 1 2 3 4 5
mod2 =: 2 | ]
x =: mod2 i. 10
x
+ /\ x
* /\ 1 + i. 10

NB. funcion que devuelve un vector de longitud n de doses
times2 =: 2 + 0 * i.
* /\ 1 , times2 4

NB. definimos una funcion que devuelve las n potencias de 2
pows2 =: * /\ @: 1 , 1 }. times2
pows2 10
pows2 15
|. pows2 10
4 {. pows2 10
4 }. pows2 10
(times2 5) ^ i. 5   NB. otra forma de hacer potencias de 2
(pows2 5) = (times2 5) ^ i. 5

NB. definimos una funcion que haga un popback
popback =: |. @: (1 }. |.)
popback i. 10
popback |. i. 10

NB. tests simples para take, drop, permute, sort y grade down
5 {. i. 10
5 }. i. 10
? 10
? 10
? 5
? 1 2 3 4
/: ? 10
\: ? 10

NB. ahora permutaremos la variable x dos veces
x =: 10 20 30 40 50
(? #x) { x
(? #x) { x

NB. otra prueba
mask =: 5 < ? 10
mask NB. imprimimos la mascara: 0 1 0 1 1 0 0 1 0 0
values =: i. 10
mask # values
