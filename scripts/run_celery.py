import os
import subprocess
import sys
import time


def stop_processes(processes: list[subprocess.Popen[bytes]]) -> None:
    for process in processes:
        if process.poll() is None:
            process.terminate()

    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def main() -> int:
    worker_command = [
        sys.executable,
        "-m",
        "celery",
        "-A",
        "config",
        "worker",
        "--loglevel=INFO",
    ]
    if os.name == "nt":
        worker_command.extend(["--pool=solo"])

    beat_command = [
        sys.executable,
        "-m",
        "celery",
        "-A",
        "config",
        "beat",
        "--scheduler",
        "celery.beat:Scheduler",
        "--loglevel=INFO",
    ]

    processes = []
    try:
        print("Starting Celery worker...", flush=True)
        processes.append(subprocess.Popen(worker_command))
        print("Starting Celery Beat...", flush=True)
        processes.append(subprocess.Popen(beat_command))

        while all(process.poll() is None for process in processes):
            time.sleep(0.25)

        return next(
            (process.returncode for process in processes if process.returncode not in (None, 0)),
            1,
        )
    except KeyboardInterrupt:
        return 0
    finally:
        stop_processes(processes)


if __name__ == "__main__":
    raise SystemExit(main())