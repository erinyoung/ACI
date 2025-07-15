def divide_chrom_by_span(bed_trees, threads):
    """ Devide bedfile into chunks to chunk bams """
    regions = []
    for chrom, tree in bed_trees.items():
        starts = [iv.begin for iv in tree]
        ends = [iv.end for iv in tree]

        chrom_start = min(starts)
        chrom_end = max(ends)
        total_span = chrom_end - chrom_start
        chunk_size = (total_span + threads - 1) // threads

        end = chrom_start
        while end < chrom_end:
            start = end
            end = start + chunk_size
            regions.append(f"{chrom}:{str(start)}:{str(end)}")

    return regions
