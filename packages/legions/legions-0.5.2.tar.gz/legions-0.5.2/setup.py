from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()


setup(name='legions',
      version='0.5.2',
      description='Handy toolkit for (security) researchers poking around Ethereum nodes and contracts, now with a slick command-line interface, with auto complete commands and history.',
      long_description=readme,
      long_description_content_type="text/markdown",  
      url='https://github.com/shayanb/Legions',
      author='Shayan Eskandari - ConsenSys Diligence',
      author_email='shayan.eskandari@consensys.net',
      license='MIT',
      packages=['legions'],
      package_data={
          'legions': ['commands/**'],
      },
      install_requires=[
          'python-nubia',
          'jellyfish',
          'prettytable',
          'prompt-toolkit',
          'Pygments',
          'pyparsing',
          'termcolor',
          'wcwidth',
          'web3>=5.1.0'
          #'requests',
      ],    

      entry_points='''
          [console_scripts]
          legions=legions.main:main
      ''',
      zip_safe=False)