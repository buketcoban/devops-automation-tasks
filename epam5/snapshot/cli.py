# snapshot/cli.py
import argparse
import json
import os
import time

from snapshot.monitor import SystemMonitor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Interval between snapshots in seconds",
                        type=int, default=30)
    parser.add_argument("-f", help="Output file name", default="snapshot.json")
    parser.add_argument("-n", help="Quantity of snapshot to output",
                        type=int, default=20)

    args = parser.parse_args()

    monitor = SystemMonitor(
        interval=args.i,
        output_file=args.f,
        quantity=args.n
    )

    with open(args.f, "w") as f:
        pass

    for _ in range(args.n):
        snapshot = monitor.collect_snapshot()

        os.system('clear')
        print(snapshot, end="\r")

        with open(args.f, "a") as f:
            json.dump(snapshot, f)
            f.write("\n")

        time.sleep(args.i)


if __name__ == "__main__":
    main()