#!/usr/bin/env python3.11
"""Kill then start front and back ends"""
import logging
import subprocess
import sys
import time


def main():
    """Run front and backends until killed with stop argument"""
    logging.info("Killing old processes")
    print(subprocess.run(["pkill", "-f", "discord"], check=False))
    print(subprocess.run(["pkill", "-f", "django"], check=False))

    time.sleep(2)
    if "stop" in sys.argv:
        return
    logging.info("Starting new processes")
    path = "/usr/local/bin:/opt/homebrew/bin/"
    subprocess.Popen(["/usr/bin/env", "-P", path, "poetry", "run", "discord"], shell=False)
    subprocess.Popen(
        ["/usr/bin/env", "-P", path, "poetry", "run", "django"],
        shell=False,
        stdin=subprocess.DEVNULL,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
