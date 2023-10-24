#!/usr/bin/env python3
import logging
import os
import pandas
import pysam


def aci_depth(df, bam, region, single, out):
    """Function for getting the depth of an amplicon

    :param df: Pandas dataframe
    :type df: dataframe
    :param bam: Input file
    :type bam: str
    :param region: Region to get coverage for
    :type region: str
    :param single: Specifies if single-end
    :type single: bool
    :param out: Final directory
    :type out: str

    
    """

    logging.debug('Made it to checkpoint 0 for ' + bam)
    ref        = region.split(':')[0]
    start      = int(region.split(':')[1])
    end        = int(region.split(':')[2])
    name       = region.split(':')[3]
    subregion  = ref + ':' + str(start) + '-' + str(end)
    file_name  = os.path.basename(bam)

    bed1 = out + '/tmp.' + name + '.'   + file_name + '.bed'
    bam0 = out + '/tmp.' + file_name
    bam1 = out + '/tmp.' + name + '.1.' + file_name
    bam2 = out + '/tmp.' + name + '.2.' + file_name
    bam3 = out + '/tmp.' + name + '.3.' + file_name
    bam4 = out + '/tmp.' + name + '.4.' + file_name
    logging.debug('temp filenames are ' + bed1 + ', ' + bam0 + ', ' + bam1 + ', ' + bam2 + ', ' + bam3 + ', and ' + bam4 )
    logging.debug('Made it to checkpoint 1 for ' + bam + ' and ' + region)

    if start <= 1:
        with open(bed1, mode='wt') as file:
            file.write(ref + '\t' + str(end + 1) + '\t50000000\n')
    else:
        with open(bed1, mode='wt') as file:
            file.write(ref + '\t' + str('0') + '\t' + str(start - 1) + '\n' + ref + '\t' + str(end + 1) + '\t5000000\n')

    # running samtools via pysam   
    if os.path.exists(bam0):
        logging.debug('Made it to checkpoint 2 for ' + bam + ' and ' + region)
        single_check = int(pysam.view('-c', '-f',  '1', bam0))
        if single_check == 0 and not single :
            single = True
            logging.warning(bam + ' is single end')

        logging.debug('Made it to checkpoint 3 for ' + bam + ' and ' + region)
        if single:
            pysam.view('-bh', '-o', bam1, bam0, subregion, catch_stdout=False)    
        else:
            pysam.view('-bh','-f2', '-o', bam1, bam0, subregion, catch_stdout=False)
    
    if os.path.exists(bam1):
        logging.debug('Made it to checkpoint 4 for ' + bam + ' and ' + region)
        pysam.index(bam1)
        pysam.view('-bh', bam1, '-U', bam2, '-o', bam3, '-L', bed1, catch_stdout=False)
        os.remove(bam1)
        os.remove(bam1 + '.bai')
    
    logging.debug('Made it to checkpoint 5 for ' + bam + ' and ' + region)
    os.remove(bed1)

    if os.path.exists(bam2):
        logging.debug('Made it to checkpoint 6 for ' + bam + ' and ' + region)
        pysam.index(bam2)
        if single:
            pysam.view('-bh', '-o', bam4, bam2, subregion, catch_stdout=False)    
        else:
            pysam.view('-bh', '-f2', '-o', bam4, bam2, subregion, catch_stdout=False)
        os.remove(bam2)
        os.remove(bam2 + '.bai')
        os.remove(bam3)

    if os.path.exists(bam4):
        logging.debug('Made it to checkpoint 7 for ' + bam + ' and ' + region)
        pysam.index(bam4)
        cov=float(pysam.coverage('--no-header', bam4, '-r', subregion).split()[6]) 
        os.remove(bam4)
        os.remove(bam4 + '.bai')  
    else:
        cov=0

    logging.debug('Made it to checkpoint 8 for ' + bam + ' and ' + region)
    bamindex = df.index[df['bam'] == bam]
    df.loc[bamindex, [name]] = cov

    return(df)