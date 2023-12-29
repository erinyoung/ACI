import pytest
import subprocess

def run_command(cmd):
    stdout=subprocess.PIPE
    stderr=subprocess.PIPE
    
    proc = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
    out, err = proc.communicate()
    
    if proc.returncode != 0:
        raise RuntimeError(f"FAILED: {cmd}\n{err}")

def test_aci():
    """test aci"""    
    cmd = "aci -b tests/data/test.bam -d tests/data/test.bed -o tests -t 1"
    run_command(cmd)

def test_version():
    """test aci"""    
    cmd = "aci -v"
    run_command(cmd)

def test_help():
    """test aci"""    
    cmd = "aci -h"
    run_command(cmd)

# TODO : Finish unit testing
# # initialize list of lists
# data = [['tom', 10], ['nick', 15], ['juli', 14]]
# 
# Create the pandas DataFrame
# df = pd.DataFrame(data, columns=['Name', 'Age'])

#def test_amplicon_depth():
#    meta = {}
#    meta['subregion_bed'] = 'tests/data/test.bed'
#    meta['filename'] = 'test.bed'
#    meta['sorted_bam'] = 'tests/data/test.bam'
#    amplicon_depth(meta, region)

#def test_get_regions():   
#    get_regions(bed)

# def test_plotting_amplicons():
#     plotting_amplicons(df, out)

# def test_split_dataframe():
#     split_dataframe(df)

# def test_column_names():
#     column_names(bed)    

# def test_group_create():
#     group_create(positions)

# def test_plotting_boxplot():
#     plotting_boxplot(df, d)   

# def test_subregion():
#     subregion(region, bed)

# def test_genome_depth():
#     genome_depth(meta)  

# def test_group_mean():
#     group_mean(df, name)  

# def test_plotting_depth():
#     plotting_depth(df, out)    

# def test_within():
#     within(initial_bam, final_bam, subregion)

# def test_get_coverage():
#     get_coverage(meta, region)   

# def test_prep():
#     prep(initial, final, threads)

# def test_without():
#     without(initial, unmatched, matched, bed)
