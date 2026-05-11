import os
import logging
import torch
import yaml
from PIL import Image
from torch.utils.data import DataLoader
from datasets.lol import LOLDataset
from models.sci_model import Network

def load_params(path_config_path: str) -> dict:
    with open(path_config_path, 'r') as f:
        params = yaml.safe_load(f)
    return params

def save_img(img_tensor: torch.Tensor, path: str):
    img_tensor = img_tensor.squeeze(0).cpu().clamp(0, 1)
    img = Image.fromarray((img_tensor.permute(1, 2, 0).numpy() * 255).astype('uint8'))
    img.save(path)

def main():
    # # config GPU
    # devide = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # if devide != 'cuda':
    #     raise RuntimeError('CUDA and maybe GPU isn\'t available')

    # # config logging
    # logging.basicConfig(filename = 'logs.csv', filemode='w', level = logging.INFO, format = '%(asctime)s,%(levelname)s,%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    print('hello world')