from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='dvtDecimal',
    version='1.4.0',
    description='Repeating digits of rational numbers',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://twitter.com/david_cobac',
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    keywords=['rational',
              'numbers',
              'fraction',
              'decimal',
              'nombres',
              'décimaux'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license='CC-BY-NC-SA',
    packages=find_packages()
)
