# PH 306 Week 5: Differentiation and Integration

## Homework

### General

1. Complete the following exercises from Boas by finding the derivative of the given function with `sympy` (*e.g.*, `sympy.diff`) rather than differentiating by hand:
    - Problem 4.1.3 with `boas_problem_4_1_3`.
    - Problem 4.1.8 with `boas_problem_4_1_8`.
    - Problem 4.1.12 with `boas_problem_4_1_12`.
    - Problem 4.1.19 with `boas_problem_4_1_19`.
    - Example 4.9.3 with `boas_example_4_9_3(x, y, z, a, b, c, semi_major_axes=None)` using Lagrange Multipliers.
        - `x`, `y`, `z`, `a`, `b`, `c` should be `sympy` symbols.
        - If `semi_major_axes` is `None`, return the general symbolic result in terms of $a$, $b$, $c$.
        - If `semi_major_axes` is a tuple/array of numeric values $(a, b, c)$, substitute them into the symbolic result and return the numeric maximum volume as a scalar.
        - I recommend using [`sympy`](https://docs.sympy.org/latest/index.html) to solve this constrained optimization problem symbolically (e.g., via Lagrange multipliers, `sympy.solve`, or `sympy.calculus.util`), then substitute numeric semi-axis values with `.subs()` and `.evalf()` when they are provided.
    - Problem 4.9.1: find the maximum area of a rectangle capped with isoceles triangles with `boas_problem_4_9_1(l, s, theta, total_perimeter=None)` using Lagrange multipliers. Note that `l`, `s`, `theta` should be `sympy` symbols for the rectangle length, triangle-side length, and triangle half-angle.
        - If `total_perimeter` is `None`, return the general symbolic solution `(l, s, theta)` at the optimum.
        - If `total_perimeter` is a numeric value, substitute the solution into the area expression and return the numeric maximum area as a scalar.
1. Complete the following exercises from Boas by evaluating the given double integral with `scipy.integrate.dblquad` for an arbitrary `integrand` (a callable matching `dblquad`'s expected argument order):
    - Problem 5.2.1 with `boas_problem_5_2_1`.
    - Problem 5.2.6 with `boas_problem_5_2_6`.
    - Problem 5.2.10 with `boas_problem_5_2_10`.
1. Complete the following exercise from Boas:
    - Problem 5.3.18: evaluate the definite integral for arbitrary `limits` with `boas_problem_5_3_18(limits)`.

### Physical: Electric Curl from a Magnetic Disturbance

Get electric curl from the [March 17, 2015 Magnetic Disturbance](https://www.usgs.gov/programs/geomagnetism/science/march-17-2015-magnetic-disturbance). Recall that $$\vec{\nabla}\times\vec{E} = -\frac{\partial\vec{B}}{\partial t}.$$ Therefore to get a component of the curl of $\vec{E}$ we have to take the time derivative of $\vec{B}$.

Dr. Waldron has already downloaded the data from [Intermagnet](https://imag-data.bgs.ac.uk/GIN_V1/GINForms2?observatoryIagaCode=BOU&publicationState=Best+available&dataStartDate=2015-03-17&dataDuration=1&samplesPerDay=minute&submitValue=View+%2F+Download&request=DataView) from the station at Boulder, CO. The JSON data has already been converted to CSV which can be read with [`pd.read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

- The first column is the date and time of the measurement. Use [`pd.to_numeric`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_numeric.html) to convert the imported `datetime` object to microseconds after the [Unix Epoch](https://en.wikipedia.org/wiki/Unix_time).
- The second column is the *north/south* component of the magnetic field in $\mathrm{nT}$.
- Complete the function `magnetic_time_deriv`.
- Complete the function `magnetic_plot` which plots $\vec{B}$ and $$-\frac{\partial\vec{B}}{\partial t}$$ as a function of time (see Canvas for reference plot).

### Physical: Total Solar Irradiance

[NNL/SSI](https://lasp.colorado.edu/lisird/) the 2025 year average spectral irradiance data is provided in `nnl_ssi_P1Y.csv`, with columns for time (days since 1610-01-01), wavelength ($\mathrm{nm}$), and spectral irradiance ($\mathrm{W/m^2/nm}$).

- Complete `total_solar_irradiance(wavelength, spectral_irradiance)`, which integrates the spectral irradiance over wavelength (*e.g.*, with `scipy.integrate.trapezoid` or `scipy.integrate.simpson`) to return the total solar irradiance in $\mathrm{W/m^2}$.
- Complete `irradiance_plot(csv_name)`, which reads the spectral irradiance data from the given CSV file, plots the spectrum, and displays the total irradiance computed with `total_solar_irradiance` (see Canvas for reference plot).

## Running checks

From the repository root, run:

```bash
python -m pytest test_public.py test_public_docs.py
python -m mypy --config-file mypy.ini --strict calculus.py
```

CodeGrade runs comparable checks after submission.
