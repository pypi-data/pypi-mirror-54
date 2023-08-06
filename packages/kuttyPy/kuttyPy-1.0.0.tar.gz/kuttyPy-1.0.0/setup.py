import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="kuttyPy",
    version="1.0.0",
    install_requires=requirements,
    author="Jithin B.P",
    author_email="jithinbp@gmail.com",
    description="Python Library for KuttyPy AVR trainer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/csparkresearch/kuttypy-gui",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Education',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = 'atmega32 trainer data-acquisition',
    python_requires='>=3.4',
    project_urls={  # Optional
        'Source': 'https://github.com/csparkresearch/kuttypy-gui',
        'Read The Docs': 'https://kuttypy.readthedocs.io',
        'Buy Hardware': 'https://csparkresearch.in/kuttypy',
    },
)
