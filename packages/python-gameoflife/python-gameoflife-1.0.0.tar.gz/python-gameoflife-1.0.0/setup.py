from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="python-gameoflife",
    version="1.0.0",
    description="python implementation for Conway's game of life",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/itsmehdi97/GameofLife",
    author="itsmehdi97",
    author_email="itsmehdi97@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["python_gameoflife"],
    include_package_data=True,
    install_requires=["pygame"],
    entry_points={
        "console_scripts": [
            "python-gameoflife=python_gameoflife.main:main",
        ]
    }
)