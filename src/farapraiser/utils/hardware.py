"""Hardware detection utilities."""

import psutil
import platform
from typing import Dict, Optional


class HardwareDetector:
    """Detect system hardware capabilities."""
    
    @staticmethod
    def get_system_info() -> Dict[str, any]:
        """Get comprehensive system information."""
        return {
            "platform": platform.system(),
            "processor": platform.processor(),
            "ram_gb": psutil.virtual_memory().total / (1024**3),
            "cpu_count": psutil.cpu_count(logical=False),
            "cpu_threads": psutil.cpu_count(logical=True),
        }
    
    @staticmethod
    def has_gpu() -> bool:
        """Check if system has GPU (basic check)."""
        try:
            # Check for NVIDIA GPU
            import subprocess
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 and result.stdout.strip()
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Could add checks for AMD/Intel GPUs here
        return False
    
    @staticmethod
    def recommend_model() -> str:
        """Recommend an appropriate LLM model based on hardware."""
        info = HardwareDetector.get_system_info()
        ram_gb = info["ram_gb"]
        has_gpu = HardwareDetector.has_gpu()
        
        if has_gpu and ram_gb >= 16:
            return "llama2:13b"  # Larger model for powerful systems
        elif ram_gb >= 8:
            return "llama2:7b"  # Medium model
        elif ram_gb >= 4:
            return "phi"  # Smaller, efficient model
        else:
            return "tinyllama"  # Minimal model for low-end systems
    
    @staticmethod
    def get_optimal_threads() -> int:
        """Get optimal number of threads for LLM inference."""
        cpu_count = psutil.cpu_count(logical=False) or 1
        # Use physical cores, leave some headroom
        return max(1, cpu_count - 1)
