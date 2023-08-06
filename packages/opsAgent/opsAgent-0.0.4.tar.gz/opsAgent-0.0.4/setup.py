import os

from setuptools import setup, find_packages

from src import opsAgent

this_directory = os.path.abspath(os.path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os.path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name=opsAgent.name,
    version=opsAgent.version,
    author="fanghongbo",
    author_email="718787573@qq.com",
    license='MIT',
    url="https://github.com/fanghongbo/opsAgent",
    description="Monitoring client based on OpsMgr",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    install_requires=read_requirements('requirements.txt'),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.5',

    entry_points={
        'console_scripts': [
            'opsAgent=opsAgent.bin.cli:main',
        ],
    },

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
