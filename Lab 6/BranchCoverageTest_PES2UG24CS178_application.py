import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


# ---------------- FUEL BILL BRANCH TESTS ----------------

def test_unknown_fuel_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 50, "gold")


def test_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_gold_regular_with_no_extra_litres():
    assert fuel_bill("regular", 15, "gold") == 0


def test_silver_regular_with_no_extra_litres():
    assert fuel_bill("regular", 10, "silver") == 0


def test_gold_regular_with_extra_below_30():
    assert fuel_bill("regular", 20, "gold") == 525


def test_silver_regular_with_extra_above_30():
    assert fuel_bill("regular", 50, "silver") == 3960


def test_gold_regular_with_extra_above_30():
    assert fuel_bill("regular", 60, "gold") == 4275


def test_gold_diesel_no_extra_bonus():
    assert fuel_bill("diesel", 25, "gold") == 450


def test_silver_diesel_with_extra_above_30():
    assert fuel_bill("diesel", 60, "silver") == 3360

# ---------------- PUMP ALLOWED BRANCH TESTS ----------------

def test_fleet_within_200_litres():
    assert pump_allowed(200, 5, True) is True


def test_fleet_above_200_litres():
    assert pump_allowed(201, 5, True) is False


def test_non_fleet_above_60_litres():
    assert pump_allowed(61, 1, False) is False


def test_non_fleet_at_60_litres_one_container():
    assert pump_allowed(60, 1, False) is True


def test_non_fleet_multiple_containers():
    assert pump_allowed(30, 2, False) is False


# ---------------- SESSION STATUS BRANCH TESTS ----------------

def test_card_payment_active():
    assert session_status(60, True, False) == "active"


def test_card_payment_warning():
    assert session_status(45, True, False) == "warning"


def test_card_payment_timed_out():
    assert session_status(44, True, False) == "timed_out"


def test_cash_payment_active():
    assert session_status(30, False, False) == "active"


def test_cash_payment_warning():
    assert session_status(15, False, False) == "warning"


def test_cash_payment_timed_out():
    assert session_status(14, False, False) == "timed_out"


def test_night_session_active():
    assert session_status(60, False, True) == "active"


def test_night_session_warning():
    assert session_status(45, False, True) == "warning"


def test_night_session_timed_out():
    assert session_status(44, False, True) == "timed_out"