# PH306 Assignment Template (Notebook + Script Grading)

This template is designed to create specific assignment templates for PH 306 using [CodeGrade](https://www.codegrade.com/).

- The Python files `assignment.ipynb` & `assignment.py` serve as example CodeGrade assignments.
- To create a new assignment, create a new repository based on this template then [set up that new repository as a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository).

## Files

- `assignment.ipynb`: example notebook assignment
- `assignment.py`: example script assignment
- `tests/test_public.py`: visible tests used by CodeGrade autograder

## Student workflow

1. Open the assignment script or notebook.
1. Commit and push.
1. Review autograding results in CodeGrade.

## Devcontainer environment

The provided `.devcontainer/devcontainer.json` and `.devcontainer/Dockerfile` uses a Micromamba image and creates a new environment with `mamba` from `environment.yml` (using `conda-forge` and `astropy`). This is primarily used for students who prefer to develop in [GitHub Codespaces](https://github.com/features/codespaces).
