from setuptools import setup


setup(
    name='PieLedger',
    version='1.0.2',
    setup_requires=['setuptools-git'],
    packages=['pieledger'],
    include_package_data=True,
    install_requires=[
        'click==6.7',
        'grpcio==1.12.1',
        'protobuf>=3.5.2',
        'piecash==0.18.0',
        'PyMySQL==0.8.0',
        'PyYAML==3.12',
        'requests==2.18.4',
        'raven==6.8.0',
        'MapperPy==0.11.1py34',
        'backoff==1.5.0'
    ],
    dependency_links=[
        'git+http://dev.smart4e.com/cohirer/mapperpy.git@v0.11.1py34#egg=MapperPy-0.11.1py34'  #noqa
    ],
    entry_points='''
        [console_scripts]
        pieledger=pieledger.manager:manager
    '''
)
