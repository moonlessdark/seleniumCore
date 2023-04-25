# 打包命令 python setup.py sdist

from setuptools import setup, find_packages
setup(
    name="seleniumCore",
    version="0.4",
    packages=find_packages(),
    # py_modules=['seleniumCore'],
    author='JiangY',
    install_requires=['docutils>=0.3', 'selenium', 'colorama', 'requests', 'webdriver-manager'],
    # metadata for upload to PyPI
    description="这是一个selenium二次封装",
    license="PSF",
    requires=['selenium', 'colorama', 'requests', 'webdriver_manager'],
)
