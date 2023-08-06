import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bagpipe",
    version="0.0.1",
    author="Nicolas Landier",
    author_email="nicolas.landier@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/landier/bagpipe",
    packages=setuptools.find_packages(),
    install_requires=["sanic"],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['bagpipe=bagpipe.main:main'],
    }
)
