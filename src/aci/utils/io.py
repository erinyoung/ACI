import os
import pysam
import logging

def check_bam_status(bam_path):
    """
    Checks if a BAM is coordinate-sorted and has an index.
    Returns: (is_sorted, has_index)
    """
    is_sorted = False
    has_index = False
    
    # Check Index (.bai or .crai)
    if os.path.exists(bam_path + ".bai") or os.path.exists(bam_path + ".crai"):
        has_index = True
    elif os.path.exists(os.path.splitext(bam_path)[0] + ".bai"):
        has_index = True
        
    # Check Sort Order in Header
    try:
        with pysam.AlignmentFile(bam_path, "rb") as f:
            if f.header.get('HD', {}).get('SO') == 'coordinate':
                is_sorted = True
    except Exception:
        # If we can't read the header, assume it's broken/not sorted
        pass
        
    return is_sorted, has_index

def prep(initial_bam, temp_bam_path, threads):
    """
    Prepares a BAM for analysis.
    - If original is sorted+indexed, returns original path (Zero I/O).
    - If not, sorts/indexes into the temp_bam_path and returns that.
    """
    is_sorted, has_index = check_bam_status(initial_bam)
    
    # CASE 1: Ready to go!
    if is_sorted and has_index:
        logging.info(f"Using existing sorted/indexed BAM: {initial_bam}")
        return initial_bam

    # CASE 2: Needs work (Sort and Index)
    logging.info(f"Sorting/Indexing required. creating temp file: {temp_bam_path}")
    
    # Sort
    pysam.sort("-o", temp_bam_path, "-@", str(threads), initial_bam)
    
    # Index
    pysam.index(temp_bam_path)
    
    return temp_bam_path