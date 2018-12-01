import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codesync",
    version="0.0.1",
    author="Edward Liu",
    author_email="edwardliu573@gmail.com",
    description="Sync code with a remote server in real time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yl573/codesync",
    entry_points={
        'console_scripts': ['codesync=codesync:main'],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
