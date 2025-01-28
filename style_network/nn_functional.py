import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from PIL import Image
#import matplotlib.pyplot as plt

import torchvision.transforms as transforms
from torchvision.models import vgg19, VGG19_Weights

import copy


def normalization(img, mean, std):
  mean = torch.tensor(mean).view(-1, 1, 1)
  std = torch.tensor(std).view(-1, 1, 1)
  return (img - mean) / std

loader = transforms.Compose([
    transforms.Resize([512, 512]),  # scale imported image
    transforms.ToTensor()])  # transform it into a torch tensor


def image_loader(image_name, device):
    image = Image.open(image_name)
    # fake batch dimension required to fit network's input dimensions
    image = loader(image).unsqueeze(0)
    #image = normalization(image.to(device), cnn_normalization_mean.to(device), cnn_normalization_std.to(device))
    return image.to(device, torch.float)


def gram_matrix(input : torch.Tensor):
  a, b, c, d = input.size()
  input_matrix = input.view(a*b, c*d)
  gram = torch.mm(input_matrix, input_matrix.mT)
  return gram


def style_loss(target, input):
  loss = 0
  for i in range(len(target)):
    loss += F.mse_loss(gram_matrix(target[i]), gram_matrix(input[i]))
  return loss


class ModelStyle(nn.Module):
  def __init__(self):
    super().__init__()
    self.layers = vgg19(weights=VGG19_Weights.DEFAULT).features
    self.layers.requires_grad_(False)
    self.requires_grad_(False)

  def forward(self, x):
    outputs = []
    for layer in self.layers:
      x = layer(x)
      if isinstance(layer, nn.Conv2d):
        outputs.append(x)
    return outputs


