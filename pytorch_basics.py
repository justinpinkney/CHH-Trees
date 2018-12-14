import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt


transform = transforms.Compose([
                transforms.RandomResizedCrop(224), 
                transforms.ToTensor(),
                ])

dataset = torchvision.datasets.ImageFolder("data/processed", transform=transform)
print(dataset)

data_loader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)
iterator = iter(data_loader)
batch, labels = iterator.next()

grid = torchvision.utils.make_grid(batch, nrow=4)
images = grid.numpy()
print(images.shape)
plt.imshow(np.transpose(images, (1, 2, 0)))
plt.show()
print(labels)
