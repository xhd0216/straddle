from setuptools import setup, find_packages

setup(
    name='Straddle',
    version='0.3.5',
    author_email='xhd0216@gmail.com',
    url='https://github.com/xhd0216/straddle',
    packages=find_packages(),
    package_data={
      '':['*.json', '*.html', '*.R', '*.cnf', '*.sh', '*.txt']
    },
    entry_points={
      'console_scripts': [
        'getEarningCalendar = straddle.zacks_parser:main',
        'getStrategy = straddle.get_strategy:main',
        'uploadOptionsPrices = straddle.upload_options_prices:main',
      ]
    },
    install_requires=[
      'argparse',
      'MySQL-python',
      'python-dateutil',
      'sqlalchemy',
      'testing.mysqld',
    ]
)
