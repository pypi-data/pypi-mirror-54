from nnql import Executor, InstContext, Tool

from torch import Tensor


class Pruner(Tool):
    def __init__(self):
        self.layer_to_activations = {}
        self.layer_to_gradients = {}
        self.layer_to_masks = {}

    def apply(self, executor: Executor):
        def forward(context: InstContext):
            op = context.op
            output_tensor = context.op.call()
            assert isinstance(output_tensor, Tensor)
            if op.type == "Conv2d":
                self.layer_to_activations[op.name] = output_tensor.ref
                if op.name not in self.layer_to_masks:
                    self.layer_to_masks[op.name] = self.init_mask(output_tensor)
                output_tensor = output_tensor * self.layer_to_masks[op.name]
            context.set_output(output_tensor)

        def backward(context: InstContext):
            op = context.op
            if context.op.type == "Conv2d":
                self.layer_to_gradients[op.name] = op.input_tensor.ref
            context.op.call()

        def finish(context: InstContext):
            self.update_masks()

        executor.on_invoke_op(forward=forward, backward=backward)
        executor.after_execute(finish)

    def init_mask(self, output_tensor) -> Tensor:
        pass

    def update_masks(self):
        pass
