from setuptools import setup, find_packages

setup(
    name='PieLedger',
    version='1.0.0',
    setup_requires=['setuptools-git'],
    packages=find_packages(exclude=['tests.*', 'test']),
    include_package_data=True,
    py_modules=['manager']
)
