from setuptools import setup, find_packages

setup(
  name='dyndns',
  version='0.1.0',
  description='Library and cli tool for manipulating dyn dns.',
  packages = ['dyndns'],
  author = 'Stephen Wood',
  author_email = 'smwood4@gmail.com',
  scripts = ['dyncli'],
  install_requires = [
    'argparse==1.2.1',
    'requests==2.3.0'
  ]
)
