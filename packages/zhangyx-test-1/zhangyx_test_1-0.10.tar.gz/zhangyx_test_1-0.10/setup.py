from setuptools import setup, find_packages

setup(
    name="zhangyx_test_1",
    version="0.10",
    description="My test module",
    author="Zhang Yexing",
    url="http://www.csdn.net",
    license="LGPL",
    packages= find_packages(),
    scripts=["scripts/test.py"],
)
