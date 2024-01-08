# Amplicon Coverage Inspector (aci)

Amplicon Coverage Inspector (aci) is a bioinformatics tool designed to analyze the depth of amplicons using samtools. It provides a convenient way to determine the coverage and depth of specified regions in a BAM file based on a BED file.

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

## Usage
```
aci --bam input.bam --bed amplicon.bed --out out
```

Final files are 
- out/amplicon_depth.csv : csv file of the depth of each amplicon
- out/amplicon_depth.png : boxplot of information from csv file
- out/overall_depth.csv  : csv file of overall depth of bam file
- out/overall_depth.png  : boxplot of information from csv file

Expected run time:
About 30 seconds per amplicon when using SRR13957125 (SARS-CoV-2 with ~30 KB genome size and 5,350.27 mean depth) and the artic V3 primers. Larger genomes, more coverage, and larger amplicons increase the computation time. Use -t or --threads to take advantage of determining the coverage of amplicons in parallel.


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

ACI uses the bedfile to identify regions of the genome where both read1 and read2 are bounded by the start and stop location of that bedfile. If using a bam file generated with mapping single-end reads, only that one read must be within bounds. Any reads that map out of that specific region will be excluded. Then coverage is determined for that region. Therefore, all intended sequences are included. Nearby overlapping amplicons can still mask problematic primers/primer pairs and this should be taken into account when evaluating the output of ACI.

<!---
## Target vs. bait bedfile (To Be Added - please submit an issue if this feature interests you)

ACI can also be used to evaluate baits for NGS library preparation methods that involve capture reagents. In general, the same principles apply. I recommend using a bait file as opposed to a target region file, but I can't actually stop you.

Baits need to allow for portions of sequence outside of the region of interest. It is not unfeasable that read1 maps prior and read2 maps downstream of a bait region if the insert size is large enough. The goal is that every sequence attached to that bait should be included, so reads that have **any** indication of being captured by a specific bait will be included. This does mean that neighboring baits can increase the coverage of a region and may mask poor baits and this should be taken into account when evaluating the output of ACI. Single-end reads are only included if they map to the bait region.
---> 

## Testing

This repository contains a test bam and bed file in the [/tests/data](./tests/data) subdirectory.

```
aci -b tests/data/test.bam -d tests/data/test.bed -o testing
```

The resulting image should look something like the following.
<img src="https://github.com/erinyoung/ACI/blob/b0b2800bb8c738c964db4e9c084ea4164f5b2826/assets/amplicon_depth.png" width="500"/>


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to [open an issue](https://github.com/erinyoung/ACI/issues) or submit a pull request.

## Why this exists

I just needed an individual tool that evaluates how effective a set of primers are for an amplicon or bait-based NGS library prep. Similar scripts are included in many workflows including that of (artic)[https://github.com/artic-network/artic-ncov2019], but I needed something that was standalone. Samtools has a function, [ampliconstats](http://www.htslib.org/doc/samtools-ampliconstats.html), that predicts amplicons based on a primer schema bedfile, but has errors when there are large number of primer pairs and can incorrectly pair primers when determining amplicons. This means that I needed control as to what was in the amplicon file.

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please [submit an issue](https://github.com/erinyoung/ACI/issues).
