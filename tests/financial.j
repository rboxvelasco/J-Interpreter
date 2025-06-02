transacciones =: 1000, _500, 750, _200, 1500, _300, 1200, _800, 400, _100  NB. Lista de transacciones
umbral =: 1000                              NB. Umbral para transacciones grandes
balance =: +/ transacciones                 NB. Balance neto: suma total
positivas =: (0 < transacciones) # transacciones  NB. Filtra transacciones positivas
negativas =: (0 > transacciones) # transacciones   NB. Filtra transacciones negativas
conteo_positivas =: # positivas             NB. Conteo de transacciones positivas
conteo_negativas =: # negativas             NB. Conteo de transacciones negativas
promedio_positivas =: (+/ positivas) % conteo_positivas  NB. Promedio de positivas
promedio_negativas =: (+/ negativas) % conteo_negativas  NB. Promedio de negativas
transacciones_grandes =: (umbral <= transacciones) # transacciones  NB. Transacciones >= umbral
conteo_grandes =: # transacciones_grandes   NB. Conteo de transacciones grandes
inversas =: |. transacciones                NB. Transacciones en orden inverso
diferencias =: transacciones -~ 500         NB. Diferencia de cada transacción respecto a 500
NB. procesar_resumen =: (+/ @: (0 < ]) @:. -.)  NB. Función compuesta: filtra positivas o negativas y suma
NB. suma_positivas =: procesar_resumen transacciones  NB. Suma de positivas
NB. suma_negativas =: procesar_resumen -. transacciones  NB. Suma de negativas (aplica negación unaria)
transacciones        NB. Imprime transacciones
balance              NB. Imprime balance
conteo_positivas     NB. Imprime conteo de positivas
conteo_negativas     NB. Imprime conteo de negativas
promedio_positivas   NB. Imprime promedio de positivas
promedio_negativas   NB. Imprime promedio de negativas
transacciones_grandes NB. Imprime transacciones grandes
conteo_grandes       NB. Imprime conteo de grandes
NB. suma_positivas       NB. Imprime suma de positivas
NB. suma_negativas       NB. Imprime suma de negativas