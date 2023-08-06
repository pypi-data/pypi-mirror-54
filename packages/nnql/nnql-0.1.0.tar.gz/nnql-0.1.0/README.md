## Create a virtual environment

```bash
conda env create -f environment.yml
source activate nnql
```

## Install dependencies

There are two options:

- Use pip:
    ```bash
    pip install -e ".[all]"
    ```
- Use poetry:
    ```bash
    poetry install -E all
    ```

## Install git pre-commit hooks

```bash
pre-commit install
```
