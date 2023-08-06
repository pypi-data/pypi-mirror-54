import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hausmon_client",
    version="0.0.4",
    author="Louis Calitz",
    author_email="louis@hausnet.io",
    description="A client for the HausMon monitoring service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liber-tas/hausmon-client",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['bravado']
)
