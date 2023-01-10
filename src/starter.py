#!/usr/bin/python3
import subprocess  # lib pour lancer des process(=docker)

from loguru import logger  # lib pour logger des trucs
import sys

logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> | <level>{level}</level> | <level>{message}</level>",
)


# To Do:
# Run black before pushing to github repo, everytime! => formatting
# Run flake8 before pushing to github repo, everytime! => formatting


def menu(choices):
    i = 1
    for choice in choices:
        print(f"[{i}] {choice}")
        i += 1
    # rajouter un try/except pour le int()
    index = int(input(">> "))
    return choices[index - 1]


def main():
    os = menu(["Linux", "Windows"])
    if os == "Linux":
        exploit = menu(["CVE-2021-44228"])  # Add more exploits here

        logger.info("Launching vulnerable environment...")

        if exploit == "CVE-2021-44228":
            # This will need to changed to a local Dockerfile (git clone this: https://github.com/christophetd/log4shell-vulnerable-app and
            # docker run -f ./vuln/CVE-2021-44228/Dockerfile
            subprocess.call(
                "docker run --name CVE-2021-44228 -dp 8080:8080 ghcr.io/christophetd/log4shell-vulnerable-app@sha256:6f88430688108e512f7405ac3c73d47f5c370780b94182854ea2cddc6bd59929",
                shell=True,
            )
            # Pas sur que ce github soit bon, j'ai eu pas mal de probleme pour le faire marcher :/

            logger.info("The vulnerable environment is available on port 8080")


if __name__ == "__main__":
    main()
