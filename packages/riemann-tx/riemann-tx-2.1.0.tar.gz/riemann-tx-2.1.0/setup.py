# flake8: noqa

from setuptools import setup, find_packages

setup(
    name='riemann-tx',
    version='2.1.0',
    description=('Transaction creation library for Bitcoin-like coins'),
    url='https://github.com/summa-tx/riemann',
    author='James Prestwich',
    author_email='james@summa.one',
    install_requires=[],
    packages=find_packages(),
    package_dir={'riemann': 'riemann'},
    package_data={'riemann': ['py.typed']},
    keywords = 'bitcoin litecoin cryptocurrency decred blockchain development',
    python_requires='>=3.6',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security :: Cryptography',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
