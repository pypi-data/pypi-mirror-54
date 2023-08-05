#!/usr/bin/env python

from setuptools import setup

setup(
    name='WTForms-SQLAlchemy-mlenzen',
    version='0.2',
    url='http://github.com/mlenzen/wtforms-sqlalchemy/',
    license='BSD',
    author='Thomas Johansson, James Crasta, Michael Lenzen',
    author_email='m.lenzen@gmail.com',
    description='SQLAlchemy tools for WTForms',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=[
        'wtforms_sqlalchemy',
    ],
    package_data={
    },
    test_suite='tests.tests',
    install_requires=['WTForms>=1.0.5', 'SQLAlchemy>=0.7.10'],
)
