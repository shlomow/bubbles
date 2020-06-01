from setuptools import setup, find_packages

with open('requirements-install.txt', 'r') as f:
    install_requires = f.readlines()

setup(
    name='bubbles',
    version='0.1.0',
    author='Shlomi Vaknin',
    description='Brain Computer Interface',
    packages=find_packages(),
    package_dir={'bubbles': 'bubbles'},
    package_data={'bubbles': ['gui/templates/*']},
    install_requires=install_requires,
    tests_require=['pytest', 'pytest-cov'],
)
