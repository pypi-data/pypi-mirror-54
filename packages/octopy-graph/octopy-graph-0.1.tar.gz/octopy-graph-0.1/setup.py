import os
import setuptools

# Crete new tag & update download url & version
# Run:
# venv\Scripts\python.exe setup.py sdist bdist_wheel
# venv\Scripts\twine.exe upload dist/*

if not os.environ.get("CI_COMMIT_TAG"):
    exit()

version = os.environ["CI_COMMIT_TAG"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="octopy-graph",
    packages=["octopy_graph"],
    version=version,
    license="MIT",
    description="A tool for graphing data from the Octopus Energy API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["octopy-graph=octopy_graph.__main__:main"]},
    author="Samuel Broster",
    author_email="s.h.broster@gmail.com",
    url="https://gitlab.com/broster/octopy-graph",
    keywords=["Octopus Energy", "plotly", "graph"],
    install_requires=["plotly", "octopy-api", "numpy"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
)
