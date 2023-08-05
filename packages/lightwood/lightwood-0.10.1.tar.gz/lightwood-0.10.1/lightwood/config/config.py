import torch


class CONFIG:
    USE_CUDA = False
    if torch.cuda.device_count() > 0:
        USE_CUDA = True


    USE_DEVICE = None
    USE_CACHE = True
