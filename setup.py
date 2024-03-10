from setuptools import setup, find_packages

setup(
    name="square_logger",
    version="1.0.5",
    packages=find_packages(),
    package_data={
        "square_logger": ["data/*"],
    },
    install_requires=["lapa_commons>=0.0.1"],
    author="thePmSquare, Amish Palkar",
    author_email="thepmsquare@gmail.com, amishpalkar302001@gmail.com",
    description="python logger for my personal use.",
    url="https://github.com/thepmsquare/square_logger",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
