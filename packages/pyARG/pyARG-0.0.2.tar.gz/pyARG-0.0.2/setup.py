import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyARG",
    version="0.0.2",
    author="NexGen Analytics",
    author_email="info@ng-analytics.com",
    description="This repo contains the needed Python dependencies for ARG. Version 0.0.2 contains a dependency update for matplotlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7,<3',
    install_requires=[requirements]
)
