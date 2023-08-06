import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="cft",
    version="1.0.17",
    description="codeforces command line tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="granddaifuku",
    author_email="grandnadaifuku@gmail.com",
    packages=setuptools.find_packages(),
    package_data={
        "": ["main*"]
    },
    entry_points={
        "console_scripts": [
            "cft = src.cft:main"
        ]
    },
    install_requirements=[
        "shutil", "requests"
    ],
    platforms="any",
    license='MIT'
)
