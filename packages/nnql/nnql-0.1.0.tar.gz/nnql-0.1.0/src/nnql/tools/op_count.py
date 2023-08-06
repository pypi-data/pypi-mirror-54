from nnql import Executor, InstContext, Tool
from nnql.graph import tensor_list, tensor_ref_list

import tensorflow as tf


class OpCount(Tool):
    count: int = 0

    def apply(self, executor: Executor):
        def instrument(context: InstContext):
            def do_count(*np_inputs):
                executor.graph.attrs.count += 1
                return np_inputs

            op = context.op
            if op.type != "Const":
                print("op:", op.name, op.type)
                tf_inputs = tensor_ref_list(op.input_tensors)
                new_inputs = tensor_list(
                    tf.py_function(
                        do_count, tf_inputs, [input.dtype for input in tf_inputs]
                    )
                )
                op.input_tensors = new_inputs
            op.call()

        def init(context: InstContext):
            context.graph.attrs.op_count = 0

        def finish(context: InstContext):
            print(f"op count: {context.graph.attrs.op_count}")
            self.count = context.graph.attrs.op_count

        executor.before_define_graph(init)
        executor.on_define_op(instrument)
        executor.after_run_graph(finish)
