"""
Tests for the tree_validator module.
"""
import pytest
from src.data_loader import Partner
from src.tree_validator import validate_hierarchy

@pytest.fixture
def cyclic_partners_data():
    """Fixture for partner data with a cycle."""
    return [
        {"id": 1, "parent_id": 3, "name": "Partner1", "monthly_revenue": 10000},
        {"id": 2, "parent_id": 1, "name": "Partner2", "monthly_revenue": 5000},
        {"id": 3, "parent_id": 2, "name": "Partner3", "monthly_revenue": 5000},
    ]

@pytest.fixture
def missing_parent_partners_data():
    """Fixture for partner data with a missing parent."""
    return [
        {"id": 1, "parent_id": None, "name": "Partner1", "monthly_revenue": 10000},
        {"id": 2, "parent_id": 99, "name": "Partner2", "monthly_revenue": 5000},
    ]
    
@pytest.fixture
def self_referential_partner_data():
    """Fixture for a partner that is its own parent."""
    return [
        {"id": 1, "parent_id": 1, "name": "Partner1", "monthly_revenue": 10000},
    ]

def test_validate_hierarchy_happy_path(happy_path_partners):
    """
    Tests that no exception is raised for a valid hierarchy.
    """
    try:
        validate_hierarchy(happy_path_partners)
    except ValueError:
        pytest.fail("validate_hierarchy() raised ValueError unexpectedly!")

def test_validate_hierarchy_with_cycle(cyclic_partners_data):
    """
    Tests that a ValueError is raised when a cycle is detected.
    """
    partners = [Partner(**p) for p in cyclic_partners_data]
    with pytest.raises(ValueError, match="Cycle detected"):
        validate_hierarchy(partners)

def test_validate_hierarchy_missing_parent(missing_parent_partners_data):
    """
    Tests that a ValueError is raised when a parent is missing.
    """
    partners = [Partner(**p) for p in missing_parent_partners_data]
    with pytest.raises(ValueError, match="missing parent"):
        validate_hierarchy(partners)
        
def test_validate_hierarchy_self_referential_cycle(self_referential_partner_data):
    """
    Tests that a ValueError is raised for a self-referential partner.
    """
    partners = [Partner(**p) for p in self_referential_partner_data]
    with pytest.raises(ValueError, match="Cycle detected"):
        validate_hierarchy(partners)
