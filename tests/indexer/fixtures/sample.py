"""Sample Python file for testing the parser."""


def simple_function():
    """A simple function with no parameters."""
    pass


def function_with_params(name: str, count: int = 10) -> str:
    """Function with typed parameters and return type.

    Args:
        name: The name to process
        count: Number of repetitions

    Returns:
        Processed string
    """
    return name * count


async def async_function(data: list) -> dict:
    """An async function for testing."""
    return {"data": data}


class SimpleClass:
    """A simple class for testing."""

    def __init__(self, value: int):
        """Initialize with a value."""
        self.value = value

    def get_value(self) -> int:
        """Get the stored value."""
        return self.value


class InheritedClass(SimpleClass):
    """A class that inherits from SimpleClass."""

    def __init__(self, value: int, name: str):
        """Initialize with value and name."""
        super().__init__(value)
        self.name = name

    def get_name(self) -> str:
        """Get the name."""
        return self.name
