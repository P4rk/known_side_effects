import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="known_side_effects",
    version="0.0.1",
    author="Luke Park",
    author_email="luke@p4rk.dev",
    description="A test utility library to help write explict side effects for mocked "
                "objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/P4rk/known_side_effects",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
    ],
    install_requires=[
        'PyHamcrest>=1.9.0',
    ],
)
