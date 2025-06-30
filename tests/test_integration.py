"""
Integration tests for the MLM Commission Engine CLI.
"""
import json
import subprocess
import sys
import pytest

def test_cli_end_to_end(partners_file, tmp_path):
    """
    Tests the full CLI workflow from input file to output file.
    """
    output_file = tmp_path / "commissions.json"
    month = "2023-04"  # April has 30 days
    days_in_month = 30

    command = [
        sys.executable,
        "main.py",
        "--input",
        str(partners_file),
        "--output",
        str(output_file),
        "--month",
        month,
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 0, f"CLI command failed with stderr: {result.stderr}"
    assert output_file.exists()

    with open(output_file, 'r') as f:
        commissions = json.load(f)

    # Expected calculations from test_commission_engine
    expected_commissions = {
        "1": 20.0,
        "2": 3.33,
        "3": 0.0,
        "4": 0.0,
    }
    
    # The JSON keys will be strings
    assert commissions.keys() == expected_commissions.keys()
    for pid, expected in expected_commissions.items():
        assert commissions[pid] == pytest.approx(expected, abs=1e-2)

def test_cli_cycle_error(tmp_path):
    """
    Tests that the CLI gracefully handles and reports a cycle error.
    """
    cyclic_data = [
        {"id": 1, "parent_id": 2, "name": "Partner1", "monthly_revenue": 10000},
        {"id": 2, "parent_id": 1, "name": "Partner2", "monthly_revenue": 5000},
    ]
    input_file = tmp_path / "cyclic.json"
    with open(input_file, 'w') as f:
        json.dump(cyclic_data, f)
        
    output_file = tmp_path / "commissions_fail.json"

    command = [
        sys.executable,
        "main.py",
        "--input",
        str(input_file),
        "--output",
        str(output_file),
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=False)

    assert result.returncode == 1
    assert "Cycle detected" in result.stderr
    assert not output_file.exists()
