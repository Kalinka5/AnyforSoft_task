"""
Utility functions for the commission engine.
"""
import calendar
from datetime import datetime

def get_days_in_month(year: int, month: int) -> int:
    """
    Gets the number of days in a specific month and year.

    Args:
        year: The year.
        month: The month (1-12).

    Returns:
        The number of days in the given month.
        
    Raises:
        ValueError: If the month is not between 1 and 12.
    """
    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12.")
    return calendar.monthrange(year, month)[1]

def get_current_year_month() -> (int, int):
    """Returns the current year and month."""
    now = datetime.now()
    return now.year, now.month
