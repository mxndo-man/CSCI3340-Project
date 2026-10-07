---
title: CI
---

# CI basics

This is how the CI pipeline for this repo works. It runs every time we push, and it's made of two files: the workflow itself, and a small setup action that the workflow reuses.

## The workflow

`.github/workflows/code-quality.yaml`

```yml
name: Python Code Quality
on: [push]
jobs:
  lock_file:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: ./.github/actions/setup
      - run: uv lock --locked
  linting:
    runs-on: ubuntu-latest
    needs: [lock_file]
    steps:
      - uses: actions/checkout@v6
      - uses: ./.github/actions/setup
      - run: uvx ruff check .
```

- `name` is just the name of the pipeline. It's what shows up in the Actions tab.
- `on: [push]` means it runs every time someone pushes to the repo.
- `jobs` is where the real work happens. Each job runs on its own fresh machine.
  - `lock_file` is the name of the first job. It makes sure `uv.lock` matches `pyproject.toml`.
  - `linting` is the second job. It runs Ruff on the code.
  - `needs: [lock_file]` means linting waits for `lock_file` and only runs if it passes.
  - `runs-on: ubuntu-latest` is the image the job runs on.
  - `steps` is the list of things the job does, in order:
    - `actions/checkout@v6` pulls the repo onto the machine.
    - `./.github/actions/setup` runs the setup action from below.
    - `run: uvx ruff check .` is the actual check.

Every job follows this same pattern: checkout, setup, then one command.

## The setup action

`.github/actions/setup/action.yml`

```yml
name: "install uv"
description: "installs uv using the community action"
runs:
  using: composite
  steps:
    - name: install uv
      uses: astral-sh/setup-uv@v6
      with:
        version: "latest"
    - name: install python
      shell: bash
      run: uv python install
```

This is a composite action, which just means it bundles a few steps into one so I don't have to copy them into every job.

- `install uv`. 
- `install python` runs `uv python install`, which reads `.python-version` and installs that version of Python.
- `shell: bash` is needed on any `run` step inside a composite action. It won't work without it. 
