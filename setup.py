#!/usr/bin/env python
 
from setuptools import setup, find_packages
 
setup(
    name='django-libertyreserve',
    version='0.1',
    description='A pluggable Django application for integrating LibertyReserve',
    author='George S. Parker',
    author_email='George.Safford.Parker@gmail.com',
    url='http://github.com/GeorgeSParker/django-libertyreserve',
    license='MIT License',
    classifiers=[
      'Framework :: Django',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python',
    ],
    packages=find_packages(),
    zip_safe=False,
)
