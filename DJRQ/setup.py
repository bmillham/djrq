from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='djrq',
      version=version,
      description="Request Site For DJs",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Brian Millham',
      author_email='brian@millham.net',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
                        'Mako',
                        'Beaker',
                        'humanize', # for human numbers
                        'flup',
                        'sqlalchemy',
                        'oursql', # May need libmysqlclient-dev to install oursql
      ],
      entry_points="""
        
      """,
      paster_plugins = ['PasteScript', 'WebCore'],
      )
