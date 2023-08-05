from setuptools import setup, find_packages

setup(
    name='wf-database-connection-honeycomb',
    packages=find_packages(),
    version='0.1.0',
    include_package_data=True,
    description='An implementation of the database_connection API using Wildflower\'s Honeycomb database',
    long_description=open('README.md').read(),
    url='https://github.com/WildflowerSchools/database_connection_honeycomb',
    author='Theodore Quinn',
    author_email='ted.quinn@wildflowerschools.org',
    install_requires=[
        'wf-database-connection>=0.1.0'
        'wildflower-honeycomb-sdk>=0.7.2',
        'python-dateutil>=2.8.0'
    ],
    keywords=['database'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
