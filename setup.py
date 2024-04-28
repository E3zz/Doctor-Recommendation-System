from setuptools import setup, find_packages

# Read the dependencies from requirements.txt
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='app',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)