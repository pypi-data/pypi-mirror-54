from setuptools import setup, find_packages

VERSION = '1.1.5'
PACKAGES = find_packages()
# ['ciplog']

setup(name='ciplog',
      version=VERSION,
      description='TCIP logging class.',
      author='Adriano Canofre',
      author_email='adrianoknofre@gmail.com',
      license='MIT',
      packages=PACKAGES,
      install_requires=[],
      zip_safe=False)
