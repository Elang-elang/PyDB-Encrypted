from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyDB-Encrypted',
    version="1.1.5",
    author='Elang-elang',
    author_email='elangmuhammad888@gmail.com',  # Ganti dengan email Anda
    description='A simple, efficient, and encrypted Python database library for secure data storage',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Elang-elang/PyDB-Encrypted',  # Ganti dengan URL repository Anda
    project_urls={
        'Bug Tracker': 'https://github.com/Elang-elang/PyDB-Encrypted/issues',
        'Documentation': 'https://github.com/Elang-elang/PyDB-Encrypted#readme',
        'Source Code': 'https://github.com/Elang-elang/PyDB-Encrypted',
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    keywords='database, encryption, json, lightweight, embedded-database, python-database, encrypted-storage',
    python_requires='>=3.7',
    install_requires=[
        'cryptography>=41.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license='MIT',
)
