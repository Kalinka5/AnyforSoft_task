"""
Tests for the commission_engine module.
"""
import pytest
from src.data_loader import Partner
from src.commission_engine import CommissionCalculator

DAYS_IN_MONTH = 30 # For simplicity in tests

@pytest.fixture
def commission_calculator(happy_path_partners):
    """Fixture for a CommissionCalculator instance."""
    return CommissionCalculator(happy_path_partners, DAYS_IN_MONTH)

def test_calculate_commissions_happy_path(commission_calculator):
    """
    Tests the commission calculation for a standard hierarchy.
    """
    commissions = commission_calculator.calculate_commissions()

    # Expected calculations:
    # Partner 1's descendants (2, 3, 4) total revenue: 5000 + 5000 + 2000 = 12000
    # Partner 2's descendants (4) total revenue: 2000
    # Partner 3's descendants: 0
    # Partner 4's descendants: 0
    #
    # Commission for Partner 1: (12000 / 30) * 0.05 = 20.0
    # Commission for Partner 2: (2000 / 30) * 0.05 = 3.33
    # Commission for Partner 3: 0
    # Commission for Partner 4: 0
    expected_commissions = {
        1: 20.0,
        2: 3.33,
        3: 0.0,
        4: 0.0,
    }

    assert commissions.keys() == expected_commissions.keys()
    for pid, expected in expected_commissions.items():
        assert commissions[pid] == pytest.approx(expected, abs=1e-2)

def test_calculate_commissions_leaf_node(commission_calculator):
    """
    Tests that a leaf node (no descendants) gets zero commission.
    """
    commissions = commission_calculator.calculate_commissions()
    assert commissions[4] == 0.0

def test_calculate_commissions_different_month_lengths(happy_path_partners):
    """
    Tests that commission calculations vary correctly with the number of days in a month.
    """
    # Test with 28 days
    calc_28_days = CommissionCalculator(happy_path_partners, 28)
    commissions_28 = calc_28_days.calculate_commissions()
    expected_28 = (12000 / 28) * 0.05
    assert commissions_28[1] == pytest.approx(expected_28, abs=1e-2)

    # Test with 31 days
    calc_31_days = CommissionCalculator(happy_path_partners, 31)
    commissions_31 = calc_31_days.calculate_commissions()
    expected_31 = (12000 / 31) * 0.05
    assert commissions_31[1] == pytest.approx(expected_31, abs=1e-2)
    
def test_deep_hierarchy_commission():
    """
    Tests commission calculation in a deep, single-branch hierarchy.
    """
    partners_data = [
        Partner(id=1, parent_id=None, name="L1", monthly_revenue=1000),
        Partner(id=2, parent_id=1, name="L2", monthly_revenue=1000),
        Partner(id=3, parent_id=2, name="L3", monthly_revenue=1000),
        Partner(id=4, parent_id=3, name="L4", monthly_revenue=1000),
    ]
    calculator = CommissionCalculator(partners_data, DAYS_IN_MONTH)
    commissions = calculator.calculate_commissions()

    # Expected calculations:
    # L1 descendants revenue: 1000 (L2) + 1000 (L3) + 1000 (L4) = 3000
    # L2 descendants revenue: 1000 (L3) + 1000 (L4) = 2000
    # L3 descendants revenue: 1000 (L4) = 1000
    # L4 descendants revenue: 0
    expected = {
        1: (3000 / DAYS_IN_MONTH) * 0.05,
        2: (2000 / DAYS_IN_MONTH) * 0.05,
        3: (1000 / DAYS_IN_MONTH) * 0.05,
        4: 0.0,
    }

    assert commissions.keys() == expected.keys()
    for pid, expected_val in expected.items():
        assert commissions[pid] == pytest.approx(expected_val, abs=1e-2)
