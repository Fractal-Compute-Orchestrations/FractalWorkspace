# Submodule Management Guide

Project Fractal utilizes Git submodules to decouple backend orchestration services (`FractalCore`) from edge client implementations (`FractalAndroid`).

## Cloning the Repository

To clone the workspace repository with all submodules populated:

```bash
git clone --recursive https://github.com/Fractal-Compute-Orchestrations/FractalWorkspace.git
```

If the repository was cloned without `--recursive`, initialize submodules manually:

```bash
git submodule update --init --recursive
```

## Pulling Updates

When pulling changes from the master branch, submodule reference pointers must be synchronized:

```bash
git pull origin master
git submodule update --recursive --remote
```

## Submodule Development Workflow

Submodule references in the parent repository point to specific commit hashes. When making changes inside a submodule:

1. Navigate to the submodule directory:
   ```bash
   cd FractalCore
   # or
   cd FractalApp/FractalAndroid
   ```
2. Checkout the active development branch:
   ```bash
   git checkout main   # or master
   ```
3. Commit and push changes directly from within the submodule directory:
   ```bash
   git add .
   git commit -m "feat: your change summary"
   git push origin main
   ```
4. Return to the root workspace and update the submodule commit reference:
   ```bash
   cd ../..
   git add FractalCore FractalApp/FractalAndroid
   git commit -m "chore: update submodule pointers"
   git push origin master
   ```
