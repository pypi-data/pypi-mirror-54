import setuptools
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

with open(str(Path("BWFM").joinpath("version.txt")), "r", encoding="utf-8") as v:
    version = v.read()

setuptools.setup(
    name="BWFM",
    version=version,
    author="kreny",
    author_email="kronerm9@gmail.com",
    description="Simple Qt front-end for botwfstools management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/23kreny/BWFM",
    include_package_data=True,
    packages=["BWFM"],
    entry_points={
        'gui_scripts': [
            'bwfm = BWFM.__init__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PySide2 >= 5.13.1",
        "botwfstools >= 1.4.3",
    ]
)
