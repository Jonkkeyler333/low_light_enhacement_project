from PIL import Image
import os
import numpy as np
import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms
import torchvision.transforms.functional as F

class LOLDataset(Dataset):
    def __init__(self, root_dir: str, train:bool = True, crop_size = 256) -> None:
        super().__init__()
        self.root_dir = root_dir
        self.train = train
        self.crop_size = crop_size
        self.transform = transforms.Compose([
            transforms.ToTensor(),
        ])
        self.low_images = []
        self.high_images = []
        if self.train:
            self.low_dir = os.path.join(root_dir, 'our485/low')
            self.high_dir = os.path.join(root_dir, 'our485/high')
        else:
            self.low_dir = os.path.join(root_dir, 'eval15/low')
            self.high_dir = os.path.join(root_dir, 'eval15/high')    
        for file in os.listdir(self.low_dir):
            if file.endswith('.png'):
                image_path = os.path.join(self.low_dir, file)
                self.low_images.append(image_path)
        for file in os.listdir(self.high_dir):
            if file.endswith('.png'):
                image_path = os.path.join(self.high_dir, file)
                self.high_images.append(image_path)
        self.low_images.sort()
        self.high_images.sort()
    
    def _load_image_transform(self, image_path: str) -> torch.Tensor:
        image = Image.open(image_path).convert('RGB')
        img_norm = self.transform(image)
        if torch.is_tensor(img_norm):
            return img_norm
        else:
            raise TypeError(f"Expected a torch.Tensor, but got {type(img_norm)}")
        
    def __len__(self) -> int:
        return len(self.low_images)
    
    def __getitem__(self, index) -> tuple[torch.Tensor, torch.Tensor, str, str]:
        low_image_path = self.low_images[index]
        high_image_path = self.high_images[index]
        low_image = self._load_image_transform(low_image_path)
        high_image = self._load_image_transform(high_image_path)
        i, j, h, w = transforms.RandomCrop.get_params(low_image, output_size = (self.crop_size,self.crop_size) )
        low_image = F.crop(low_image, i, j, h, w)
        high_image = F.crop(high_image, i, j, h, w)
        return low_image, high_image, low_image_path, high_image_path