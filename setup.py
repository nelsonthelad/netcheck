from setuptools import setup, find_packages

setup(
    name="netcheck",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "speedtest-cli",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "netcheck=netcheck.main:cli",
        ],
    },
    author="Nelson Daniels",
    author_email="nelsongdaniels@gmail.com",
    description="A shell command for network speed and information",
    keywords="network, speed test, CLI",
    url="https://github.com/nelsonthelad/netcheck",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
) 