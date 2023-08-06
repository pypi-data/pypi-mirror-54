import time

from nnql import InstContext, Tool
from nnql.graph import Graph


# usage: ./nnql --tool nnql.tools.profiler.Profiler nnql.tests.inference_vgg16
class Profiler(Tool):
    def __init__(self, period: int = 10):
        self.period = period
        self.batch_num = 0

    def instrument(self, context: InstContext) -> None:
        op = context.op
        if self.batch_num % self.period == 0:
            op.attrs.start_time = time.time()
            op.call()
            op.attrs.end_time = time.time()
            op.attrs.elapsed_time = op.attrs.end_time - op.attrs.start_time
            if op.parent is None:
                self.save_graph_attrs(op.graph)
        if op.parent is None:  # this is a top-level op, i.e., the whole graph
            self.batch_num += 1

    def save_graph_attrs(self, graph: Graph):
        pass
