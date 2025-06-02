NB. The objective of this test is to check some non-mandatory features of my G interpreter.

NB. Boolean operators: AND, OR, NOT.
-. 0 1 0
-. ((1 *. 0) +. (0 +. 0))

NB. Membership.
1 3 5 e. i.5

NB. Take and Drop.
3 }. 1 2 3 4 5
3 {. 1 2 3 4 5
7 }. 1 2 3 4 5        NB. Empty return
7 {. 1 2 3 4 5        NB. Completes with 0's

1 2 + 3 }. 1 2 3 4 5

NB. Increment and Decrement.
>: 10 20 30
<: (i. 5) + 2

NB. Absolute Value.
1 1 1 + (| _1 _2 _3)

NB. Reverse.
|. 3 2 1 0

NB. Generator i:
i: 3

NB. We can see how things that we had to craft ourselves, now
NB. can be done with specific operators.

inc =: 1 + ]
list =: 0 1 2 4 8

*. / ((|. 1 2 3) = (, ~ / 1 2 3))  NB. Reverse equivalency
*. / ((inc list) = (>: list))      NB. Increment equivalency