from nnql import Executor, InstContext, Tool, use
from nnql.executor import start_program
from nnql.graph import Tensor, tensor

import torch


class Pruner(Tool):
    """
    usage: nnql --tool -m nnql.tools.pruner_v2 --program -m nnql.tests.train_model
    """

    def __init__(self):
        self.layer_to_activations = {}
        self.layer_to_gradients = {}
        self.layer_to_masks = {}
        self.batch_num = 0

    def instrument(self, context: InstContext) -> None:
        op = context.op
        if self.need_to_prune(self.batch_num):
            if context.pass_type.is_forward():
                output_tensor = context.op.call()
                assert isinstance(output_tensor, Tensor)
                if op.type == "Conv2d":
                    torch_output = output_tensor.ref
                    self.layer_to_activations[op.id] = torch_output
                    if op.id not in self.layer_to_masks:
                        self.layer_to_masks[op.id] = self.init_mask(torch_output)
                    output_tensor = tensor(torch_output * self.layer_to_masks[op.id])
                context.set_output(output_tensor)
            else:
                op = context.op
                if context.op.type == "Conv2d":
                    self.layer_to_gradients[op.id] = op.input_tensor.ref
                op.call()
                if op.parent is None:  # this is a top-level op, i.e., the whole graph
                    self.update_masks()
        else:
            op.call()
        if (
            op.parent is None and context.pass_type.is_forward()
        ):  # this is a top-level op, i.e., the whole graph
            self.batch_num += 1

    def init_mask(self, output_tensor) -> Tensor:
        return torch.ones_like(output_tensor)

    def update_masks(self):
        pass

    def need_to_prune(self, batch_num: int) -> bool:
        return True


if __name__ == "__main__":
    with Executor():
        use(Pruner())
        start_program()
