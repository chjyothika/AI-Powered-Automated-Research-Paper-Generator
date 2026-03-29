"""
GPU Test Script - Verify CUDA functionality
"""
import torch

def test_gpu():
    print("=== GPU TEST RESULTS ===")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"GPU Device: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        print(f"CUDA Version: {torch.version.cuda}")
        
        # Test tensor operations on GPU
        device = torch.device("cuda")
        x = torch.randn(1000, 1000, device=device)
        y = torch.randn(1000, 1000, device=device)
        z = torch.matmul(x, y)
        
        print(f"GPU tensor operation successful: {z.shape}")
        print("GPU is working correctly!")
    else:
        print("CUDA not available")
    
    print("========================")

if __name__ == "__main__":
    test_gpu()