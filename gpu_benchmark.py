
import time
import torch

SIZE = 2000
REPEATS = 3

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"MPS available: {torch.backends.mps.is_available()}")

# Use a smaller matrix initially to keep memory usage manageable.
a = torch.randn(SIZE, SIZE)
b = torch.randn(SIZE, SIZE)


def benchmark_cpu():
    # Warm up the CPU implementation.
    _ = a @ b

    start = time.perf_counter()

    for _ in range(REPEATS):
        result = a @ b

    elapsed = (time.perf_counter() - start) / REPEATS
    return elapsed, result


def benchmark_mps():
    if not torch.backends.mps.is_available():
        return None, None

    a_gpu = a.to("mps")
    b_gpu = b.to("mps")

    # Warm up the GPU.
    _ = a_gpu @ b_gpu
    torch.mps.synchronize()

    start = time.perf_counter()

    for _ in range(REPEATS):
        result = a_gpu @ b_gpu

    # GPU operations can be asynchronous, so wait before measuring.
    torch.mps.synchronize()

    elapsed = (time.perf_counter() - start) / REPEATS
    return elapsed, result


cpu_time, cpu_result = benchmark_cpu()

print(f"\nCPU average: {cpu_time:.4f} seconds")

mps_time, mps_result = benchmark_mps()

if mps_time is not None:
    print(f"Apple GPU average: {mps_time:.4f} seconds")
    print(f"Approximate speedup: {cpu_time / mps_time:.2f}x")

    # Check that both implementations give similar results.
    difference = (
        cpu_result - mps_result.cpu()
    ).abs().max().item()

    print(f"Maximum absolute difference: {difference:.6f}")
else:
    print("\nApple GPU unavailable; CPU benchmark completed.")
