from setuptools import setup

with open("README.md") as file:
    long_description = file.read()

setup(
    name="goethe",
    version="1.0.0",
    author="mxschll",
    author_email="mail@mxschll.com",
    packages=["goethe"],
    description="Python interpreter for the Goethe programming language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mxschll/goethe",
    keywords="esoteric goethe interpreter",
    install_requires=[
        'Pyphen',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Interpreters",
    ],
    python_requires=">= 3.8",
    entry_points={
        "console_scripts": ["goethe=goethe.__main__:main"]
    },
)
