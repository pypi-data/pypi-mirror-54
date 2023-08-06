import importlib.util

from nnql import error

spec = importlib.util.find_spec("torch")
if spec is None:
    raise error.DependencyNotInstalled(
        f"can't find the torch module. "
        "You can install PyTorch dependencies by running 'pip install nnql[pytorch]'"
    )
