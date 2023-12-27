from setuptools import setup, find_packages

setup(
    name='aci',
    version='1.0.20231222',
    author='Erin Young',
    author_email='eriny@utah.gov',
    description='Visualization of coverage for amplicon sequencing',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)