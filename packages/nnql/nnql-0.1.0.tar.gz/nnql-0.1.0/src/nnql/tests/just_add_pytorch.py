import torch


def just_add_pytorch():
    vec = torch.tensor(3, dtype=torch.float32).uniform_().requires_grad_()
    out1 = vec + 1
    out2 = vec + 2
    print(out1, out2)
    out1.backward()
    out2.backward()
    print(vec.grad)


def just_add_pytorch_functional():
    vec = torch.tensor(3, dtype=torch.float32).uniform_().requires_grad_()
    out1 = torch.add(vec, 1)
    out2 = torch.add(vec, 2)
    out1.backward()
    out2.backward()
