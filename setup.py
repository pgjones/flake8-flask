import os

from setuptools import setup

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PROJECT_ROOT, 'flake8_flask.py')) as file_:
    version_line = [line for line in file_ if line.startswith('__version__')][0]

__version__ = version_line.split('=')[1].strip().strip("'").strip('"')

with open(os.path.join(PROJECT_ROOT, 'README.md')) as file_:
    long_description = file_.read()

setup(
    name='flake8_flask',
    version=__version__,
    description='Flake8 plugin that checks Flask code against opinionated style rules',
    long_description=long_description,
    url='https://github.com/pgjones/flake8-flask',
    author='P G Jones',
    author_email='philip.graham.jones@googlemail.com',
    keywords=[
        'flake8',
        'plugin',
        'flask',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Flake8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
    py_modules=['flake8_flask'],
    install_requires=[
        'flake8',
        'setuptools',
    ],
    entry_points={
        'flake8.extension': [
            'F4 = flake8_flask:Linter',
        ],
    },
    zip_safe=False,
)
