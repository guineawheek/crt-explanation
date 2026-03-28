import math
import matplotlib.pyplot as plt
import test

#ENC1_RATIO = 5
#ENC2_RATIO = 9

# 9, [10] 11, 12
ENC1_RATIO = 90 / 10
# 16, 17, [18], 19, 20
ENC2_RATIO = 90 / 19


def first_sync(a, b):
    i = 1
    while True:
        if (a * i) % b < 0.001:
            return i
        i += 1

for enc1 in [10]: #[9, 10, 11, 12]:
    for enc2 in [16, 17, 18, 19, 20]:
        r1 = 90 / enc1
        r2 = 90 / enc2
        # 9, 5 -> i = 5, lcm = 45

        # 5 rotations of your enc1 == ambiguity
        sync = first_sync(r1, r2)
        print(f"{enc1=}, {enc2=}, {r1=:.03}, {r2=:.03}, {sync=}, rots = {sync / r2}")

#exit(0)


#ENC1_TEETH = 10
#ENC2_TEETH = 18
TURRET_TEETH = 90



def real_mod(a, b):
    return ((a % b) + b) % b

enc1_reads = []
enc2_reads = []
prev_errors = []
rotations = []

import numpy as np
import random

sync = first_sync(ENC1_RATIO, ENC2_RATIO)
rot_range = sync / ENC2_RATIO
print(f"Configured degrees: {rot_range * 360}")

#random.seed(20)
#range(0, 720):
for deg in np.linspace(0, rot_range * 360, 1000):


    enc1_read = real_mod(int((float(deg) *  ENC1_RATIO) / 360.0 * 4096.0), 4096)
    enc2_read = real_mod(int((float(deg) *  ENC2_RATIO) / 360.0 * 4096.0), 4096)

    NOISE = 110 

    enc1_rot = real_mod((float(deg) *  ENC1_RATIO / 360.0 * 4096.0 + random.randint(-1, 1) * NOISE), 4096) / 4096.0
    enc2_rot = real_mod((float(deg) *  ENC2_RATIO / 360.0 * 4096.0 + random.randint(-1, 1) * NOISE), 4096) / 4096.0

    """
    There are five discrete rotation regions with enc1.
    There are nine discrete rotation regions with enc2.

    There are two rotation ranges with the turret itself.

    Test hypothesis 0..1: 
    
    """


    enc1_guesses = []
    enc2_guesses = []

    for rot_region in range(90):
        enc1_guesses.append(real_mod((enc1_rot + rot_region) / ENC1_RATIO, rot_range))
        enc2_guesses.append(real_mod((enc2_rot + rot_region) / ENC2_RATIO, rot_range))

    best_error = math.inf
    prev_error = math.inf
    candidate = 0
    ij = (0, 0)
    for (i, guess2) in enumerate(enc2_guesses):
        for (j, guess1) in enumerate(enc1_guesses):
            if abs(guess2 - guess1) < best_error:
                prev_error = best_error
                if prev_error < 1e-6:
                    print(f"deg: {deg}")
                    print("prev enc1/enc2: ", enc1_guesses[ij[1]], enc2_guesses[ij[0]])
                    print("curr enc1/enc2: ", guess1, guess2)


                best_error = abs(guess2 - guess1)
                candidate = guess1
                ij = (i, j)

    #print("actual:", deg, "sensor:", (enc1_rot, enc2_rot))
    


    turret_rotations = candidate * 360




    enc1_mod = int(round(enc1_read * ENC2_RATIO / 4096.0)) % ENC2_RATIO
    enc2_mod = int(round(enc2_read * ENC1_RATIO / 4096.0)) % ENC1_RATIO

    enc1_positions = [pos for pos in range(90)]
    enc2_positions = list(range(90))


    #turret_full_rotations = real_mod((10 * enc1_mod) + (36 * enc2_mod), 45) / 45.0
    #turret_fractional_rot = enc2_read / 4096.0 / ENC2_RATIO

    #turret_rotations = test.solve_turret_rotations(enc1_read / 4096.0, enc2_read / 4096.0, 0, 2, 1e-3)
    #turretAngle #turret_full_rotations + turret_fractional_rot
    rotations.append(turret_rotations)
    enc1_reads.append(enc1_read)
    enc2_reads.append(enc2_read)
    prev_errors.append(prev_error)

#print(rotations)

#print(prev_errors)


plt.figure()
plt.plot(range(0, len(rotations)), rotations)
#plt.plot(range(0, 1080), enc1_reads)
#plt.plot(range(0, 1080), enc2_reads)
#plt.vlines(360, 0, 5000, color='g')
#plt.vlines(720, 0, 5000, color='g')

plt.show()

"""
enc1: 9 rotations for spur  (10t)
enc2: 5 rotations for spur (18t)

center: 90t gear


"""
#for region1 in range(5 * 2):
#    #print((enc1_rot + region) / ENC1_RATIO)
#    enc2_guess = real_mod(((enc1_rot + region1)) / ENC1_RATIO * ENC2_RATIO, 1.0)
#    error = abs(enc2_guess - enc2_rot)
#    #print(360 * error)
#    if error < best_enc2_error:
#        best_guess1 = region1
#        best_enc2_error = error

#turret_rotations_enc1 = (best_guess1 / 5.0 + enc1_rot) / ENC1_RATIO

#for region2 in range(9 * 2):
#    #print((enc2_rot + region) / ENC2_RATIO)
#    enc1_guess = real_mod((enc2_rot + region2 / 5.0) / ENC2_RATIO * ENC1_RATIO, 1.0)
#    error = abs(enc1_guess - enc1_rot)
#    #print(360 * error)
#    if error < best_enc1_error:
#        best_guess2 = region2
#        best_enc1_error = error
#    
#turret_rotations_enc2 = (best_guess2 / 9.0 + enc2_rot) / ENC2_RATIO


#if best_enc1_error < best_enc2_error:
#    turret_rotations = turret_rotations_enc1
#else:
#    turret_rotations = turret_rotations_enc2



    #actual_rot = deg / 360.0
    #if abs(actual_rot - turret_rotations) > 0.5:
    #    print("encs:" , enc1_rot, enc2_rot)
    #    print("rot_enc1: ", turret_rotations_enc1, turret_rotations_enc1 * 4096, "error", best_enc2_error, "actual", deg / 360.0, "region:", best_guess1 )
    #    print("rot_enc2: ", turret_rotations_enc2, turret_rotations_enc2 * 4096, "error", best_enc1_error, "actual", deg / 360.0, "region:", best_guess2)


    #difference = (enc2_read - enc1_read)
    #if difference > 250.0/360:
    #    difference -= 1.0 
    #if difference < -250.0/360:
    #    difference += 1.0


    #difference *= ENC2_TEETH * ENC1_TEETH / ((ENC1_TEETH - ENC2_TEETH) * TURRET_TEETH)
    #e1_rotations = difference * TURRET_TEETH / ENC1_TEETH

    #e1_rotations_floored = int(e1_rotations)
    #turretAngle = (e1_rotations_floored + enc1_read) * ENC1_TEETH / TURRET_TEETH
    #if (turretAngle - difference < -100/360):
    #    turretAngle += ENC1_TEETH / TURRET_TEETH
    #elif (turretAngle - difference > 100/360):
    #    turretAngle -= ENC1_TEETH / TURRET_TEETH