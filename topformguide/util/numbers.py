"""
Number conversion utilities for easier type conversions.
"""

def toInt(value, default=None):
    """
    Converts any value to an integer if possible, and if the conversion fails returns a
    optionally specified default value. makes it easy to convert to int without the need
    to handle ValueErrors.
    :param value: what to convert
    :param default: [integer] What to return if conversion is not possible. Defaults to None.
    :return: [integer] the converted value, or the default value if conversion isn't possible.
    """
    try:
        return int(value)
    except ValueError:
        return default

