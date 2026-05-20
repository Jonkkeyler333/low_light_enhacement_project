import os
import torch
import numpy as np
from PIL import Image
import torchvision.transforms.functional as F
from models.sci_model import Finetunemodel
from torchmetrics.functional.image import peak_signal_noise_ratio as PSNR
from skimage.metrics import structural_similarity as SSIM
import logging
import matplotlib.pyplot as plt

def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Inference in device type {device.type}')
    model_path = 'checkpoints/model_epoch_100.pth'
    input_folder = 'data/eval15/low'
    reference_folder = 'data/eval15/high'
    output_folder = 'results'
    os.makedirs(output_folder, exist_ok=True)
    logging.basicConfig(filename = os.path.join(output_folder, 'inference_log.csv'), level=logging.INFO, format='%(asctime)s,%(levelname)s,%(message)s')
    
    # load model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Don't exist model {model_path}")
    model = Finetunemodel(model_path).to(device)
    model.eval()

    psnr_values = []
    ssim_values = []
    with torch.inference_mode():
        for img_name, ref_name in zip(sorted(os.listdir(input_folder)), sorted(os.listdir(reference_folder))):
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f'Image {img_name} is not a valid image file. Skipping.')
                continue
            img_path = os.path.join(input_folder, img_name)
            img = Image.open(img_path).convert('RGB') # H, W, C
            input_tensor = F.to_tensor(img).unsqueeze(0).to(device) # 1, C, H, W
            reference_tensor = F.to_tensor(Image.open(os.path.join(reference_folder, ref_name)).convert('RGB')).unsqueeze(0).to(device) # 1, C, H, W
            i_map, r = model(input_tensor)
            enhanced_tensor = r
            psnr = PSNR(enhanced_tensor, reference_tensor, data_range=1.0).item()
            psnr_values.append(psnr)
            img_np = enhanced_tensor.squeeze(0).cpu().permute(1, 2, 0).numpy()
            ref_np = reference_tensor.squeeze(0).cpu().permute(1, 2, 0).numpy()
            ssim_result = SSIM(img_np, ref_np, data_range=1.0, channel_axis=-1, full=True)
            ssim_val = float(ssim_result[0])
            map_error = ssim_result[1]
            ssim_values.append(ssim_val)
            logging.info(f"{img_name},PSNR: {psnr:.2f}, SSIM: {ssim_val:.4f}")
            out_tensor = enhanced_tensor.squeeze(0).cpu().clamp(0, 1)
            out_img = Image.fromarray((out_tensor.permute(1, 2, 0).numpy() * 255).astype('uint8'))
            out_img.save(os.path.join(output_folder, img_name))
            # map_error_norm = np.clip((map_error + 1.0) / 2.0 * 255.0, 0, 255).astype('uint8')
            # map_img = Image.fromarray(map_error_norm)
            fig, ax = plt.subplots()
            im = ax.imshow(map_error, cmap='viridis')
            ax.set_title(f'SSIM Error Map for {img_name}')
            ax.axis('off')
            fig.colorbar(im, ax=ax)
            plt.savefig(os.path.join(output_folder, f"mapa_ssim_{img_name}.png"), dpi = 400)
            print(f" Image save: {img_name} | PSNR: {psnr:.2f} | SSIM: {ssim_val:.4f}")
    logging.info(f"Average PSNR: {np.mean(psnr_values):.2f}, Average SSIM: {np.mean(ssim_values):.4f}")

if __name__ == '__main__':
    main()
