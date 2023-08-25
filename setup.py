from setuptools import setup, find_packages

setup(
    name="square_logger",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "square_logger": ["data/*"],
    },
    install_requires=[],
    author="thePmSquare",
    author_email="thepmsquare@thepmsquare.com",
    description="FastAPI application, meant to be used for encoding and decoding messages in images i.e. steganography.",
    url="https://github.com/thepmsquare/square_logger",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
