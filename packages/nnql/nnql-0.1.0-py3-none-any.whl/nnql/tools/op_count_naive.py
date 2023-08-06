from nnql import Executor, InstContext, Tool


class OpCount(Tool):
    count: int = 0

    def apply(self, executor: Executor):
        def instrument(context: InstContext):
            if context.op.type != "Const":
                self.count += 1
                print("op:", context.op.name, context.op.type)
            context.op.call()

        def init(context: InstContext):
            context.graph.attrs.op_count = 0

        def finish(context: InstContext):
            print(f"op count: {context.graph.attrs.op_count}")
            self.count = context.graph.attrs.op_count

        executor.before_define_graph(init)
        executor.on_define_op(instrument)
        executor.after_run_graph(finish)
