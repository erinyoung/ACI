from setuptools import setup, find_packages

setup(
    name='aci',
    version='0.1.20230815',
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