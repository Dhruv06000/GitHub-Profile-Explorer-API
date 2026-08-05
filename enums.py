from enum import Enum

class SortOption(str, Enum):
    """Enum for sorting options."""
    NAME = "name"
    STARS = "stars"
    FORKS = "forks"
    UPDATED = "updated"

class OrderOption(str, Enum):
    """Enum for order options."""
    ASC = "asc"
    DESC = "desc"
