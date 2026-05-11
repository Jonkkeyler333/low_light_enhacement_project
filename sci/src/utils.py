import numpy as np
import os
import torch
import shutil

def count_parameters_in_MB(model):
    # para = 0.0
    # for name, v in model.named_parameters():
    #     if v.requires_grad == True:
    #         if "auxiliary" not in name:
    #             para += np.prod(v.size())
    # return para / 1e6
    return np.sum(np.prod(v.size()) for name, v in model.named_parameters() if "auxiliary" not in name)/1e6



def save_checkpoint(state, is_best, save):
  filename = os.path.join(save, 'checkpoint.pth.tar')
  torch.save(state, filename)
  if is_best:
    best_filename = os.path.join(save, 'model_best.pth.tar')
    shutil.copyfile(filename, best_filename)


def save(model, model_path):
  torch.save(model.state_dict(), model_path)


def load(model, model_path):
  model.load_state_dict(torch.load(model_path))