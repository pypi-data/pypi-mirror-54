from setuptools import setup

with open('/wherever/README.md') as f:
    long_description = f.read()

setup(
  name = 'dolittle-timeseries-runtime-contracts',
  packages = ['dolittle-timeseries-runtime-contracts'],
  version = '1.0.2',
  license='MIT',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Dolittle',
  author_email = 'post@dolittle.com',
  url = 'https://github.com/dolittle-timeseries/contracts.runtime',
  keywords = ['Dolittle', 'gRPC', 'Contracts'],
  install_requires=[
    'protobuf3'
  ],
  python_requires='>=3.3',
  classifiers=[
    'Intended Audience :: Developers',      
    'License :: OSI Approved :: MIT License'
  ]
)