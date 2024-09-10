from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="terminai",
    version="0.1.0",
    author="Pablo Misirov",
    author_email="carebymedia@gmail.com",
    description="A terminal-based AI assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/misirov/terminAI",
    packages=find_packages(),
    package_data={
        'terminai': ['../.env'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ai=terminai.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Unix",
    ],
    python_requires=">=3.6",
)