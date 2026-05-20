import os
import logging
import torch
import yaml
from PIL import Image
from torch.utils.data import DataLoader
from dataset.lol import LOLDataset
from models.sci_model import Network
from torchmetrics.image import StructuralSimilarityIndexMeasure as SSIM
from torchmetrics.image import PeakSignalNoiseRatio as PSNR
from src.utils import save_checkpoint, save

def load_params(path_config_path: str) -> dict:
    with open(path_config_path, 'r') as f:
        params = yaml.safe_load(f)
    return params

def save_img(img_tensor: torch.Tensor, path: str):
    img_tensor = img_tensor.squeeze(0).cpu().clamp(0, 1)
    img = Image.fromarray((img_tensor.permute(1, 2, 0).numpy() * 255).astype('uint8'))
    img.save(path)

def inference_enhance(img: torch.Tensor, checkpoint_path: str, device: torch.device) -> torch.Tensor:
    from models.sci_model import EnhanceNetwork
    enhance_net = EnhanceNetwork(layers=1, channels=3).to(device)
    checkpoint = torch.load(checkpoint_path, map_location=device)
    # Handle both dict and direct state_dict formats
    state_dict = checkpoint.get('model', checkpoint) if isinstance(checkpoint, dict) and 'model' in checkpoint else checkpoint
    enhance_net.load_state_dict(state_dict)
    enhance_net.eval()
    
    with torch.no_grad():
        output = enhance_net(img)
        loss = enhance_net._loss
    return output

def setup_logging(log_dir: str = './logs') -> tuple[logging.Logger, logging.Logger]:
    os.makedirs(log_dir, exist_ok=True)

    general_logger = logging.getLogger('train')
    general_logger.setLevel(logging.INFO)
    general_logger.handlers.clear()
    general_logger.propagate = False

    general_handler = logging.FileHandler(os.path.join(log_dir, 'train.log'), mode='w')
    general_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    general_logger.addHandler(general_handler)

    metrics_logger = logging.getLogger('metrics')
    metrics_logger.setLevel(logging.INFO)
    metrics_logger.handlers.clear()
    metrics_logger.propagate = False

    metrics_handler = logging.FileHandler(os.path.join(log_dir, 'metrics.csv'), mode='w')
    metrics_handler.setFormatter(logging.Formatter('%(asctime)s,%(message)s'))
    metrics_logger.addHandler(metrics_handler)

    return general_logger, metrics_logger

def main():
    # config GPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if device.type != 'cuda':
        raise RuntimeError('CUDA and maybe GPU isn\'t available')

    # load params
    params = load_params('src/config.yaml')
    DATA_DIR = params.get('DATA_DIR', './data')
    batch_size = params.get('BATCH_SIZE', 16)
    num_workers = params.get('NUM_WORKERS', 4)
    epochs = params.get('EPOCHS', 100)
    learning_rate = params.get('LEARNING_RATE', 1e-4)
    
    # config logging
    logger, metrics_logger = setup_logging()
    logger.info('Starting training')
    
    # data
    train_dataset = LOLDataset(DATA_DIR)
    val_dataset = LOLDataset(DATA_DIR, train = False)
    train_loader = DataLoader(train_dataset, batch_size = batch_size, shuffle = True, num_workers = num_workers)
    val_loader = DataLoader(val_dataset, batch_size = batch_size, shuffle = False, num_workers = num_workers)
    
    # model, optimizer, metrics
    model = Network().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
    ssim_train = SSIM().to(device)
    psnr_train = PSNR(data_range = 1).to(device)
    
    # training loop
    logger.info('Starting training loop')
    loss_history = []
    ssim_history = []
    psnr_history = []
    for epoch in range(epochs):
        logger.info(f'Epoch {epoch + 1}/{epochs}')
        model.train()
        losses = []
        metrics_ssim = []
        metrics_psnr = []
        for low_imgs, high_imgs, _, _ in train_loader:
            low_imgs = low_imgs.to(device)
            high_imgs = high_imgs.to(device)
            optimizer.zero_grad()
            ilist, rlist, inlist, attlist = model(low_imgs)
            loss = model._loss(low_imgs)
            loss.backward()
            optimizer.step()
            losses.append(loss.item())
            with torch.no_grad():
                ssim_train.update(rlist[-1], high_imgs)
                psnr_train.update(rlist[-1], high_imgs)
        loss_history.append(sum(losses)/len(losses))
        ssim_val = ssim_train.compute()
        psnr_val = psnr_train.compute()
        ssim_history.append(ssim_val.item() if isinstance(ssim_val, torch.Tensor) else ssim_val)
        psnr_history.append(psnr_val.item() if isinstance(psnr_val, torch.Tensor) else psnr_val)
        metrics_logger.info(f'epoch={epoch + 1},loss={sum(losses)/len(losses):.6f},psnr={psnr_val:.4f},ssim={ssim_val:.4f}')
        ssim_train.reset()
        psnr_train.reset()
        logger.info(f'Finished epoch {epoch + 1}/{epochs}')
        if (epoch+1) % 10 == 0:
            logger.info(f'Saving checkpoint for epoch {epoch + 1}')
            checkpoint_dir = './checkpoints'
            os.makedirs(checkpoint_dir, exist_ok=True)
            save(model, os.path.join(checkpoint_dir, f'model_epoch_{epoch + 1}.pth'))
            logger.info(f'Saved checkpoint for epoch {epoch + 1}')
            model.eval()
            with torch.no_grad():
                for low_imgs, high_imgs, low_paths, high_paths in val_loader:
                    low_imgs = low_imgs.to(device)
                    high_imgs = high_imgs.to(device)
                    ilist, rlist, inlist, attlist = model(low_imgs)
                    for i in range(low_imgs.size(0)):
                        save_img(rlist[-1][i], os.path.join(checkpoint_dir, f'val_epoch_{epoch + 1}_{os.path.basename(low_paths[i])}'))
    logger.info('Finished training')
if __name__ == '__main__':
    main()