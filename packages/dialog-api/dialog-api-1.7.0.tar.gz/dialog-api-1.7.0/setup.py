import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dialog-api",
    version="v1.7.0",
    author="Dialog LLC",
    author_email="services@dlg.im",
    description="Dialog API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dialogs/api-schema",
    packages=setuptools.find_packages(),
    license='Apache License 2.0',
    keywords='dialog messenger',
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
