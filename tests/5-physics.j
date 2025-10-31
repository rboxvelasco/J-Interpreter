NB. This test calculates average acceleration, projects future velocity, and estimates displacement from velocity data after t time.

vels =: 0 2 4 6 8 10       NB. Velocities recorded every 1 second
dt   =: 1                  NB. Time interval between velocity measurements (1s)
t    =: 3                  NB. Time elapsed since the beginning

vels_init =: 1 }. vels     NB. All elements except the first: [2 4 6 8 10]

vels_rev =: |. vels              NB. Reverse the velocity list: [10 8 6 4 2 0]
vels_rev_drop =: 1 }. vels_rev   NB. Drop the first element of reversed list: [8 6 4 2 0]
vels_first =: |. vels_rev_drop   NB. Reverse back to get all except last original: [0 2 4 6 8]

diffs =: vels_init - vels_first  NB. Differences between consecutive velocities: [2 2 2 2 2]

acc =: (+/ diffs) % (# diffs)    NB. Average acceleration (sum of differences / count)

last_vel =: 0 { vels_rev         NB. Last velocity recorded (first element of reversed list): 10

proj_vf =: last_vel + acc * t    NB. Projected velocity after 3 seconds using average acceleration

avg_pairs =: (vels_first + vels_init) % 2  NB. Average velocity between pairs for trapezoidal approximation
disp =: +/ (avg_pairs * dt)                NB. Estimated displacement (area under velocity-time curve)

result =: acc, proj_vf, disp               NB. Result vector: [acceleration, projected velocity, displacement]
result                                     NB. Output the result
