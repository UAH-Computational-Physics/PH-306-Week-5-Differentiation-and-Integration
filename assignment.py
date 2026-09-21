"""Student assignment implementation file.

Complete the TODOs in this file.
"""

# --- Imports --- #
# Numerical Imports
import numpy as np


# --- Student Assignment --- #
# Problem 1
def problem1_array_operations() -> tuple[np.ndarray, np.ndarray]:
    """Return x and y for Problem 1.

    - x: 100 evenly spaced values from 0 to 2*pi (inclusive)
    - y: sin(x)
    """
    raise NotImplementedError("Implement problem1_array_operations")


# Problem 2
def problem2_numerical_integration() -> tuple[float, float]:
    """Return (result, error) for integral of exp(-x^2) from -inf to +inf."""
    raise NotImplementedError("Implement problem2_numerical_integration")


# --- Public Checks --- #
def problem1_check() -> None:
    """Check Problem 1 implementation."""
    x, y = problem1_array_operations()
    assert isinstance(x, np.ndarray), "x is not a numpy array"
    assert isinstance(y, np.ndarray), "y is not a numpy array"
    assert x.shape == (100,), "x does not have shape (100,)"
    assert y.shape == (100,), "y does not have shape (100,)"
    assert np.allclose(y[0], 0), "y[0] is not close to 0"
    assert np.allclose(y[-1], 0), "y[-1] is not close to 0"

def problem2_check() -> None:
    """Check Problem 2 implementation."""
    result, error = problem2_numerical_integration()
    assert isinstance(result, float), "result is not a float"
    assert isinstance(error, float), "error is not a float"
    assert np.isclose(result, np.sqrt(np.pi)), "result is not close to sqrt(pi)"
    assert error < 1e-6, "error is not less than 1e-6"


# --- Main --- #
if __name__ == "__main__":
    # Run checks for Problem 1
    try:
        problem1_check()
        print("Problem 1 passed all checks.")
    except AssertionError as e:
        print(f"Problem 1 failed: {e}")
        raise
    except NotImplementedError as e:
        print(f"Problem 1 not yet implemented: {e}")
        raise

    # Run checks for Problem 2
    try:
        problem2_check()
        print("Problem 2 passed all checks.")
    except AssertionError as e:
        print(f"Problem 2 failed: {e}")
        raise
    except NotImplementedError as e:
        print(f"Problem 2 not yet implemented: {e}")
        raise
