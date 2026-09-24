import os
from pathlib import Path
from warnings import catch_warnings, simplefilter

import matplotlib
from yaml import warnings
matplotlib.use("Agg")  # headless backend for CI/CodeGrade

import matplotlib.pyplot as plt
import numpy as np
import pytest
import sympy as sp
from astropy import units as u
from astropy.constants import c, h, k_B
from scipy import integrate
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.metrics import structural_similarity
from skimage.util import img_as_float

import calculus

# Reference plots are rendered with LaTeX text rendering enabled.
plt.rcParams["text.usetex"] = True

# mpmath (a sympy dependency) emits this on some solve()/evalf() calls; not actionable here.
pytestmark = pytest.mark.filterwarnings(
    "ignore:bitcount function is deprecated:DeprecationWarning"
)

UPLOADED_FILES = os.environ.get("UPLOADED_FILES", ".")


# --- Differentiation --- #
def test_magnetic_time_deriv_sinusoidal():
    """magnetic_time_deriv should differentiate a sinusoidal B(t) built with astropy units."""
    omega = (2 * np.pi / 60.0) * (u.rad / u.s)
    amplitude = 20000.0 * u.nT
    time = np.linspace(0.0, 120.0, 2401) * u.s

    magnetic_field = amplitude * np.sin(omega * time)
    expected = (amplitude * omega * np.cos(omega * time)).to(
        u.nT / u.s, equivalencies=u.dimensionless_angles()
    )

    result = calculus.magnetic_time_deriv(magnetic_field, time)

    assert isinstance(result, u.Quantity), "magnetic_time_deriv should return an astropy Quantity."
    assert u.allclose(result, expected, rtol=1e-2, atol=0.1 * u.nT / u.s)


def test_boas_problem_4_1_3():
    """z = ln(sqrt(u**2 + v**2 + w**2)); check (dz/du, dz/dv, dz/dw)."""
    u_, v_, w_ = sp.symbols("u v w", real=True)

    result = calculus.boas_problem_4_1_3(u_, v_, w_)

    assert isinstance(result, tuple) and len(result) == 3
    denom = u_**2 + v_**2 + w_**2
    expected = (u_ / denom, v_ / denom, w_ / denom)
    for got, exp in zip(result, expected):
        assert sp.simplify(got - exp) == 0


def test_boas_problem_4_1_8():
    """z = x**2 + 2*y**2, r**2 = x**2 + y**2; check (dz/dx) holding r constant."""
    x_, r_ = sp.symbols("x r", real=True)

    result = calculus.boas_problem_4_1_8(x_, r_)

    x0, r0 = 1.1, 2.5
    value = complex(result.subs({x_: x0, r_: r0}).evalf())
    assert np.isclose(value.real, -2 * x0, rtol=1e-8, atol=1e-8)


def test_boas_problem_4_1_12():
    """z = x**2 + 2*y**2, tan(theta) = y / x; check (dz/dy) holding theta constant."""
    y_, theta_ = sp.symbols("y theta", real=True)

    result = calculus.boas_problem_4_1_12(y_, theta_)

    theta0, y0 = 0.9, 1.4
    x0 = y0 / np.tan(theta0)
    expected = 2 * x0**2 / y0 + 4 * y0
    value = complex(result.subs({y_: y0, theta_: theta0}).evalf())
    assert np.isclose(value.real, expected, rtol=1e-8, atol=1e-8)


def test_boas_problem_4_1_19():
    """z = x**2 + 2*y**2, x = r*cos(theta), y = r*sin(theta); check (d^2 z)/(dr dy)."""
    y_, r_ = sp.symbols("y r", real=True)

    result = calculus.boas_problem_4_1_19(y_, r_)

    x0, y0 = 1.3, 0.7
    r0, theta0 = np.hypot(x0, y0), np.arctan2(y0, x0)
    expected = 0
    value = complex(result.subs({y_: y0, r_: r0}).evalf())
    assert np.isclose(value.real, expected, rtol=1e-6, atol=1e-6)


def test_boas_example_4_9_3_symbolic():
    """Box of volume 8*x*y*z inscribed in an ellipsoid; check the general max-volume formula."""
    x_, y_, z_, a_, b_, c_ = sp.symbols("x y z a b c", positive=True)

    result = calculus.boas_example_4_9_3(x_, y_, z_, a_, b_, c_)

    expected = 8 * a_ * b_ * c_ / (3 * sp.sqrt(3))
    assert sp.simplify(result - expected) == 0


def test_boas_example_4_9_3_numeric():
    """Box of volume 8*x*y*z inscribed in an ellipsoid; check the numeric max volume."""
    x_, y_, z_, a_, b_, c_ = sp.symbols("x y z a b c", positive=True)

    a0, b0, c0 = 2.0, 3.0, 4.0
    result = calculus.boas_example_4_9_3(x_, y_, z_, a_, b_, c_, semi_major_axes=(a0, b0, c0))

    expected = 8 * a0 * b0 * c0 / (3 * np.sqrt(3))
    assert np.isclose(float(result), expected, rtol=1e-6)


def test_boas_problem_4_9_1_symbolic():
    """Rectangle with two isoceles-triangle caps; check the general max-area condition."""
    l_, s_, theta_ = sp.symbols("l s theta", positive=True)

    result = calculus.boas_problem_4_9_1(l_, s_, theta_)

    assert isinstance(result, tuple) and len(result) == 3
    l_sol, s_sol, theta_sol = result
    assert sp.simplify(l_sol - s_sol) == 0
    assert sp.simplify(theta_sol - sp.pi / 6) == 0


def test_boas_problem_4_9_1_numeric():
    """Rectangle with two isoceles-triangle caps; check the numeric max area."""
    l_, s_, theta_ = sp.symbols("l s theta", positive=True)

    for total_perimeter in (6.0, 10.0):
        result = calculus.boas_problem_4_9_1(l_, s_, theta_, total_perimeter=total_perimeter)

        expected = np.sqrt(3) / 24 * total_perimeter**2
        assert np.isclose(float(result), expected, rtol=1e-6)


# --- Integration --- #
def test_boas_problem_5_2_1():
    """Double integral of 3x over 0<=x<=1, 2<=y<=4; expected value is 3."""
    # scipy dblquad calls func(y, x), so x is the second positional argument.
    result = calculus.boas_problem_5_2_1(lambda y, x: 3 * x)

    assert np.isclose(result[0], 3, rtol=1e-6)


def test_boas_problem_5_2_6():
    """Double integral of x over 1<=y<=2, sqrt(y)<=x<=y**2; expected value is 2.35."""
    result = calculus.boas_problem_5_2_6(lambda x, y: x)

    assert np.isclose(result[0], 2.35, rtol=1e-3)


def test_boas_problem_5_2_10():
    """Sum of two double integrals of y; expected value is 5*pi."""
    # scipy dblquad calls func(y, x), so y is the first positional argument.
    result = calculus.boas_problem_5_2_10(lambda y, x: y)

    assert np.isclose(result, 5 * np.pi, rtol=1e-6)


def test_boas_problem_5_3_18():
    """Integral from 0 to 2; expected value is 3*sqrt(2)/2 + ln(1 + sqrt(2))/2."""
    result = calculus.boas_problem_5_3_18((0, 2))

    expected = 3 * np.sqrt(2) / 2 + np.log(1 + np.sqrt(2)) / 2
    assert np.isclose(result[0], expected, rtol=1e-6)


def _planck_spectral_irradiance(wavelength, temperature):
    """Blackbody spectral exitance (Planck's law) in W/m^2/nm for a wavelength Quantity."""
    exponent = (h * c / (wavelength * k_B * temperature)).to_value(u.dimensionless_unscaled)
    prefactor = 2 * np.pi * h * c**2 / wavelength**5
    with catch_warnings():
        simplefilter("ignore")
        return (prefactor / np.expm1(exponent)).to(u.W / (u.m**2 * u.nm))


def test_total_solar_irradiance_blackbody():
    """total_solar_irradiance should integrate a blackbody spectrum from 0.5 nm to 200000 nm."""
    temperature = 5778.0 * u.K
    wavelength = np.geomspace(0.5, 200000.0, 5000) * u.nm
    spectral_irradiance = _planck_spectral_irradiance(wavelength, temperature)

    reference, _ = integrate.quad(
        lambda w: _planck_spectral_irradiance(w * u.nm, temperature).to_value(u.W / (u.m**2 * u.nm)),
        wavelength.min().value,
        wavelength.max().value,
        limit=200
    )
    reference <<= u.W / u.m**2

    total = calculus.total_solar_irradiance(wavelength, spectral_irradiance)

    assert isinstance(total, u.Quantity), "total_solar_irradiance should return an astropy Quantity."
    assert u.allclose(total, reference, rtol=5e-2)


# --- Plot Checks --- #
def _load_grayscale(path):
    image = imread(path)
    if image.ndim == 3:
        image = rgb2gray(image[..., :3])
    return img_as_float(image)


def _assert_matches_reference(fig, reference_name, tmp_path, min_similarity=0.8):
    if not UPLOADED_FILES:
        pytest.skip("UPLOADED_FILES is not set; reference plot is unavailable outside CodeGrade.")

    reference_path = Path(UPLOADED_FILES) / reference_name
    if not reference_path.exists():
        pytest.skip(f"Reference plot {reference_path} was not found.")

    candidate_path = tmp_path / reference_name
    fig.savefig(candidate_path)

    candidate = _load_grayscale(candidate_path)
    reference = _load_grayscale(reference_path)

    assert candidate.shape == reference.shape, (
        f"{reference_name} dimensions do not match the reference; "
        "use the matplotlib default figure size."
    )

    similarity = structural_similarity(candidate, reference, data_range=1.0)
    assert similarity >= min_similarity, (
        f"{reference_name} similarity {similarity:.3f} is below the {min_similarity} threshold."
    )


def test_magnetic_plot_matches_reference(tmp_path):
    plt.close("all")
    calculus.magnetic_plot("BOU20150317.csv")
    _assert_matches_reference(plt.gcf(), "solar_event.png", tmp_path)


def test_irradiance_plot_matches_reference(tmp_path):
    plt.close("all")
    calculus.irradiance_plot("nnl_ssi_P1Y.csv")
    _assert_matches_reference(plt.gcf(), "solar_spectrum.png", tmp_path)
