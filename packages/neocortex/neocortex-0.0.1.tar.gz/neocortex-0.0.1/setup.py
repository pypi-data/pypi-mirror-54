from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="neocortex",
    version="0.0.1",
    author="Tyler Banks",
    author_email="tbanks@mail.missouri.edu",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tjbanks/neocortex",
    download_url='',
    license='MIT',
    install_requires=[
        'click-plugins',
        'clint',
        'configparser',
        'flask',
        'flask-sqlalchemy',
        'flask-restful',
        'flask-migrate',
        'flask-jwt-extended',
        'tornado==4.5.2',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'python-dotenv',
        'passlib',
        'questionary',
        'tox',
        'twython',
        'webargs',
        'py2neo',
        'neo4j-driver',
        'flask-neo4j4'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Operating System :: OS Independent"
    ],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'neocortex = neocortex.cli.manage:cli',
            'neo = neocortex.cli.manage:cli',
            'neo-api-server = neocortex.manage:cli'
        ]
    }
)
