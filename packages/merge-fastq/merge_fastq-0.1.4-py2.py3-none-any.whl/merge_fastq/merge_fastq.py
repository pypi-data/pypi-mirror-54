# -*- coding: utf-8 -*-

import os
import logging
import shutil

"""
merge_fastq
~~~~~~~~~~~~~~~
:Description: main module for merge_fastq
"""
"""
Created on October 21, 2019
Description: main module for merge_fastq
@author: Ronak H Shah
"""

# Making logging possible
logger = logging.getLogger("merge_fastq")


def run(fastq1, fastq2, output_path, out_fastq1, out_fastq2):
    out_file1 = os.path.join(output_path, out_fastq1)
    out_file2 = os.path.join(output_path, out_fastq2)
    if(len(fastq1) == len(fastq2)):
        if len(fastq1) == 1:
            try:
                shutil.copyfile(fastq1[0], out_file1)
            except IOError as e:
                logging.error(
                    "Could not copy file %s to %s, please see the execution error. \n %s \n", fastq1[0], out_file1, e)
                exit(1)
            try:
                shutil.copyfile(fastq2[0], out_file2)
            except IOError as e:
                logging.error(
                    "Could not copy file %s to %s, please see the execution error. \n %s \n", fastq2[0], out_file2, e)
                exit(1)
        else:
            merge_fastq(fastq1, fastq2, out_file1, out_file2)
            logging.info("Done merging fastq file in %s and %s", out_file1, out_file2)

    else:
        logger.error("The program expects that the same number of fastq are provided for READ1 and READ2, current they dont match. \n\n ### READ1 ### \n %s \n ### READ2 ### \n %s \n", fastq1, fastq2)
        exit(1)


def merge_fastq(fastq_list_R1, fastq_list_R2, out_file1, out_file2):
    with open(out_file1, 'wb') as outfile:
        for fastq in fastq_list_R1:
            with open(fastq, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)
    with open(out_file2, 'wb') as outfile:
        for fastq in fastq_list_R2:
            with open(fastq, 'rb') as infile:
                shutil.copyfileobj(infile, outfile)
