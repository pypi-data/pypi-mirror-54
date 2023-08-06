import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parktoma-vscconan",
    version="1.0.1",
    author="Parker Tomatoes",
    author_email="parker.tomatoes@gmail.com",
    description="Utility to update Visual Studio Code C++ Tools include paths from a conanfile",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parkertomatoes/parktoma-vscconan",
    packages=setuptools.find_namespace_packages(include=['parktoma.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools"
    ],
    python_requires='>=3.5',
)