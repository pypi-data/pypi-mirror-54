from setuptools import setup

setup(name='techela',
      version='3.2.6',
      description='Utilities for techela.',
      url='http://github.com/jkitchin/techela',
      author='John Kitchin',
      author_email='jkitchin@andrew.cmu.edu',
      license='GPL',
      platforms=[],
      packages=['techela'],
      scripts=['techela/bin/techela',
               'techela/bin/techela-el'],
      include_package_data=True,
      long_description='''A python version of techela''',
      install_requires=['Flask'],)

# to put up a new version
# (shell-command "python setup.py sdist upload")
