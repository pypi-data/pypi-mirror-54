# -*-coding:utf-8 -*-
# @Time : 2019/10/30 0030 上午 10:42
# @Author : huangjie
# @File : setup.py

from distutils.core import setup

setup(
    name='firstmodule',
    version='1.0',
    description = '这是第一个对外发布的模块，测试喽',
    author = 'huangjie',
    author_email = 'h0419j@163.com',
    py_modules = ['firstmodule.add','firstmodule.multiple']
)