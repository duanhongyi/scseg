import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
# need install xapian-binding-python
scripts = ['scripts/learn']
requires = [
    'nose',
    'chardet',
    ]

setup(name='scseg',
      version='1.1',
      description='a python chinese seg word',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='duanhongyi',
      author_email='duanhyi@gmail.com',
      url='https://bitbucket.org/duanhongyi/scseg/get/tip.zip',
      keywords='Chinese Word Segmentation',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      scripts = scripts,
      platforms = 'all platform',
      license = 'BSD',
      homepage = 'https://bitbucket.org/duanhongyi/scseg/get',
      )

