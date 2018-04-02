from setuptools import setup, find_packages

setup(
    name='Straddle',
    version='0.2.2',
    author_email='xhd0216@gmail.com',
    url='https://github.com/xhd0216/straddle',
    packages=find_packages(),
    package_data={
      '':['*.json', '*.html']
    },
    entry_points={
      'console_scripts': [
        'getOptionsPrices = straddle.market_watcher_parser:main',
        'getEarningCalendar = straddle.zacks_parser:main',
        'getStrategy = straddle.get_strategy:main'
      ]
    },
    install_requires=[
      'argparse',
      'mysql-python',
      'sqlalchemy',
    ]
)
