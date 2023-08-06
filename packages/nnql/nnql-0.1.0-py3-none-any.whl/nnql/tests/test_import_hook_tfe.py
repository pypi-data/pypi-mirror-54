from nnql import Executor, InstContext, Tool, use
from nnql.graph import Tensors, tensors
from nnql.tests.just_add_tfe import just_add_tfe

import tensorflow as tf


class SkipOpCall(Tool):
    def apply(self, executor: Executor):
        async def instrument(context: InstContext) -> Tensors:
            return tensors(tf.random.uniform(shape=(3,)))

        executor.on_define_op(instrument)


def test_skip_op_call():
    with Executor():
        use(SkipOpCall())
        just_add_tfe()
