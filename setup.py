import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wurtzisms",
    version="1.1.1",
    author="Daniel Andersson",
    author_email="wurtz@muthur6000.se",
    description="print wurtzism in your shell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/splump/wurtzisms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'wurtzisms = wurtzisms.__main__:main'
        ]
    },
    install_requires=[
        'beautifulsoup4~=4.6',  # 4.6 or later, below major version 5
        'requests~=2.19'  # 2.19 or later, below major version 3
    ]
)
