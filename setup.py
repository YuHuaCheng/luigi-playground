import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    install_requires = f.read().splitlines()

test_requires = [
]

setup(
    name='LuigiPlayground',
    version='0.0.1',
    description="Anything you need to play with to understand Luigi's dark magic",
    author='Yu Hua Cheng',
    author_email='yuhua.nyc@gmail.com',
    url='https://github.com/YuHuaCheng/LuigiPlayground',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=test_requires
)
