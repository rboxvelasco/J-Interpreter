NB. mod2 =: 2 | ]
NB. eq0 =: 0 = ]
NB. parell =: eq0 @: mod2
NB. parell i. 6    NB. resultat: 1 0 1 0 1 0
NB. 
NB. inc =: 1 + ]
NB. test =: +/ @: inc @: i.
NB. test 3    NB. resultat: 6

NB. #/ 1 2 3 4

NB. 2 # 0 1 2 3
NB. 0 1 2 3 # 2

NB. square1 =: +
NB. square1 0 1 2 3   NB. result:  0 1 1 1
NB. square2 =: +:
NB. square2 0 1 2 3   NB. result: 0 2 4 6


sum =: +:
square =: *:
sum square 1 2 3    NB. result: 2 8 18

f =: sum @: square
f 1 2 3             NB. result: 2 8 18

mod2 =: 2 | ]
eq0 =: 0 = ]
parell =: eq0 @: mod2
parell i. 6        NB. result: 1 0 1 0 1 0

sum =: +: @: *:
inc =: 1 + ]
test =: +/ @: inc @: i.
test 3    NB. resultat: 6