import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="protosync",
    version="0.0.2",
    author="Edward Liu",
    author_email="edwardliu573@gmail.com",
    description="Sync code with a remote server in real time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yl573/protosync",
    entry_points={
        'console_scripts': ['protosync=protosync:main'],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
