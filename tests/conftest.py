"""
Shared fixtures for pytest.
"""
import pytest
import json

from src.data_loader import Partner

@pytest.fixture
def sample_partners_data():
    """Fixture for sample partner data."""
    return [
        {"id": 1, "parent_id": None, "name": "Partner1", "monthly_revenue": 10000},
        {"id": 2, "parent_id": 1, "name": "Partner2", "monthly_revenue": 5000},
        {"id": 3, "parent_id": 1, "name": "Partner3", "monthly_revenue": 5000},
        {"id": 4, "parent_id": 2, "name": "Partner4", "monthly_revenue": 2000},
    ]

@pytest.fixture
def partners_file(tmp_path, sample_partners_data):
    """Fixture to create a temporary partners JSON file."""
    file_path = tmp_path / "partners.json"
    with open(file_path, 'w') as f:
        json.dump(sample_partners_data, f)
    return file_path

@pytest.fixture
def happy_path_partners(sample_partners_data):
    """Fixture for a valid list of Partner objects."""
    return [Partner(**p) for p in sample_partners_data] 