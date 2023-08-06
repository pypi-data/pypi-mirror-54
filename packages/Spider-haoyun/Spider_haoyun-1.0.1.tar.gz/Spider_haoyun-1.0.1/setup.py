# -*- coding: utf-8 -*-
# @Time    : 2019/10/31 16:31
# @Author  : longwenzhang
# @Email   : mat_wu@163.com
# @File    : setup.py
# @Software: PyCharm
from setuptools import setup

setup(name='Spider_haoyun',
      version='1.0.1',
      description='spider utils',
      author='haoyun',
      author_email='1469779169@qq.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='ga nn',
      project_urls={
            'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
            'Funding': 'https://donate.pypi.org',
            'Source': 'https://github.com/pypa/sampleproject/',
            'Tracker': 'https://github.com/pypa/sampleproject/issues',
      },
      packages=['Spider_haoyun'],
      install_requires=['happybase>=1.1.0', 'scrapy>=1.6.0','pymongo>=3.7.2','pypinyin>=0.35.3'],
      python_requires='>=3'
     )
