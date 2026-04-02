import torch

if torch.cuda.is_available():
    print("✅ CUDA is available!")
    print(f"GPU Name: {torch.cuda.get_device_name(0)}")