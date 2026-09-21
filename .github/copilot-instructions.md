# AI Instructions

## Workspace Details

This repository is a base template for PH 306 (Computational Physics) at [UAHuntsville](https://www.uah.edu/).

This repository itself is not an assignment submission repository. The instructor copies this template to create a separate repository for each assignment, then adds assignment-specific instructions there.

The course uses Python. Students may complete assignments using either:
- Python scripts
- Jupyter notebooks

Submissions are made through CodeGrade. Auto-grading is used, with possible manual follow-up grading by the instructor.

Students may work in one of these environments:
- Local machine
- GitHub Codespaces
- Google Colab
- CodeGrade platform

The instructor provides assignment-specific platform instructions. Students are not expected to manually manage Python environments.

Environment setup expectations:
- Codespaces: the repository includes devcontainer.json and environment.yml (micromamba-managed) to provision the environment.
- Google Colab: the repository includes requirements.txt for package installation.
- CodeGrade: environment is preconfigured by the instructor.

### Regarding Student Use of AI

Generative AI use is permitted. However, students are responsible for explaining their code and results through one of the following:
1. Meeting with the instructor during class.
2. Giving a class presentation about their assignment.

## Generating a Specific Assignment Template

If an AI model is asked to generate a specific assignment template, it should treat this as a full template regeneration task.

Required behavior:
1. Replace prior assignment-facing files rather than incrementally patching them.
2. Generate content from the instructor-provided assignment instructions.
3. Ensure all required assignment files are present and internally consistent.

Scope boundaries for replacement:
- Assignment-facing files may be replaced as part of regeneration (for example: assignment.ipynb, assignment.py, README.md, requirements.txt, environment.yml).
- Infrastructure and repository-maintenance files should not be modified unless explicitly requested (for example: LICENSE, .devcontainer/*, .github/*, utility modules).

When generating a specific assignment template, produce:
- Exactly one primary student work file, either assignment.ipynb or assignment.py
- README.md with assignment instructions
- requirements.txt with required Python packages
- environment.yml with required Python packages

Consistency rules for generated files:
- Package requirements listed in requirements.txt and environment.yml should match in intent.
- README.md should clearly state whether students must use the notebook or script workflow for that assignment.
- The student work file should include placeholders or prompts where student code is expected.

Repository consistency rules:
- README.md must only reference files and folders that actually exist in the repository at generation time.
- If tests are referenced in README.md, the referenced test paths must exist.
- If a script workflow is selected, the script entry points and function names should match any referenced tests or checks.

Environment specification rules:
- requirements.txt should be compatible with pip installation in Google Colab.
- environment.yml should remain suitable for micromamba/conda-based workflows.
- Prefer broadly available package versions unless the assignment requires strict pinning.

Validation before completion:
- Confirm exactly one primary student work file is designated in README.md.
- Confirm requirements.txt and environment.yml are both present after regeneration.
- Run at least one lightweight sanity check appropriate to the generated workflow (for example, Python syntax check for script-based assignments).

Autograder contract rules:
- Do not rename required functions, classes, or files that are referenced by tests or grading harnesses.
- Keep function signatures stable unless the instructor instructions explicitly require changes.
- Ensure README.md instructions, starter code names, and test expectations all use the same identifiers.

Notebook hygiene rules (when notebook workflow is selected):
- Keep notebook cells in a clear, top-to-bottom execution order.
- Avoid hidden state dependencies between cells whenever possible.
- Include markdown prompts that clearly indicate where students should write code and explanations.
