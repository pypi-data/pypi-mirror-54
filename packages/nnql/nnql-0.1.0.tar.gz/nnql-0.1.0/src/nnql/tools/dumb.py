from nnql import Executor, InstContext, Tool


class Dumb(Tool):
    def apply(self, executor: Executor):
        def instrument(context: InstContext):
            context.op.call()

        executor.on_define_op(instrument)
