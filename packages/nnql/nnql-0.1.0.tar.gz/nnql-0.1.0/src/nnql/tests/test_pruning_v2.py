from nnql import Executor, use
from nnql.tests.just_add_pytorch import just_add_pytorch_functional
from nnql.tests.train_model import train_vgg16
from nnql.tools.pruner_v2 import Pruner


def test_pruning_v2_simple():
    with Executor():
        use(Pruner())
        just_add_pytorch_functional()


def test_pruning_v2():
    with Executor():
        use(Pruner())
        train_vgg16()


def test_train_vgg16():
    train_vgg16()


if __name__ == "__main__":
    train_vgg16()
