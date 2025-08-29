#!/usr/bin/env python3
"""
thread_utils.py - Utilities for optimal thread pool sizing

This module provides functions to calculate the optimal number of threads
for parallel operations based on available CPU cores and system resources.
"""

import os
import multiprocessing
from typing import Optional


class ThreadPoolOptimizer:
    """
    Calculates optimal thread pool sizes based on system resources.

    This class provides methods to determine the best number of threads
    for different types of operations (I/O-bound vs CPU-bound).
    """

    @staticmethod
    def get_cpu_count() -> int:
        """
        Get the number of available CPU cores.

        Returns:
            int: Number of CPU cores available on the system
        """
        try:
            # Use multiprocessing.cpu_count() which is more reliable
            cpu_count = multiprocessing.cpu_count()
            if cpu_count is None:
                # Fallback to os.cpu_count()
                cpu_count = os.cpu_count()
            return cpu_count if cpu_count else 4  # Default fallback
        except Exception:
            return 4  # Safe default

    @staticmethod
    def calculate_optimal_threads(
        operation_type: str = "io_bound",
        multiplier: Optional[float] = None,
        max_threads: Optional[int] = None
    ) -> int:
        """
        Calculate optimal number of threads for parallel operations.

        Args:
            operation_type: Type of operation ("io_bound", "cpu_bound", "mixed")
            multiplier: Custom multiplier for thread calculation (optional)
            max_threads: Maximum number of threads to allow (optional)

        Returns:
            int: Optimal number of threads for the operation
        """
        cpu_count = ThreadPoolOptimizer.get_cpu_count()

        if operation_type == "cpu_bound":
            # For CPU-bound operations, don't exceed core count
            optimal = cpu_count
        elif operation_type == "io_bound":
            # For I/O-bound operations, can use more threads
            if multiplier:
                optimal = int(cpu_count * multiplier)
            else:
                # Empirical formula: core_count * 2, but not more than core_count + 4
                optimal = min(cpu_count * 2, cpu_count + 4)
        elif operation_type == "mixed":
            # For mixed operations, use 1.5x core count
            optimal = int(cpu_count * 1.5)
        else:
            # Default to I/O-bound calculation
            optimal = min(cpu_count * 2, cpu_count + 4)

        # Apply maximum limit if specified
        if max_threads:
            optimal = min(optimal, max_threads)

        # Ensure minimum of 2 threads for parallel processing
        optimal = max(optimal, 2)

        return optimal

    @staticmethod
    def get_translation_threads() -> int:
        """
        Get optimal number of threads for translation operations.

        Translation operations are I/O-bound due to API calls,
        so we can use more threads than CPU cores.

        Returns:
            int: Optimal number of threads for translations
        """
        return ThreadPoolOptimizer.calculate_optimal_threads(
            operation_type="io_bound",
            max_threads=16  # Cap at 16 threads to avoid overwhelming APIs
        )

    @staticmethod
    def get_api_request_threads() -> int:
        """
        Get optimal number of threads for API requests.

        API requests are network I/O-bound, so we can be more aggressive
        with thread count, but need to be respectful to avoid rate limiting.

        Returns:
            int: Optimal number of threads for API requests
        """
        return ThreadPoolOptimizer.calculate_optimal_threads(
            operation_type="io_bound",
            multiplier=1.5,  # More conservative for API calls
            max_threads=12   # Lower cap for API politeness
        )

    @staticmethod
    def get_system_info() -> dict:
        """
        Get system information for debugging and monitoring.

        Returns:
            dict: System information including CPU count and optimal thread counts
        """
        cpu_count = ThreadPoolOptimizer.get_cpu_count()

        return {
            "cpu_count": cpu_count,
            "translation_threads": ThreadPoolOptimizer.get_translation_threads(),
            "api_request_threads": ThreadPoolOptimizer.get_api_request_threads(),
            "system_type": "I/O-bound optimized"
        }


def get_optimal_thread_count(operation_type: str = "translation") -> int:
    """
    Convenience function to get optimal thread count.

    Args:
        operation_type: Type of operation ("translation", "api", "general")

    Returns:
        int: Optimal number of threads
    """
    if operation_type == "translation":
        return ThreadPoolOptimizer.get_translation_threads()
    elif operation_type == "api":
        return ThreadPoolOptimizer.get_api_request_threads()
    else:
        return ThreadPoolOptimizer.calculate_optimal_threads("io_bound")


# Global instance for easy access
thread_optimizer = ThreadPoolOptimizer()
