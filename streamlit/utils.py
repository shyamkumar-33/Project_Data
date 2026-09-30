# ============================================================
# CART2INSIGHTS - UTILITY FUNCTIONS
# ============================================================


def format_number(value):
    """
    Format a number with comma separators.
    Example: 99441 -> 99,441
    """

    if value is None:
        return "0"

    return f"{int(value):,}"


def format_currency(value):
    """
    Format a number as Indian Rupees.
    Example: 123456.78 -> ₹123,456.78
    """

    if value is None:
        return "₹0.00"

    return f"₹{float(value):,.2f}"


def format_decimal(value):
    """
    Format a decimal value to 2 decimal places.
    """

    if value is None:
        return "0.00"

    return f"{float(value):.2f}"