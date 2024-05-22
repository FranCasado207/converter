from setuptools import setup, find_packages

setup(
    name='converter',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
    'console_scripts': [
        'converter = converter:main',
    ],
    }
)