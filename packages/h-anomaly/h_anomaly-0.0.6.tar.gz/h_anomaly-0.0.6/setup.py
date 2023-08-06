import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="h_anomaly",
        version="0.0.6",
        author="RAISE_LAB",
        author_email="smajumd3@ncsu.edu",
        description="A small example package Anomaly detection using hierarchical clustering, anomaly detector, classifiers and fast model rebuilding",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ai-se/h_anomaly",
        packages=setuptools.find_packages(),
        install_requires=[
            'freediscovery[core]',
            'seaborn',
            'pandas',
            'numpy',
            'scipy',
            'matplotlib'
        ],
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )