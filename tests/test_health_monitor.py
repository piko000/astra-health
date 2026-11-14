import pytest
from analysis.health_monitor import (
    calculate_deviation,
    classify_health_status
    )

def test_positive_deviation():
    result = calculate_deviation(60, 72)
    assert result == pytest.approx(20.0)

def test_negative_deviation():
    result = calculate_deviation(80, 72)
    assert result == pytest.approx(-10.0)


def test_zero_baseline():
    with pytest.raises(ValueError):
        calculate_deviation(0, 80)

def test_no_deviation():
    result = calculate_deviation(100,100)
    assert result == pytest.approx(0.0)

def test_normal_status():
    assert classify_health_status(5.0) == "NORMAL"

def test_warning_status():
    assert classify_health_status(15.0) == "WARNING"

def test_critical_status():
    assert classify_health_status(30.0) == "CRITICAL"

def test_normal_status1():
    assert classify_health_status(9.9) == "NORMAL"

def test_warning_status1():
    assert classify_health_status(10.0) == "WARNING"

def test_warning_status2():
    assert classify_health_status(24.99) == "WARNING"

def test_critical_status1():
    assert classify_health_status(25.0) == "CRITICAL"

def test_value_error_status():
    with pytest.raises(ValueError, match="Deviation darf nicht negativ sein."):
        classify_health_status(-5.0)