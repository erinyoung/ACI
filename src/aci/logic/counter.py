import pysam
import logging
from collections import defaultdict
from intervaltree import IntervalTree

def build_amplicon_index(amplicons):
    trees = defaultdict(IntervalTree)
    for amp in amplicons:
        trees[amp['chrom']].addi(amp['start'], amp['end'], amp['name'])
    return trees

def get_contained_amplicons(read, tree):
    """Returns set of amplicons STRICTLY containing the read."""
    valid_amplicons = set()
    hits = tree.overlap(read.reference_start, read.reference_end)
    for interval in hits:
        # Strict Check: Read must be inside amplicon
        if read.reference_start >= interval.begin and read.reference_end <= interval.end:
            valid_amplicons.add(interval.data)
    return valid_amplicons

def count_amplicons_in_bam(bam_path, amplicons):
    sample_name = bam_path.split("/")[-1]
    
    max_counts = defaultdict(int)
    min_counts = defaultdict(int)
    
    # New: List to store every read assignment
    read_assignments = [] 

    for amp in amplicons:
        max_counts[amp['name']] = 0
        min_counts[amp['name']] = 0

    try:
        trees = build_amplicon_index(amplicons)
        
        with pysam.AlignmentFile(bam_path, "rb") as bam:
            read_cache = {}

            for read in bam:
                if read.is_unmapped or read.is_secondary or read.is_supplementary:
                    continue
                
                qname = read.query_name
                
                if qname not in read_cache:
                    read_cache[qname] = read
                else:
                    r1 = read_cache.pop(qname)
                    r2 = read
                    
                    if r1.reference_name != r2.reference_name:
                        continue
                    
                    chrom = r1.reference_name
                    if chrom not in trees:
                        continue

                    tree = trees[chrom]

                    # 1. Get containment for both reads
                    r1_amps = get_contained_amplicons(r1, tree)
                    if not r1_amps: continue
                    
                    r2_amps = get_contained_amplicons(r2, tree)
                    if not r2_amps: continue

                    # 2. Intersection (Pair must be in same amplicon)
                    valid_set = r1_amps.intersection(r2_amps)
                    
                    if not valid_set:
                        continue

                    # 3. Assign Counts & Track Names
                    for amp_name in valid_set:
                        max_counts[amp_name] += 1
                        
                        # DEBUG: Record that this read belongs to this amplicon
                        read_assignments.append({
                            'bam': sample_name,
                            'amplicon': amp_name,
                            'read_name': qname
                        })
                        
                    if len(valid_set) == 1:
                        unique_amp = list(valid_set)[0]
                        min_counts[unique_amp] += 1

    except Exception as e:
        logging.error(f"Error processing {sample_name}: {e}")
        return [], []

    # Format Summary
    final_output = []
    for amp_name in max_counts:
        final_output.append({
            'bam': sample_name,
            'amplicon': amp_name,
            'max_count': max_counts[amp_name],
            'min_count': min_counts[amp_name]
        })
        
    # Return TWO things: The counts, and the raw read list
    return final_output, read_assignments