# TabPFNPractitioner

Hands-on notebooks on working with **TabPFN**, a tabular foundation model, written for practitioners
who built their instincts on gradient boosting. Each notebook walks the classical pre-modeling
reflexes (scaling, missing values, parameters) and shows how they change when the model is a
pretrained transformer instead of a booster. Every experiment is a small, self-contained synthetic
construction, so the behaviour is real but the setup stays easy to read.

## Environment

Managed with [uv](https://docs.astral.sh/uv/). Python 3.11, fully pinned via `uv.lock`.

```bash
# install uv (once)
curl -LsSf https://astral.sh/uv/install.sh | sh

# from the repo root: create the venv and install the exact pinned versions
uv sync

# launch Jupyter in the project's venv
uv run jupyter lab
```

`uv` reads `.python-version` and fetches Python 3.11 automatically if it is missing.

### GPU vs CPU

TabPFN runs on CPU but its prediction step is much slower; a CUDA GPU is recommended. On Linux the
default `torch` wheel bundles **CUDA 12.4**, so `uv sync` gives GPU support out of the box (needs an
NVIDIA driver supporting CUDA 12.4 or newer). For a CPU-only build, uncomment the `pytorch-cpu`
index block in `pyproject.toml` before running `uv sync`.

### First run

TabPFN downloads its pretrained checkpoint (about 213 MB for the v3 classifier) to `~/.cache/tabpfn/`
on first use, so the first run needs network access. Every run after that is offline.

## Reproducibility

`uv.lock` pins the full transitive dependency graph, so `uv sync` reproduces the exact environment on
any machine. Regenerate it with `uv lock` after editing `pyproject.toml`.

## License

TODO: add a license before publishing (for example MIT or Apache-2.0).
