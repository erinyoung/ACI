from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='amplicon_coverage_inspector',
    version='1.0.20231222',
    author='Erin Young',
    author_email='eriny@utah.gov',
    url="https://github.com/erinyoung/ACI",
    description='Visualization of coverage for amplicon sequencing',
    long_description=long_description,
    long_description_content_type="text/markdown", 
    packages=find_packages(include=['aci', 'aci.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta ',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Bio-Informatics '
        ],
    keywords = [
        "bioinformatics",
        "amplicon",
        "coverage",
        "visualization",
    ],
    python_requires=">=3.7, <4",
    install_requires=[
        "pandas>=2.1.4",
        "pysam>=0.22.0",
        "matplotlib>=3.8.2",
        "numpy>=1.26.2",
    ],
    entry_points={
        'console_scripts': [
            'aci=aci.aci:main'
            ],
    },
)