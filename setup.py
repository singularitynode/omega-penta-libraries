from setuptools import setup, find_packages

setup(
    name="omega-penta-libraries",
    version="1.0.0",
    author="singularitynode",
    author_email="noreply@users.noreply.github.com",
    description="Enterprise-Grade Distributed Systems Libraries for Python — Omega Penta Libraries",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/singularitynode/omega-penta-libraries",
    packages=find_packages(),
    install_requires=[
        "asyncio",
        "redis",
        "pyjwt",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.9",
)
