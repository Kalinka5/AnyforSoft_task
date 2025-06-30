"""
Tests for the data_loader module.
"""
import json
import pytest
from src.data_loader import load_partners, Partner

def test_load_partners_happy_path(partners_file):
    """
    Tests successful loading of a valid partners file.
    """
    partners = load_partners(partners_file)
    assert isinstance(partners, list)
    assert len(partners) == 4
    assert all(isinstance(p, Partner) for p in partners)
    assert partners[0].id == 1
    assert partners[1].parent_id == 1
    assert partners[3].name == "Partner4"
    assert partners[3].monthly_revenue == 2000

def test_load_partners_file_not_found():
    """
    Tests that FileNotFoundError is raised for a non-existent file.
    """
    with pytest.raises(FileNotFoundError):
        load_partners("non_existent_file.json")

def test_load_partners_malformed_json(tmp_path):
    """
    Tests that ValueError is raised for a malformed JSON file.
    """
    malformed_file = tmp_path / "malformed.json"
    with open(malformed_file, 'w') as f:
        f.write('{"id": 1, "parent_id": null, "name": "Partner1", "monthly_revenue": 10000},')
    
    with pytest.raises(ValueError, match="Malformed JSON"):
        load_partners(malformed_file)

def test_load_partners_invalid_data(tmp_path):
    """
    Tests that ValueError is raised for data with missing keys.
    """
    invalid_data = [
        {"id": 1, "parent_id": None, "name": "Partner1"} # Missing monthly_revenue
    ]
    invalid_file = tmp_path / "invalid_data.json"
    with open(invalid_file, 'w') as f:
        json.dump(invalid_data, f)

    with pytest.raises(ValueError, match="Invalid data format"):
        load_partners(invalid_file)

def test_load_partners_not_a_list(tmp_path):
    """
    Tests that ValueError is raised if the JSON root is not a list.
    """
    not_a_list_file = tmp_path / "not_a_list.json"
    with open(not_a_list_file, 'w') as f:
        json.dump({"data": "not a list"}, f)

    with pytest.raises(ValueError, match="Input JSON must be a list"):
        load_partners(not_a_list_file)
