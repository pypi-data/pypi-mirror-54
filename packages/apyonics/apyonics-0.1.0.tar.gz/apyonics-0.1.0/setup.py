from setuptools import setup, find_packages

setup(name='apyonics',
    version='0.1.0',
    author='AIONICS',
    author_email='austin@aionics.io',
    description='Client for interacting with AIONICS APIs',
    long_description=open('README.rst','r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lensonp/apyonics',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.5'
)

