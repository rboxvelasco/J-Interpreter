list =: i. 10                  NB. Genera [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
sum =: +/ list                NB. sum total usando fold: 45
conteo =: # list               NB. Número de elementos: 10
media =: sum % conteo          NB. Media: 45 % 10 = 4.5
patron_pares =: 0 = 2 | list   NB. Patrón booleano para pares: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
pares =: patron_pares # list   NB. Selecciona pares: [0, 2, 4, 6, 8]
sum_pares =: +/ pares          NB. sum de pares: 20
patron_impares =: 1 = 2 | list    NB. Patrón booleano para impares: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
impares =: patron_impares # list  NB. Selecciona impares: [1, 3, 5, 7, 9]
sum_impares =: +/ impares         NB. sum de impares: 25
list_reversa =: |. list          NB. list invertida: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
sum_reversa =: +/ list_reversa   NB. sum de la reversa (igual a sum): 45
list_incrementada =: >: list     NB. Incrementa cada elemento: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
sum_incrementada =: +/ list_incrementada  NB. sum incrementada: 55
diferencia =: list -~ 5  NB. 5 - cada elemento: [5, 4, 3, 2, 1, 0, -1, -2, -3, -4]
sum_diferencia =: +/ diferencia  NB. sum de diferencias: 5
NB. incrementar_y_sumr =: +/ @: >:  NB. Función compuesta: incrementa y sum
NB. resultado_compuesto =: incrementar_y_sumr list  NB. Aplica composición: 55

list                  NB. Imprime list
sum                   NB. Imprime sum
media                  NB. Imprime media
sum_pares             NB. Imprime sum de pares
sum_impares           NB. Imprime sum de impares
sum_incrementada      NB. Imprime sum incrementada
sum_diferencia        NB. Imprime sum de diferencias
NB. resultado_compuesto    NB. Imprime resultado de composición