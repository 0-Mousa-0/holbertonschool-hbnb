# Part 2 - Issue Solutions Log

This file records each graded situation (t0 to t6), the original mistake, and the implemented fix.
Each section is updated in the same commit as its corresponding code change.

## t0 - README and project setup documentation

### Mistake
- `part2/README.md` had a brief overview but it did not include clear dependency installation steps.
- It also missed explicit run commands and detailed per-directory/per-file purpose descriptions.

### Solution implemented
- Rewrote `part2/README.md` with:
  - explicit dependency installation command (`pip install -r requirements.txt`);
  - explicit run command (`python run.py`);
  - test commands;
  - detailed project structure and purpose notes for key directories/files.
