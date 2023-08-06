import torch
import torch.nn.parallel
import torch.optim as optim
import torch.utils.data as data
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms


def loader(dataset_size, batch_size, num_workers=4, pin_memory=True):
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )
    return data.DataLoader(
        datasets.FakeData(
            size=dataset_size,
            image_size=(3, 224, 224),
            num_classes=1000,
            transform=transforms.Compose(
                [
                    transforms.RandomResizedCrop(224),
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


def train(model, optimizer, epoches, dataset_size, batch_size):
    data_loader = loader(dataset_size=dataset_size, batch_size=batch_size)
    criterion = torch.nn.CrossEntropyLoss()
    for _ in range(epoches):
        for _, (batch, label) in enumerate(data_loader):
            optimizer.zero_grad()
            output = model(batch)
            criterion(output, label).backward()
            optimizer.step()


def train_vgg16(epoches=2, dataset_size=4, batch_size=2):
    model = models.vgg16().train()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    train(
        model,
        optimizer,
        epoches=epoches,
        dataset_size=dataset_size,
        batch_size=batch_size,
    )


def train_alexnet(epoches=2, dataset_size=4, batch_size=2):
    model = models.alexnet().train()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    train(
        model,
        optimizer,
        epoches=epoches,
        dataset_size=dataset_size,
        batch_size=batch_size,
    )


def train_resnet18(epoches=2, dataset_size=4, batch_size=2):
    model = models.resnet18().train()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    train(
        model,
        optimizer,
        epoches=epoches,
        dataset_size=dataset_size,
        batch_size=batch_size,
    )


if __name__ == "__main__":
    train_vgg16(epoches=1, dataset_size=1, batch_size=1)
