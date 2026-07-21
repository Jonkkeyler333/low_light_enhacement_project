import torch
from app.core.settings import Settings, get_settings
from app.inference.model import Finetunemodel

class SciEngine:
    def __init__(self):
        self.settings: Settings = get_settings()
        self.model_path = self.settings.model_path
        self.model_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
    
    def load(self) -> None:
        self.model = Finetunemodel(self.model_path)
        self.model.to(self.model_device)
        self.model.eval()