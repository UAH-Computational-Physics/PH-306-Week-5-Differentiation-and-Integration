import os
from pathlib import Path

import matplotlib
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
    x_, y_, r_ = sp.symbols("x y r", real=True)

    result = calculus.boas_problem_4_1_8(x_, y_, r_)

    x0, r0 = 1.1, 2.5
    y0 = np.sqrt(r0**2 - x0**2)
    value = complex(result.subs({x_: x0, y_: y0, r_: r0}).evalf())
    assert np.isclose(value.real, -2 * x0, rtol=1e-8, atol=1e-8)


def test_boas_problem_4_1_12():
    """z = x**2 + 2*y**2, tan(theta) = y / x; check (dz/dy) holding theta constant."""
    x_, y_, theta_ = sp.symbols("x y theta", real=True)

    result = calculus.boas_problem_4_1_12(x_, y_, theta_)

    theta0, y0 = 0.9, 1.4
    x0 = y0 / np.tan(theta0)
    expected = 2 * x0**2 / y0 + 4 * y0
    value = complex(result.subs({x_: x0, y_: y0, theta_: theta0}).evalf())
    assert np.isclose(value.real, expected, rtol=1e-8, atol=1e-8)


def test_boas_problem_4_1_19():
    """z = x**2 + 2*y**2, x = r*cos(theta), y = r*sin(theta); check (d^2 z)/(dr dy)."""
    x_, y_, r_, theta_ = sp.symbols("x y r theta", real=True)

    result = calculus.boas_problem_4_1_19(x_, y_, r_, theta_)

    x0, y0 = 1.3, 0.7
    r0, theta0 = np.hypot(x0, y0), np.arctan2(y0, x0)
    expected = y0 * (6 * x0**2 + 4 * y0**2) / (x0**2 + y0**2) ** 1.5
    value = complex(result.subs({x_: x0, y_: y0, r_: r0, theta_: theta0}).evalf())
    assert np.isclose(value.real, expected, rtol=1e-6, atol=1e-6)


def test_boas_example_4_9_3_symbolic():
    """Box of volume 8*x*y*z inscribed in an ellipsoid; check the general max-volume formula."""
    x_, y_, z_, a_, b_, c_ = sp.symbols("x y z a b c", positive=True)
    volume = 8 * x_ * y_ * z_
    ellipsoid = x_**2 / a_**2 + y_**2 / b_**2 + z_**2 / c_**2

    result = calculus.boas_example_4_9_3(volume, ellipsoid)

    expected = 8 * a_ * b_ * c_ / (3 * sp.sqrt(3))
    assert sp.simplify(result - expected) == 0


def test_boas_example_4_9_3_numeric():
    """Box of volume 8*x*y*z inscribed in an ellipsoid; check the numeric max volume."""
    x_, y_, z_, a_, b_, c_ = sp.symbols("x y z a b c", positive=True)
    volume = 8 * x_ * y_ * z_
    ellipsoid = x_**2 / a_**2 + y_**2 / b_**2 + z_**2 / c_**2

    a0, b0, c0 = 2.0, 3.0, 4.0
    result = calculus.boas_example_4_9_3(volume, ellipsoid, semi_major_axes=(a0, b0, c0))

    expected = 8 * a0 * b0 * c0 / (3 * np.sqrt(3))
    assert np.isclose(float(result), expected, rtol=1e-6)


def test_boas_problem_4_9_1_symbolic():
    """Rectangle with two isoceles-triangle caps; check the general max-area formula."""
    l_, s_, theta_ = sp.symbols("l s theta", positive=True)
    area = 2 * l_ * s_ * sp.cos(theta_) + s_**2 * sp.sin(2 * theta_)
    perimeter = 2 * l_ + 4 * s_

    result = calculus.boas_problem_4_9_1(area, perimeter)

    extra_symbols = result.free_symbols - {l_, s_, theta_}
    assert len(extra_symbols) == 1
    p_symbol = extra_symbols.pop()

    for p_val in (6.0, 10.0):
        got = complex(result.subs(p_symbol, p_val).evalf())
        expected = np.sqrt(3) / 24 * p_val**2
        assert np.isclose(got.real, expected, rtol=1e-6)


def test_boas_problem_4_9_1_numeric():
    """Rectangle with two isoceles-triangle caps; check the numeric max area."""
    l_, s_, theta_ = sp.symbols("l s theta", positive=True)
    area = 2 * l_ * s_ * sp.cos(theta_) + s_**2 * sp.sin(2 * theta_)
    perimeter = 2 * l_ + 4 * s_

    total_perimeter = 6.0
    result = calculus.boas_problem_4_9_1(area, perimeter, total_perimeter=total_perimeter)

    expected = np.sqrt(3) / 24 * total_perimeter**2
    assert np.isclose(float(result), expected, rtol=1e-6)


# --- Integration --- #
def _planck_spectral_irradiance(wavelength, temperature):
    """Blackbody spectral exitance (Planck's law) in W/m^2/nm for a wavelength Quantity."""
    exponent = (h * c / (wavelength * k_B * temperature)).to_value(u.dimensionless_unscaled)
    prefactor = 2 * np.pi * h * c**2 / wavelength**5
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
