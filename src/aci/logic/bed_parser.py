import logging
import sys

def parse_bed(bed_path):
    """Parses a 4-column BED file into a list of dictionaries."""
    amplicons = []
    try:
        with open(bed_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue
                amplicons.append({
                    'chrom': parts[0],
                    'start': int(parts[1]),
                    'end': int(parts[2]),
                    'name': parts[3]
                })
    except Exception as e:
        logging.critical(f"Failed to parse BED file: {e}")
        sys.exit(1)
    return amplicons