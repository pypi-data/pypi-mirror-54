# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os import path as os_path
this_directory = os_path.abspath(os_path.dirname(__file__))
import time
# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='tseq2seq',
    version='0.1.0.1'+str(time.time()),
    description='tseq2seq',
    author='Terry Chan',
    author_email='napoler2008@gmail.com',
    url='https://github.com/napoler/tseq2seq',
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    install_requires=[
        'tqdm==4.36.1',
        'AutoBUlidVocabulary==0.1.0.11572302573.261918',
        'numpy==1.17.3',
        'requests==2.22.0',
        'torch==1.3.0',
        'torchvision==0.4.1',
    ],
    packages=['tseq2seq'])

"""
python3 setup.py sdist
python3 setup.py install
python3 setup.py sdist upload


"""
