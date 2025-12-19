"""
Make snapshot

{"Tasks": {"total": 440, "running": 1, "sleeping": 354, "stopped": 1, "zombie": 0},
"%CPU": {"user": 14.4, "system": 2.2, "idle": 82.7},
"KiB Mem": {"total": 16280636, "free": 335140, "used": 11621308},
"KiB Swap": {"total": 16280636, "free": 335140, "used": 11621308},
"Timestamp": 1624400255}
"""
import argparse
import json
import os
import time

from .monitor import SystemMonitor


def main():
    """Snapshot tool."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        help="Interval between snapshots in seconds",
        type=int,
        default=30,
    )
    parser.add_argument(
        "-f",
        help="Output file name",
        default="snapshot.json",
    )
    parser.add_argument(
        "-n",
        help="Quantity of snapshot to output",
        type=int,
        default=20,
    )
    args = parser.parse_args()

    monitor = SystemMonitor(
        interval=args.i,
        output_file=args.f,
        quantity=args.n,
    )

    # file truncate at start
    open(monitor.output_file, "w", encoding="utf-8").close()

    for _ in range(monitor.quantity):
        snapshot = monitor.collect_snapshot()

        os.system("clear")
        print(snapshot, end="\r")

        with open(monitor.output_file, "a", encoding="utf-8") as file:
            json.dump(snapshot, file)
            file.write("\n")

        time.sleep(monitor.interval)


if __name__ == "__main__":
    main()
