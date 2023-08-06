from setuptools import setup,find_packages

setup(
    name='tf-cloud-api',
    version='0.0.1',
    description='Script for interact with the tf cloud api',
    url='https://github.com/redaptiveinc/tf-cloud-api',
    author='Mariano Gimenez',
    author_email='mariano.gimenez@redaptiveinc.com',
    license='unlicense',
    zip_safe=False,
    packages = find_packages(),
    entry_points ={
        'console_scripts': [
            'tf-output = src.getTFOutput:main'
        ]
    },
    install_requires = [
        'requests==2.20.0',
        'pyhcl==0.3.12'
    ]
)
