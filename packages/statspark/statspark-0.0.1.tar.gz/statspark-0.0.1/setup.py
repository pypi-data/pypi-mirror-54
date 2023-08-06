import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="statspark",
    version="0.0.1",
    author="Junkyu Park",
    author_email="joon3216@gmail.com",
    description="Functions for statistical analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joon3216/statspark",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'matplotlib', 'numpy', 'pandas', 'patsy', 
        'scipy', 'sklearn', 'statsmodels'
    ],
    license="MIT License",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
