from setuptools import setup
from mixnn.__version__ import version

setup(
      name='mix-nn',
      version='0.1',
      description='High-Level API to train kears NN',
      url='http://github.com/pmerienne/mix-nn',
      download_url=f'https://github.com/pmerienne/datalab-utils/archive/{version}.tar.gz',
      author='Pierre Merienne',
      license='Apache License, Version 2.0',
      packages=['mixnn'],
      package_data={
            'mixnn.datasets': ['titanic.csv']
      },
      install_requires=[
            'keras>=2.2.4',
            'Pillow>=6.0.0',
            'scikit-learn>=0.20.3'
      ],
      zip_safe=False
)

# TODO: optional dependencies: pandas, livelossplot