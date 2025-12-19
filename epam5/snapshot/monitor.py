"""
System monitoring logic.
"""
import time

import psutil


class SystemMonitor:
    """Collects system snapshots using psutil."""

    def __init__(self, interval=30, output_file="snapshot.json", quantity=20):
        self.interval = interval
        self.output_file = output_file
        self.quantity = quantity

    def collect_snapshot(self):
        """Collect a single system snapshot."""
        snapshot = {}
        snapshot["Tasks"] = self._get_tasks()
        snapshot["%CPU"] = self._get_cpu()
        snapshot["KiB Mem"] = self._get_memory()
        snapshot["KiB Swap"] = self._get_swap()
        snapshot["Timestamp"] = int(time.time())
        return snapshot

    def _get_tasks(self):
        """Get process/task statistics."""
        tasks = {
            "total": 0,
            "running": 0,
            "sleeping": 0,
            "stopped": 0,
            "zombie": 0
        }
        
        for proc in psutil.process_iter():
            try:
                tasks["total"] += 1
                status = proc.status()
                
                if status == psutil.STATUS_RUNNING:
                    tasks["running"] += 1
                elif status in (psutil.STATUS_SLEEPING, psutil.STATUS_DISK_SLEEP):
                    tasks["sleeping"] += 1
                elif status == psutil.STATUS_STOPPED:
                    tasks["stopped"] += 1
                elif status == psutil.STATUS_ZOMBIE:
                    tasks["zombie"] += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return tasks

    def _get_cpu(self):
        """Get CPU usage percentages."""
        cpu_times = psutil.cpu_times_percent(interval=0.1)
        return {
            "user": round(cpu_times.user, 1),
            "system": round(cpu_times.system, 1),
            "idle": round(cpu_times.idle, 1)
        }

    def _get_memory(self):
        """Get memory usage in KiB."""
        mem = psutil.virtual_memory()
        return {
            "total": mem.total // 1024,
            "free": mem.free // 1024,
            "used": mem.used // 1024
        }

    def _get_swap(self):
        """Get swap usage in KiB."""
        swap = psutil.swap_memory()
        return {
            "total": swap.total // 1024,
            "free": swap.free // 1024,
            "used": swap.used // 1024
        }