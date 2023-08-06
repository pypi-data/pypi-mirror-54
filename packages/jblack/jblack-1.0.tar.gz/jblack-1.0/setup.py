import setuptools


with open("jblack/README.md", "r") as f:
    long_description = f.read()
short_description = long_description.split("\n")[1].replace("\\", "")


setuptools.setup(
    name="jblack",
    version="1.0",
    scripts=["jblack/jblack"],
    author="QuentinN42",
    author_email="jupyter.black@gmail.com",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jupyter-black/jblack",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"jblack": ["arguments.json"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
