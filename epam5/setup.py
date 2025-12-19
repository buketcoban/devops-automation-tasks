from setuptools import setup, find_packages

setup(
    name="snapshot",
    version="0.1.0",
    description="System monitoring snapshot utility using psutil",
    author="EPAM",
    packages=find_packages(),
    install_requires=["psutil"],
    entry_points={
        "console_scripts": [
            "snapshot=snapshot.cli:main",
        ],
    },
    python_requires=">=3.6",
)