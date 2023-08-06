#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='investpy',
    version='0.9.8',
    packages=find_packages(),
    url='https://investpy.readthedocs.io/',
    download_url='https://github.com/alvarob96/investpy/archive/0.9.8.tar.gz',
    license='MIT License',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='investpy — a Python package for financial historical data extraction from Investing',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=[
        'Unidecode>=1.1.1',
        'pandas>=0.25.1',
        'lxml>=4.4.1',
        'setuptools>=41.2.0',
        'requests>=2.22.0',
        'numpy==1.17.2'
    ],
    data_files=[
        ('stocks', [
            'investpy/resources/stocks/stocks.csv',
            'investpy/resources/stocks/stock_countries.csv'
        ]),
        ('funds', [
            'investpy/resources/funds/funds.csv',
            'investpy/resources/funds/fund_countries.csv'
        ]),
        ('etfs', [
            'investpy/resources/etfs/etfs.csv',
            'investpy/resources/etfs/etf_countries.csv'
        ]),
        ('indices', [
            'investpy/resources/indices/indices.csv',
            'investpy/resources/indices/index_countries.csv',
            'investpy/resources/indices/global_indices_countries.csv',
        ]),
        ('currency_crosses', [
            'investpy/resources/currency_crosses/currency_crosses.csv',
            'investpy/resources/currency_crosses/currency_cross_continents.csv'
        ]),
        ('bonds', [
            'investpy/resources/bonds/bonds.csv',
            'investpy/resources/bonds/bond_countries.csv'
        ]),
        ('user_agents', [
            'investpy/resources/user_agent_list.txt'
        ])
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    keywords='investing, investing-api, historical-data, financial-data, stocks, funds, etfs, indices',
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://github.com/alvarob96/investpy/issues',
        'Source': 'https://github.com/alvarob96/investpy',
        'Documentation': 'https://investpy.readthedocs.io/'
    },
)
