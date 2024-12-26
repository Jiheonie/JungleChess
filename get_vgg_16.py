import torch
import torchvision.models as models

vgg16 = models.vgg16(pretrained=False)

features = vgg16.features
print(features)