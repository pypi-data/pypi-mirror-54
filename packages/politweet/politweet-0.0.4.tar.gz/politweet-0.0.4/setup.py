import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="politweet",
    version="0.0.4",
    author="Danail Krzhalovski",
    author_email="dkrzhalovski@gmail.com",
    description="library for processing italian political tweets",
    packages=setuptools.find_packages(),
    install_requires = required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
