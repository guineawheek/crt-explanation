import math


def solve_turret_rotations(encoder1, encoder2, min_turret_rot, max_turret_rot, tolerance):
    ratio1 = 90.0 / 10.0
    ratio2 = 90.0 / 18.0

    #encoder1 = wrap(encoder1)
    #encoder2 = wrap(encoder2)

    best_error = math.inf
    second_error = math.inf
    best_turret_rot = math.nan

    n_min_d = min(ratio1 * min_turret_rot, ratio1 * max_turret_rot) - encoder1
    n_max_d = max(ratio1 * min_turret_rot, ratio1 * max_turret_rot) - encoder1
    min_n = math.floor(n_min_d) - 1
    max_n = math.ceil(n_max_d) + 1

    print(n_min_d, n_max_d, min_n, max_n)

    for n in range(min_n, max_n + 1):
        turret_rot = (encoder1 + n) / ratio1
        if turret_rot < min_turret_rot - 1e-6 or turret_rot > max_turret_rot + 1e-6:
            continue

        predicted2 = wrap(ratio2 * turret_rot)
        error = modular_error(predicted2, encoder2)

        if error < best_error:
            second_error = best_error
            best_error = error
            best_turret_rot = turret_rot
        elif error < second_error:
            second_error = error

    if not math.isfinite(best_turret_rot) or best_error > tolerance:
        return math.nan
    if second_error <= tolerance and abs(second_error - best_error) < 1e-3:
        return math.nan

    return best_turret_rot


def solve_turret_degrees(encoder1, encoder2, min_turret_deg, max_turret_deg, tolerance):
    rotations = solve_turret_rotations(
        encoder1,
        encoder2,
        min_turret_deg / 360.0,
        max_turret_deg / 360.0,
        tolerance,
    )
    return math.nan if math.isnan(rotations) else rotations * 360.0


def wrap(value):
    value %= 1.0
    if value < 0:
        value += 1.0
    return value


def modular_error(a, b):
    diff = abs(a - b)
    return 1.0 - diff if diff > 0.5 else diff
