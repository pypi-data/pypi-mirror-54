from nnql import Executor
from nnql.tools.pruner import Pruner

import torch
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data as data
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from torch.autograd import Variable

train_path = ""


def loader(path, batch_size=32, num_workers=4, pin_memory=True):
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )
    return data.DataLoader(
        datasets.ImageFolder(
            path,
            transforms.Compose(
                [
                    transforms.Scale(256),
                    transforms.RandomSizedCrop(224),
                    transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    normalize,
                ]
            ),
        ),
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )


def train(model, optimizer, epoches):
    data_loader = loader(train_path)
    criterion = torch.nn.CrossEntropyLoss()
    for i in range(epoches):
        for i, (batch, label) in enumerate(data_loader):
            model.zero_grad()
            input = Variable(batch)
            criterion(model(input), Variable(label)).backward()
            optimizer.step()


def pruning(model, optimizer, executor):
    data_loader = loader(train_path)
    criterion = torch.nn.CrossEntropyLoss()
    for i, (batch, label) in enumerate(data_loader):
        with executor:
            # before_execute hook is invoked
            model.zero_grad()
            input = Variable(batch)
            output = model(input)  # forward part of on_invoke_op
            criterion(
                output, Variable(label)
            ).backward()  # backward part of on_invoke_op
            # after_execute hook is invoked


def test_pruning():
    pruner = Pruner()
    executor = Executor()
    executor.use(pruner)

    model = models.vgg16(pretrained=True)
    torch.save(model, "model")
    iterations = 10
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    for _ in range(iterations):
        pruning(model, optimizer, executor)
    train(model, optimizer, epoches=10)
