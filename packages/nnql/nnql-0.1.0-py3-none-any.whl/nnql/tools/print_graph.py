from nnql import Executor, InstContext, Tool, use
from nnql.executor import start_program


class PrintGraph(Tool):
    """
    usage: nnql --tool -m nnql.tools.print_graph --program -m nnql.tests.train_model
    """

    def instrument(self, context: InstContext) -> None:
        op = context.op
        print("  " * op.level + str(op))
        op.call()


if __name__ == "__main__":
    with Executor():
        use(PrintGraph())
        start_program()
