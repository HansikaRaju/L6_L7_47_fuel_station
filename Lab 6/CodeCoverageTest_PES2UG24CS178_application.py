import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


# ---------------- FUEL BILL TESTS ----------------

def test_invalid_fuel_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 50, "silver")


def test_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -5, "silver")


def test_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


def test_regular_gold_with_discount():
    assert fuel_bill("regular", 50, "gold") == 3325


def test_regular_silver_with_discount():
    assert fuel_bill("regular", 45, "silver") == 3465


def test_diesel_silver_with_discount():
    assert fuel_bill("diesel", 60, "silver") == 3360


def test_diesel_gold_with_discount():
    assert fuel_bill("diesel", 60, "gold") == 3200


# ---------------- PUMP ALLOWED TESTS ----------------

def test_fleet_within_limit():
    assert pump_allowed(200, 5, True) is True


def test_fleet_exceeds_limit():
    assert pump_allowed(201, 5, True) is False


def test_non_fleet_allowed():
    assert pump_allowed(30, 1, False) is True


def test_non_fleet_exceeds_litre_limit():
    assert pump_allowed(61, 1, False) is False


def test_multiple_containers_not_allowed():
    assert pump_allowed(30, 2, False) is False


# ---------------- SESSION STATUS TESTS ----------------

def test_card_payment_night_active():
    assert session_status(90, True, True) == "active"


def test_cash_payment_warning():
    assert session_status(20, False, False) == "warning"


def test_cash_payment_timed_out():
    assert session_status(14, False, False) == "timed_out"