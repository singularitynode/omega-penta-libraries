from setuptools import setup, find_packages

setup(
    name="omega-penta-libraries",
    version="1.0.0",
    author="singularitynode",
    author_email="dev@protonmail.com",
    description="Enterprise-grade distributed systems libraries for Python — Circuit Breaking, Sharding, Query Caching, and more.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/singularitynode/omega-penta-libraries",
    packages=find_packages(exclude=("tests", "examples")),
    python_requires=">=3.9",
    install_requires=[
        "redis>=5.0.0",
        "asyncio",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
)
