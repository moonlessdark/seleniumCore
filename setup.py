# python setup.py sdist

from setuptools import setup, find_packages
setup(
    name="seleniumCore",
    version="0.1",
    packages=find_packages(),
    # py_modules=['seleniumCore'],
    author='JiangY',
    install_requires=['docutils>=0.3', 'selenium'],

    # metadata for upload to PyPI
    description="这是一个selenium二次封装",
    license="PSF",
    requires=['selenium'],
)