NB. This test computes summary measures on a number list: total, average, even/odd filtering, reverse, increment, and related operations.

lst =: i. 10                  NB. Generate list [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
s =: +/ lst                   NB. Total sum using fold: 45
n =: # lst                    NB. Number of elements: 10
avg =: s % n                  NB. Average: 45 % 10 = 4.5
even_mask =: 0 = 2 | lst      NB. Boolean mask for even numbers: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
evens =: even_mask # lst      NB. Select evens: [0, 2, 4, 6, 8]
s_evens =: +/ evens           NB. Sum of evens: 20
odd_mask =: 1 = 2 | lst       NB. Boolean mask for odd numbers: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
odds =: odd_mask # lst        NB. Select odds: [1, 3, 5, 7, 9]
s_odds =: +/ odds             NB. Sum of odds: 25
rev =: |. lst                 NB. Reversed list: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
s_rev =: +/ rev               NB. Sum of reversed list (same as s): 45
inc =: >: lst                 NB. Increment each element: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
s_inc =: +/ inc               NB. Sum of incremented list: 55
diff =: lst -~ 5              NB. 5 minus each element: [5, 4, 3, 2, 1, 0, -1, -2, -3, -4]
s_diff =: +/ diff             NB. Sum of differences: 5
NB. inc_sum =: +/ @: >:       NB. Composed function: increment then sum
NB. res_comp =: inc_sum lst   NB. Apply composed function: 55

lst           NB. Print list
s             NB. Print total sum
avg           NB. Print average
s_evens       NB. Print sum of evens
s_odds        NB. Print sum of odds
s_inc         NB. Print sum of incremented list
s_diff        NB. Print sum of differences
NB. res_comp  NB. Print composed result
