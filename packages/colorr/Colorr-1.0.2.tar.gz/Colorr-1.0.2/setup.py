import setuptools

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Colorr",
    version="1.0.2",
    author="ItzAfroBoy",
    author_email="spareafro@post.com",
    description="A tool for picking Colorrs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ItzAfroBoy/colorr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)