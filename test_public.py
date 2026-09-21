import numpy as np

import assignment


def test_problem1_shapes_and_values():
    x, y = assignment.problem1_array_operations()

    assert isinstance(x, np.ndarray), "x must be a NumPy array"
    assert isinstance(y, np.ndarray), "y must be a NumPy array"
    assert len(x) == 100, "x must contain 100 elements"
    assert np.isclose(x[0], 0.0), "x must start at 0"
    assert np.isclose(x[-1], 2 * np.pi), "x must end at 2π"
    assert np.allclose(y[0], 0), "y[0] is not close to 0"
    assert np.allclose(y[-1], 0), "y[-1] is not close to 0"


def test_problem2_value_and_error():
    result, error = assignment.problem2_numerical_integration()

    assert isinstance(result, float), "result must be a float"
    assert isinstance(error, float), "error must be a float"
    assert np.isclose(result, np.sqrt(np.pi), rtol=1e-6), (
        f"result={result} is not close to sqrt(π)={np.sqrt(np.pi)}"
    )
