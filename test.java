double solveTurretRotations(double encoder1, double encoder2, double minTurretRot, double maxTurretRot, double tolerance) {
    double ratio1 = 90.0 / 10.0;
    double ratio2 = 90.0 / 18.0;

    encoder1 = wrap(encoder1);
    encoder2 = wrap(encoder2);

    double bestError = Double.MAX_VALUE;
    double secondError = Double.MAX_VALUE;
    double bestTurretRot = Double.NaN;

    double nMinD = Math.min(ratio1 * minTurretRot, ratio1 * maxTurretRot) - encoder1;
    double nMaxD = Math.max(ratio1 * minTurretRot, ratio1 * maxTurretRot) - encoder1;
    int minN = (int) Math.floor(nMinD) - 1;
    int maxN = (int) Math.ceil(nMaxD) + 1;

    for (int n = minN; n <= maxN; n++) {
        double turretRot = (encoder1 + n) / ratio1;
        if (turretRot < minTurretRot - 1e-6 || turretRot > maxTurretRot + 1e-6) continue;

        double predicted2 = wrap(ratio2 * turretRot);
        double error = modularError(predicted2, encoder2);

        if (error < bestError) {
            secondError = bestError;
            bestError = error;
            bestTurretRot = turretRot;
        } else if (error < secondError) {
            secondError = error;
        }
    }

    if (!Double.isFinite(bestTurretRot) || bestError > tolerance) return Double.NaN;
    if (secondError <= tolerance && Math.abs(secondError - bestError) < 1e-3) return Double.NaN;

    return bestTurretRot;
}

double solveTurretDegrees(double encoder1, double encoder2, double minTurretDeg, double maxTurretDeg, double tolerance) {
    double rotations = solveTurretRotations(
        encoder1,
        encoder2,
        minTurretDeg / 360.0,
        maxTurretDeg / 360.0,
        tolerance
    );
    return Double.isNaN(rotations) ? Double.NaN : rotations * 360.0;
}

double wrap(double value) {
    value %= 1.0;
    if (value < 0) value += 1.0;
    return value;
}

double modularError(double a, double b) {
    double diff = Math.abs(a - b);
    return diff > 0.5 ? 1.0 - diff : diff;
}