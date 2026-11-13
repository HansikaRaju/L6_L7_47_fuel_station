
from hypothesis import given, strategies as st

from fuel_station import (
    parse_purchase,
    volume_average,
    payable_bill
)


# Test 1: Fuzz testing for parse_purchase()
@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):
    result = parse_purchase(s)
    assert result is None or (
        isinstance(result, tuple) and len(result) == 2
    )


@given(
    grade=st.text(
        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ",
        min_size=1
    ).filter(lambda x: bool(x.strip())),
    litres=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_parse_purchase_valid(grade, litres):
    result = parse_purchase(f"{grade}:{litres}")
    assert result == (grade.strip().title(), litres)


# Test 2: Fuzz testing for volume_average()
@given(st.text() | st.none())
def test_volume_average_no_crash(s):
    result = volume_average(s)
    assert result is None or isinstance(result, int)


@given(
    st.lists(
        st.integers(min_value=0, max_value=100000),
        min_size=1,
        max_size=30
    )
)
def test_volume_average_valid(values):
    csv = ",".join(map(str, values))
    assert volume_average(csv) == sum(values) // len(values)


# Test 3: Fuzz testing for payable_bill()
@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    result = payable_bill(s)
    assert result is None or isinstance(result, float)


@given(
    bill=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    ),
    discount=st.floats(
        min_value=0,
        max_value=100000,
        allow_nan=False,
        allow_infinity=False
    )
)
def test_payable_bill_valid(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert result == max(bill * 1.18 - discount, 0)
