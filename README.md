# Amplicon Coverage Inspector (aci)

Amplicon Coverage Inspector (aci) is a bioinformatics tool designed to analyze the depth of amplicons using samtools. It provides a convenient way to determine the coverage and depth of specified regions in a BAM file based on a BED file using a user-generated bedfile.

## Installation

```
pip install amplicon_coverage_inspector
```


### From github
```
git clone https://github.com/erinyoung/ACI.git
cd ACI
pip install .
```

## Dependencies
- python3.7+
  - pandas
  - matplotlib
  - pysam
  - intervaltree

## Usage
```
aci --bam input.bam --bed amplicon.bed --out out
```

Final files are 
- out/amplicon_depth.csv : csv file of the depth of each amplicon
- out/amplicon_depth.png : boxplot of information from csv file
- out/amplicon_depth_${sample}.bam.png : per-sample amplicon depth image with max and min
- out/amplicon_min_depth.csv : csv file for the minimum depth/unique depth of each amplicon
- out/amplicon_min_depth.png : boxplot of information from csv file
- out/overall_depth.csv  : csv file of overall depth of bam file
- out/${reference}_depth.png : overal depth accross reference from overall_depth.csv

<img src="https://github.com/erinyoung/ACI/blob/b0b2800bb8c738c964db4e9c084ea4164f5b2826/assets/aci.png" width="500"/>

There are not currently options to change the look of the final image file. Instead, the amplicon_depth.csv file contains all the values in a '.csv' format that can be read into R, python, excel, or another tool for visualization.

## Options
```
usage: aci [-h] -b BAM [BAM ...] -d BED [-o OUT] [-log LOGLEVEL] [-t THREADS] [-v]

options:
  -h, --help            show this help message and exit
  -b BAM [BAM ...], --bam BAM [BAM ...]
                        (required) input bam file(s)
  -d BED, --bed BED     (required) amplicon bedfile
  -o OUT, --out OUT     directory for results
  -log LOGLEVEL, --loglevel LOGLEVEL
                        logging level
  -t THREADS, --threads THREADS
                        specifies number of threads to use
  -v, --version         print version and exit
```

## Bed file format
ACI is not very strict on the [bed file format](https://en.wikipedia.org/wiki/BED_(file_format)) as only the first four columns are used.

The four columns (tab-delimited only) are 
1. Reference (must the same as the reference of the bam file)
2. Start position
3. Stop position
4. Name of the amplicon

ACI does not support bedfiles with headers.

Example amplicon bedfile.
```
MN908947.3	54	385	1	1	+
MN908947.3	342	704	2	2	+
MN908947.3	664	1004	3	1	+
MN908947.3	965	1312	4	2	+
MN908947.3	1264	1623	5	1	+
MN908947.3	1595	1942	6	2	+
MN908947.3	1897	2242	7	1	+
MN908947.3	2205	2568	8	2	+
MN908947.3	2529	2880	9	1	+
MN908947.3	2850	3183	10	2	+
```

## Amplicon bedfile

Primers should be trimmed out of the bam file prior to ACI regardless of whether the sequencing was paired or single-end. Primer sequences force portions of DNA to match reference and mask SNPs and other variants, so it is a normal request to trim primers out first.

Please be careful to not use a primer scheme bedfile because they are not the same. For an example, let's take a left and right primer based off of the reference MN908947.3. If left primer is expected to bind to 30-54 of MN908947.3, and the right primer is expected to bind to 385-410, the expected amplicon would be from 55-384.

ACI uses the user-provided amplicon bedfile to identify regions of the genome where both read1 and read2 are bounded by the start and stop location of that bedfile. If using a bam file generated with mapping single-end reads, only that one read must be within bounds. Any reads that map out of that specific region will be excluded. Then coverage is determined for that region. Therefore, all intended sequences are included. Nearby overlapping amplicons can still mask problematic primers/primer pairs and this should be taken into account when evaluating the output of ACI.

## Testing

This repository contains a test bam and bed file in the [/tests/data](./tests/data) subdirectory.

```
aci -b tests/data/test.bam -d tests/data/test.bed -o testing
```

The resulting image should look something like the following.
<img src="https://github.com/erinyoung/ACI/blob/b0b2800bb8c738c964db4e9c084ea4164f5b2826/assets/amplicon_depth.png" width="500"/>

# Expected run time

| file(s) | number of reads | threads | Elapsed (wall clock) time (h:mm:ss or m:ss) | Percent of CPU this job got | Maximum resident set size (kbytes) |
| :--------: | ------- | ------- | -------- | -------- | -------- |
| SRR28446008.primertrim.bam | 48777166 | 1 | 24:57.42 | 91% | 65642916 |
| SRR28446008.primertrim.bam | 48777166 | 2 | 17:34.11 | 141% | 41789232 |
| SRR28446008.primertrim.bam | 48777166 | 3 | 14:44.27 | 168% | 35364164 |
| SRR28446008.primertrim.bam | 48777166 | 4 | 11:40.18 | 218% | 24623868 |
| SRR28446008.primertrim.bam | 48777166 | 5 | 10:01.77 | 258% | 20829232 |
| SRR28446008.primertrim.bam | 48777166 | 6 | 10:35.90 | 252% | 22735132 |
| SRR28446008.primertrim.bam | 48777166 | 7 | 9:40.83 | 280% | 16731812 |
| SRR28446008.primertrim.bam | 48777166 | 8 | 8:30.76 | 325% | 16694240 |
| SRR28446008.primertrim.bam | 48777166 | 9 | 8:51.93 | 313% | 17393304 |
| SRR28446008.primertrim.bam | 48777166 | 10 | 7:41.89 | 374% | 12754412 |
| SRR28446008.primertrim.bam | 48777166 | 11 | 7:28.65 | 396% | 13153432 |
| SRR28446008.primertrim.bam | 48777166 | 12 | 7:03.99 | 401% | 13854976 |
| SRR28446008.primertrim.bam | 48777166 | 13 | 6:18.10 | 475% | 11594264 |
| SRR28446008.primertrim.bam | 48777166 | 14 | 6:13.00 | 486% | 12477736 |
| SRR28446008.primertrim.bam | 48777166 | 15 | 6:17.68 | 483% | 13362504 |
| SRR28446008.primertrim.bam | 48777166 | 16 | 6:02.38 | 503% | 14244760 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 1 | 3:29:22 | 90% | 94658408 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 2 | 2:10:49 | 156% | 58148124 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 3 | 1:37:32 | 214% | 56828032 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 4 | 1:24:22 | 252% | 56665120 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 5 | 1:14:18 | 303% | 57152076 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 6 | 1:07:54 | 336% | 57187576 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 7 | 1:00:55 | 378% | 57510668 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 8 | 57:55.42 | 409% | 57734304 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 9 | 54:34.33 | 425% | 65642916 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 10 | 53:24.72 | 456% | 57246404 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 11 | 54:16.05 | 468% | 58304164 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 12 | 51:31.58 | 496% | 58392632 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 13 | 49:36.17 | 522% | 58520260 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 14 | 49:06.47 | 532% | 59454204 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 15 | 49:32.36 | 552% | 59145092 |
| SRR28446008.primertrim.bam, SRR28446040.primertrim.bam, SRR28446049.primertrim.bam, SRR28446053.primertrim.bam, SRR28446063.primertrim.bam, SRR28446123.primertrim.bam, SRR28446153.primertrim.bam | 326156244 | 16 | 48:27.36 | 563% | 344725513 |



Larger genomes, more coverage, and larger amplicons increase the computation time. Use -t or --threads to take advantage of determining the coverage of amplicons in parallel.


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to [open an issue](https://github.com/erinyoung/ACI/issues) or submit a pull request.

## Why this exists

I just needed an individual tool that evaluates how effective a set of primers are for an amplicon or bait-based NGS library prep. Similar scripts are included in many workflows including that of (artic)[https://github.com/artic-network/artic-ncov2019], but I needed something that was standalone. Samtools has a function, [ampliconstats](http://www.htslib.org/doc/samtools-ampliconstats.html), that predicts amplicons based on a primer schema bedfile, but has errors when there are large number of primer pairs, the primer pairs overlap too much, are named outside of expected values, and can incorrectly pair primers when determining amplicons. This means that I needed control as to what was in the amplicon file.

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please [submit an issue](https://github.com/erinyoung/ACI/issues).
