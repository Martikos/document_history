import os
from setuptools import setup

def get_packages():
    packages = []
    for root, dirnames, filenames in os.walk('document_history'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

required_modules = ['mongoengine', 'blinker']

setup(name='document_history',
      version='0.1',
      description='MongoEngine Document Versionning for Humans',
      url='https://github.com/Martikos/document_history',
      author='Marc Adam',
      author_email='marc.m.adam@gmail.com',
      install_requires=required_modules,
      license='MIT',
      packages=get_packages(),
      zip_safe=False,
      tests_require=['nose'],
      test_suite='nose.collector',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          ]
      )
