# Submodule Management Guide

Project Fractal relies on Git submodules to partition orchestrator backend services (`FractalCore`) from client-side edge codebases (`FractalAndroid`).

## Cloning the Repository

To clone this repository with all its submodules populated:

```bash
git clone --recursive https://github.com/Fractal-Compute-Orchestrations/FractalWorkspace.git
```

If you cloned without `--recursive`, run:

```bash
git submodule update --init --recursive
```

## Pulling Updates

When pulling changes from the master branch, submodules do not update automatically. Run:

```bash
git pull origin master
git submodule update --recursive --remote
```

## Working Inside Submodules

When making changes within submodules, remember that they point to specific commits.
Before committing in a submodule:
1. Navigate to the submodule directory (e.g. `FractalCore`).
2. Checkout the active development branch (e.g. `git checkout master`).
3. Commit and push from the submodule first before updating the reference pointer in the main workspace repo.
