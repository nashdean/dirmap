from setuptools import setup, find_packages

setup(
    name='dirmapper',
    version='1.0.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'dirmap=main:main',
        ],
    },
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    include_package_data=True,
    description="A CLI tool to generate a directory structure mapping.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Nash Dean",
    author_email="nashdean.github@gmail.com",
    url="https://github.com/nashdean/dirmap",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
