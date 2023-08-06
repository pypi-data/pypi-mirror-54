from nnql import Executor, use
from nnql.tests.train_model import train_vgg16
from nnql.tools.print_graph import PrintGraph


def test_print_graph():
    with Executor():
        use(PrintGraph())
        train_vgg16(epoches=1, dataset_size=1, batch_size=1)


if __name__ == "__main__":
    # train_vgg16()
    test_print_graph()
