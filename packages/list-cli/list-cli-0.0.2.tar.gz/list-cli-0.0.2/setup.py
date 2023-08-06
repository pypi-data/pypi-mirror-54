from ast import literal_eval as ast_literal_eval
from re import compile as re_compile
from setuptools import find_packages, setup


PKG_NAME = 'list-cli'


_version_re = re_compile(r'__version__\s+=\s+(.*)')
with open('list/cli.py'.format(PKG_NAME), 'rb') as f:
    version = str(ast_literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name=PKG_NAME,
    version=version,
    url='https://github.com/jzaleski/list-cli',
    license='MIT',
    description='List Management Application (CLI)',
    author='Jonathan W. Zaleski',
    author_email='JonathanZaleski@gmail.com',
    packages=find_packages(),
    install_requires=[],
    entry_points={'console_scripts': ['list-cli=list.__main__:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
    ],
)
