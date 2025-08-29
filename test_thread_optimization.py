#!/usr/bin/env python3
"""
test_thread_optimization.py - Test thread pool optimization

This test verifies that the thread pool sizing is calculated correctly
based on available CPU cores and system resources.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from UTILS.thread_utils import ThreadPoolOptimizer, get_optimal_thread_count
from CONST.constants import AppConstants


def test_thread_calculation():
    """Test thread calculation logic"""
    print("=" * 60)
    print("TESTING THREAD POOL OPTIMIZATION")
    print("=" * 60)

    # Get system information
    system_info = ThreadPoolOptimizer.get_system_info()
    print(f"System Information:")
    print(f"  CPU Cores: {system_info['cpu_count']}")
    print(f"  Translation Threads: {system_info['translation_threads']}")
    print(f"  API Request Threads: {system_info['api_request_threads']}")
    print(f"  Optimization Type: {system_info['system_type']}")
    print()

    # Test different operation types
    operations = ["translation", "api", "general"]
    print("Thread Calculations by Operation Type:")
    print("-" * 40)

    for op_type in operations:
        thread_count = get_optimal_thread_count(op_type)
        print(f"  {op_type.capitalize()}: {thread_count} threads")

    print()

    # Test AppConstants integration
    print("AppConstants Integration:")
    print("-" * 40)
    print(f"  MAX_THREAD_POOL_WORKERS: {AppConstants.MAX_THREAD_POOL_WORKERS}")

    # Verify the calculation makes sense
    cpu_count = ThreadPoolOptimizer.get_cpu_count()
    expected_min = max(2, cpu_count)  # At least 2 threads
    expected_max = min(16, cpu_count + 4)  # At most 16 threads or cpu_count + 4

    actual = AppConstants.MAX_THREAD_POOL_WORKERS

    print(f"  Expected range: {expected_min} - {expected_max}")
    print(f"  Actual value: {actual}")

    if expected_min <= actual <= expected_max:
        print("  ✅ Thread count is within expected range")
    else:
        print("  ❌ Thread count is outside expected range")

    print()

    # Test edge cases
    print("Edge Case Testing:")
    print("-" * 40)

    # Test with custom parameters
    custom_threads = ThreadPoolOptimizer.calculate_optimal_threads(
        operation_type="io_bound",
        multiplier=3.0,
        max_threads=10
    )
    print(f"  Custom calculation (3x multiplier, max 10): {custom_threads}")

    cpu_bound = ThreadPoolOptimizer.calculate_optimal_threads("cpu_bound")
    print(f"  CPU-bound operations: {cpu_bound}")

    print()

    # Performance recommendations
    print("Performance Recommendations:")
    print("-" * 40)

    if system_info['cpu_count'] >= 8:
        print("  💪 High-performance system detected")
        print("     - Translation operations will use parallel processing effectively")
        print("     - Consider increasing API rate limits if needed")
    elif system_info['cpu_count'] >= 4:
        print("  ⚖️  Balanced system detected")
        print("     - Good balance between performance and resource usage")
        print("     - Thread pool sizing is optimal for this configuration")
    else:
        print("  🐌 Low-performance system detected")
        print("     - Thread pool sized conservatively to avoid resource exhaustion")
        print("     - Consider reducing concurrent operations if experiencing slowdowns")

    print()
    print("=" * 60)
    print("✅ THREAD OPTIMIZATION TEST COMPLETED")
    print("=" * 60)


def test_thread_safety():
    """Test that thread calculations are thread-safe"""
    print("\nTesting Thread Safety:")
    print("-" * 40)

    import threading
    results = []

    def worker():
        result = get_optimal_thread_count("translation")
        results.append(result)

    # Run multiple threads to test thread safety
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Check if all results are consistent
    if len(set(results)) == 1:
        print(f"  ✅ Thread-safe: All {len(results)} threads returned {results[0]}")
    else:
        print(f"  ❌ Not thread-safe: Got different results {set(results)}")

    print()


if __name__ == "__main__":
    test_thread_calculation()
    test_thread_safety()
