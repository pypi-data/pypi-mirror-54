from setuptools import setup, find_packages

setup(
    name='pacco',
    version='0.1.4',
    packages=find_packages(),
    author="Kevin Winata",
    author_email="kevinwinatamichael@gmail.com",
    description="A simple package manager (used for prebuilt binary), interoperable with Nexus repository manager",
    url="https://kwinata.github.io/pacco/",
    entry_points={
        'console_scripts': [
            'pacco=pacco.cli.entry_point:run'
        ]
    }
)
