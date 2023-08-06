
from setuptools import setup, find_packages

VERSION = '1.1'

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='bhvideoconverter',
    version=VERSION,
    description='convert any video format to any format :).!',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='BandarHelal',
    author_email='bandarhelal180@gmail.com',
    url='https://github.com/BandarHL/BHVideoConverter',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'bhvideoconverter': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        bhvideoconverter = bhvideoconverter.main:main
    """,
)
