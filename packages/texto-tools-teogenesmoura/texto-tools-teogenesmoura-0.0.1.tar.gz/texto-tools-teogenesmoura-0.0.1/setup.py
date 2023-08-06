import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="texto-tools-teogenesmoura", # Replace with your own username
    version="0.0.1",
    author="Teógenes Moura",
    author_email="teogenes.moura@camara.leg.br",
    description="A small text-processing package for content analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/labhackercd/textoTools.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)