import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="backupy",
    version="0.0.1",
    description="Simple python script for backing up directories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elesiuta/backupy",
    py_modules=['backu'],
    entry_points={
        'console_scripts': [
            'backupy = backu:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
