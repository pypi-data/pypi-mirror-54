# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 22:57
# @Author  : floatsliang
# @File    : setup.py
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='neo4japi',
    version=__import__('neo4japi').__version__,
    description='A simple neo4j api driver',
    packages=find_packages(exclude=['test']),
    url='https://github.com/floatliang/neo4japi',
    author='floatsliang',
    author_email='utavianus@qq.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='neo4j driver api',
    install_requires=[
        'neo4j == 1.7.2',
        'neobolt == 1.7.9',
        'six >= 1.10.0'
    ],
    zip_safe=False,
    platforms=['any'],
)
