from typing import List, Tuple

from nnql import InstContext, Tool
from nnql.graph import Graph, Op, Tensor


class Extractor(Tool):
    """
    usage: ./nnql --tool nnql.tools.effective_path.Extractor nnql.tests.inference_vgg16
    """

    def __init__(self):
        self.output_neurons = {}
        self.layer_masks = {}
        self.weighted_inputs = {}
        self.input_masks = {}
        self.batch_num = 0

    def instrument(self, context: InstContext) -> None:
        op = context.op
        if len(op.children) == 0:  # indicate that this is a basic op
            outputs = self.with_weighted_input(context.op).call()
            assert isinstance(outputs, List)
            output_tensor, weighted_input = outputs
            self.output_neurons[op.id] = output_tensor
            self.weighted_inputs[op.id] = weighted_input
        else:
            op.call()
        if op.parent is None:  # this is a top-level op, i.e., the whole graph
            for op in self.iterate_from_last_layer(context.graph):
                if self.is_last_layer(op.id):
                    layer_output = self.output_neurons[op.id]
                    output_mask = self.extract_output_mask(layer_output)
                else:
                    output_mask = self.input_masks[op.output_op.id]
                layer_mask, input_mask = self.extract_layer(
                    op,
                    self.weighted_inputs[op.id],
                    self.output_neurons[op.id],
                    output_mask,
                )
                self.layer_masks[op.id] = layer_mask
                self.input_masks[op.id] = input_mask
            self.store(self.batch_num, self.layer_masks)
            self.batch_num += 1

    def iterate_from_last_layer(self, graph: Graph) -> List[Op]:
        pass

    def with_weighted_input(self, op) -> Op:
        pass

    def is_last_layer(self, op: int) -> bool:
        pass

    def extract_output_mask(self, layer_output) -> Tensor:
        pass

    def extract_layer(
        self, op: Op, weighted_input, output_neuron, output_mask
    ) -> Tuple[Tensor, Tensor]:
        pass

    def store(self, batch_id, layer_masks):
        pass
