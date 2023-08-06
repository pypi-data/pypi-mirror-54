# coding: utf-8
from setuptools import setup
import os


README = os.path.join(os.path.dirname(__file__), 'README.rst')
REQUIREMENTS = os.path.join(os.path.dirname(__file__), 'requirements.txt')


if __name__ == "__main__":
    setup(name='csvconv',
          description='Convert csv from one dialect to another.',
          version='1.0',
          long_description=open(README).read(),
          author="Henrique Bastos", author_email="henrique@bastos.net",
          license="MIT",
          url='http://github.com/henriquebastos/csvconv/',
          keywords=['csv', 'converter', 'dialect', 'cli'],
          install_requires=open(REQUIREMENTS).readlines(),
          packages=['csvconv'],
          package_dir={"csvconv": "csvconv"},
          entry_points={
              'console_scripts': [
                  'csvconv = csvconv.__main__:main',
              ]
          },
          zip_safe=False,
          platforms='any',
          include_package_data=True,
          classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Console',
              'License :: OSI Approved :: MIT License',
              'Natural Language :: Portuguese (Brazilian)',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3 :: Only',
              'Topic :: Utilities',
          ])
