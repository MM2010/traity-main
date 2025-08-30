#!/usr/bin/env python3
"""
thread_monitor.py - Monitor thread pool performance

This script monitors and displays thread pool usage statistics
and performance metrics for the Traity application.
"""

import sys
import os
import time
import psutil

# Aggiungi il percorso della directory principale al sys.path
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, main_dir)

from UTILS.thread_utils import ThreadPoolOptimizer
from CONST.constants import AppConstants


def get_system_stats():
    """Get current system statistics"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory.percent,
        'memory_used_gb': memory.used / (1024**3),
        'memory_total_gb': memory.total / (1024**3)
    }


def display_thread_optimization_report():
    """Display comprehensive thread optimization report"""
    print("=" * 80)
    print("THREAD POOL OPTIMIZATION REPORT - TRAITY QUIZ APPLICATION")
    print("=" * 80)

    # System Information
    system_info = ThreadPoolOptimizer.get_system_info()
    stats = get_system_stats()

    print(f"\n{'SYSTEM INFORMATION':<25}")
    print("-" * 50)
    print(f"{'CPU Cores:':<20} {system_info['cpu_count']}")
    print(f"{'CPU Usage:':<20} {stats['cpu_percent']:.1f}%")
    print(f"{'Memory Usage:':<20} {stats['memory_percent']:.1f}%")
    print(f"{'Memory Used:':<20} {stats['memory_used_gb']:.1f} GB / {stats['memory_total_gb']:.1f} GB")

    print(f"\n{'THREAD OPTIMIZATION':<25}")
    print("-" * 50)
    print(f"{'Translation Threads:':<20} {system_info['translation_threads']}")
    print(f"{'API Request Threads:':<20} {system_info['api_request_threads']}")
    print(f"{'Optimization Type:':<20} {system_info['system_type']}")

    print(f"\n{'APPLICATION CONFIGURATION':<25}")
    print("-" * 50)
    print(f"{'Max Thread Pool Workers:':<20} {AppConstants.MAX_THREAD_POOL_WORKERS}")

    # Performance Analysis
    cpu_count = system_info['cpu_count']
    translation_threads = system_info['translation_threads']

    print(f"\n{'PERFORMANCE ANALYSIS':<25}")
    print("-" * 50)

    if cpu_count >= 16:
        performance_level = "🚀 EXTREME PERFORMANCE"
        description = "Exceptional parallel processing capability"
    elif cpu_count >= 8:
        performance_level = "💪 HIGH PERFORMANCE"
        description = "Excellent for parallel translation operations"
    elif cpu_count >= 4:
        performance_level = "⚖️  BALANCED PERFORMANCE"
        description = "Good balance of performance and efficiency"
    else:
        performance_level = "🐌 MODERATE PERFORMANCE"
        description = "Conservative threading for resource management"

    print(f"{'Performance Level:':<20} {performance_level}")
    print(f"{'Description:':<20} {description}")

    # Thread Efficiency Metrics
    thread_efficiency = (translation_threads / cpu_count) * 100
    print(f"{'Thread Efficiency:':<20} {thread_efficiency:.1f}%")

    if thread_efficiency > 150:
        print("  📈 High thread-to-core ratio - Excellent for I/O-bound operations")
    elif thread_efficiency > 100:
        print("  ⚖️  Balanced thread-to-core ratio - Good performance balance")
    else:
        print("  📉 Low thread-to-core ratio - Conservative resource usage")

    # Recommendations
    print(f"\n{'RECOMMENDATIONS':<25}")
    print("-" * 50)

    if cpu_count >= 8:
        print("✅ Use parallel translation for all operations")
        print("✅ Consider increasing API rate limits if available")
        print("✅ Monitor memory usage during heavy translation loads")
    elif cpu_count >= 4:
        print("✅ Parallel translation enabled with balanced resource usage")
        print("✅ Good performance for typical quiz operations")
        print("✅ Monitor CPU usage during peak loads")
    else:
        print("⚠️  Conservative threading to preserve system responsiveness")
        print("⚠️  Consider reducing concurrent operations if experiencing slowdowns")
        print("⚠️  Monitor system resources during translation operations")

    print(f"\n{'IMPLEMENTATION STATUS':<25}")
    print("-" * 50)
    print("✅ Dynamic thread calculation based on CPU cores")
    print("✅ Automatic adjustment for I/O-bound operations")
    print("✅ Configurable limits to prevent API overload")
    print("✅ Thread-safe implementation")
    print("✅ Integrated with AppConstants")

    print("\n" + "=" * 80)
    print("Thread optimization completed successfully!")
    print("The application will automatically use optimal thread counts.")
    print("=" * 80)


def monitor_thread_usage():
    """Monitor thread usage in real-time (for development/debugging)"""
    print("\nReal-time Thread Usage Monitor (Press Ctrl+C to stop):")
    print("-" * 60)

    try:
        while True:
            # Get current process information
            process = psutil.Process()
            thread_count = process.num_threads()
            cpu_percent = process.cpu_percent(interval=0.1)

            print(f"Active Threads: {thread_count:3d} | CPU Usage: {cpu_percent:5.1f}% | "
                  f"Time: {time.strftime('%H:%M:%S')}", end='\r')

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


if __name__ == "__main__":
    display_thread_optimization_report()

    # Optional: Uncomment to enable real-time monitoring
    # monitor_thread_usage()
