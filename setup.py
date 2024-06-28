from setuptools import setup, find_packages

setup(
    name='dirmap',
    version='1.0.0',
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
    author="Nash Dean",
    author_email="nashdean.github@gmail.com",
    url="https://github.com/nashdean/dirmap",
)
