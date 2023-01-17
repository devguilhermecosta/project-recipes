def is_positive_number(value: int | float | str) -> bool:
    try:
        number: float = float(value)
    except ValueError:
        return False
    return number > 0
