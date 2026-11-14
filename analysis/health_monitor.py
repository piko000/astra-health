def calculate_deviation(
    baseline: float,
    current: float
) -> float:
    if baseline == 0:
        raise ValueError("Baseline darf nicht 0 sein.")

    deviation = ((current - baseline) / baseline) * 100
    return deviation


def classify_health_status(deviation: float) -> str:

    if deviation < 0:
        raise ValueError("Deviation darf nicht negativ sein.")

    if deviation < 10.0:
        return "NORMAL"

    elif deviation < 25.0:
        return "WARNING"

    else:
        return "CRITICAL"

def analyze_heart_rate(
    baseline: float,
    current: float
) -> dict:

    deviation = calculate_deviation(
        baseline,
        current
    )

    # Bestimme den Status mit dem Betrag
    status = classify_health_status(abs(deviation))

    return {
        "baseline": baseline,
        "current": current,
        "deviation": deviation,
        "status": status
    }

print(analyze_heart_rate(80, 60))
