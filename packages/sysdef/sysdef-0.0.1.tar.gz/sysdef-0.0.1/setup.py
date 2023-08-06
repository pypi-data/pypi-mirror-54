import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sysdef",
    version="0.0.1",
    author="Geoff Williams",
    author_email="geoff@declarativesystems.com",
    description="sysdef bootable image and configuration management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geoffwilliams/sysdef",
    packages=setuptools.find_packages(),
    # pick from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)

