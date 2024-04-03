from setuptools import setup, find_packages

setup(
    name='libcovulor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'pymongo==4.6.2'
    ],
    author='Plexicus',
    author_email='info@plexicus.com',
    description='CRUD in mongo database.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/plexicus/libcovulor',
)
