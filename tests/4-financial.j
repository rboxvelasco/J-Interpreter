NB. This test summarizes transactions by computing net balance, positive/negative stats, and large-transaction filters.

txs =: 1000, _500, 750, _200, 1500, _300, 1200, _800, 400, _100   NB. List of transactions

thresh     =: 1000                      NB. Threshold for large transactions
bal        =: +/ txs                    NB. Net balance: total sum

pos        =: (0 < txs) # txs           NB. Filter positive transactions
neg        =: (0 > txs) # txs           NB. Filter negative transactions

n_pos      =: # pos                     NB. Count of positive transactions
n_neg      =: # neg                     NB. Count of negative transactions

avg_pos    =: (+/ pos) % n_pos          NB. Average of positive transactions
avg_neg    =: (+/ neg) % n_neg          NB. Average of negative transactions

large      =: (thresh <= txs) # txs     NB. Transactions ≥ threshold
n_large    =: # large                   NB. Count of large transactions

rev        =: |. txs                    NB. Transactions in reverse order
diff       =: txs -~ 500                NB. Difference from 500 for each transaction

sum_pos    =: +/ pos                    NB. Sum of positives
sum_neg    =: +/ neg                    NB. Sum of negatives


txs         NB. Print transactions
bal         NB. Print net balance
n_pos       NB. Print count of positives
n_neg       NB. Print count of negatives
avg_pos     NB. Print average of positives
avg_neg     NB. Print average of negatives
large       NB. Print large transactions
n_large     NB. Print count of large transactions
sum_pos     NB. Print sum of positives
sum_neg     NB. Print sum of negatives
