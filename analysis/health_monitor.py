def calculate_deviation(
    baseline: float,
    current: float
) -> float:
    if baseline == 0:
        raise ValueError("Baseline must not be zero.")

    deviation = ((current - baseline) / baseline) * 100
    return deviation


def classify_health_status(deviation: float) -> str:

    if deviation < 0:
        raise ValueError("Deviation must not be negative.")

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

    # Classify the absolute deviation
    status = classify_health_status(abs(deviation))

    return {
        "baseline": baseline,
        "current": current,
        "deviation": deviation,
        "status": status
    }

