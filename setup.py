from setuptools import setup, find_packages

setup(
    name='Straddle',
    version='0.1.1',
    author_email='xhd0216@gmail.com',
    url='https://github.com/xhd0216/straddle',
    packages=find_packages(),
    package_data={
      '':['*.json', '*.html']
    }
)
