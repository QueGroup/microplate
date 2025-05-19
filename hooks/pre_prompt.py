import subprocess
import sys


def is_docker_installed() -> bool:
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except Exception as ex:
        print(f"ERROR: docker is not installed: {ex}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if not is_docker_installed():
        sys.exit(1)
