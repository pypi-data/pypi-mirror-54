import setuptools
## Uncomment and modify if you have a Github Repo for your package

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="stackfuelpippip", #change to your package name
    version="0.0.1", #musst be changed at every upload
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)