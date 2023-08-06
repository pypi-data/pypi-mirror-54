from setuptools import find_packages, setup


setup(
    name='list-cli',
    version='0.0.1',
    url='https://github.com/jzaleski/list-cli',
    license='MIT',
    description='List CLI',
    author='Jonathan W. Zaleski',
    author_email='JonathanZaleski@gmail.com',
    packages=find_packages(),
    install_requires=[],
    entry_points={'console_scripts': ['list-cli=list.__main__:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
