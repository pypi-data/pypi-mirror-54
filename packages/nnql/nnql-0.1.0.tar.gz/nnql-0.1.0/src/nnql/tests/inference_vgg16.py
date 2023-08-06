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
                    transforms.Resize(256),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    normalize,
                ]
            ),
        ),
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )


def inference_vgg16(dataset_size=4, batch_size=2):
    model = models.vgg16(pretrained=True)
    data_loader = loader(dataset_size=dataset_size, batch_size=batch_size)
    for i, (batch, label) in enumerate(data_loader):
        print(model(batch))


if __name__ == "__main__":
    inference_vgg16()
