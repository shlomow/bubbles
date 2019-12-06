from setuptools import setup, find_packages


setup(
    name = 'bubbles',
    version = '0.1.0',
    author = 'Shlomi Vaknin',
    description = 'Brain Computer Interface',
    packages = find_packages(),
    install_requires = ['click'],
    tests_require = ['pytest', 'pytest-cov'],
)