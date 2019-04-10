import torch
from torchvision import datasets, transforms

data_dir = "data/test"

data_transforms = transforms.ToTensor()

extensions = ['.txt']

train_data = datasets.DatasetFolder(root=data_dir, loader='', extensions=extensions, target_transform=data_transforms)
#train_data = torch.Tensor(train_data)
data_loader = torch.utils.data.DataLoader(train_data,
                                          batch_size=4,
                                          shuffle=True)

print(next(train_data.loader))

