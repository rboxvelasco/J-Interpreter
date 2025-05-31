mod2 =: 2 | ]
eq0 =: 0 = ]
parell =: eq0 @: mod2
parell i. 6    NB. resultat: 1 0 1 0 1 0

inc =: 1 + ]
test =: +/ @: inc @: i.
test 3    NB. resultat: 6