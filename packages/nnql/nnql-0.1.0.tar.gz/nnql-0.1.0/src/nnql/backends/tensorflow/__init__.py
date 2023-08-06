import importlib.util

from nnql import error

spec = importlib.util.find_spec("tensorflow")
if spec is None:
    raise error.DependencyNotInstalled(
        f"can't find the tensorflow module. "
        "You can install TensorFlow dependencies "
        "by running 'pip install nnql[tensorflow]'"
    )
