import io
from setuptools import setup

GITHUB_URL = 'https://github.com/cheshirekow/sphinx-codefence'

VERSION = None
with io.open('sphinx_codefence.py', encoding='utf-8') as infile:
  for line in infile:
    line = line.strip()
    if line.startswith('VERSION ='):
      VERSION = line.split('=', 1)[1].strip().strip('"')
assert VERSION is not None

with io.open('README.rst', encoding='utf-8') as infile:
  long_description = infile.read()

setup(
    name='sphinx-codefence',
    py_modules=["sphinx_codefence"],
    version=VERSION,
    description=\
        "Sphinx extension to monkeypatch docutils with a codefence parser",
    long_description=long_description,
    author='Josh Bialkowski',
    author_email='josh.bialkowski@gmail.com',
    url=GITHUB_URL,
    download_url='{}/archive/{}.tar.gz'.format(GITHUB_URL, VERSION),
    keywords=['sphinx'],
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    include_package_data=True,
    install_requires=[]
)
