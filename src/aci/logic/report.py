import os
import pandas as pd
import numpy as np
import logging

def calculate_gini(array):
    """
    Calculates Gini coefficient of a numpy array.
    0 = Perfect Equality (All amplicons have same depth)
    1 = Perfect Inequality (One amplicon has all depth)
    """
    array = np.array(array, dtype=float)
    if np.amin(array) < 0:
        return 0 # Do not handle negative values
    
    array += 0.0000001 # Avoid div by zero
    array = np.sort(array)
    index = np.arange(1, array.shape[0] + 1)
    n = array.shape[0]
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

def generate_dropout_report(min_df, out_dir, threshold=10, failure_cutoff=0.5):
    """
    Generates a TSV summary of amplicons that consistently fail.
    Format: Amplicon <tab> Failure_Rate_Percent <tab> Median_Depth
    """
    # Prepare data: Ensure 'bam' is index so we only look at amplicon columns
    if 'bam' in min_df.columns:
        data = min_df.set_index('bam')
    else:
        data = min_df

    total_samples = len(data)
    report_path = os.path.join(out_dir, "dropout_report.tsv")
    
    try:
        with open(report_path, "w") as f:
            # Write TSV Header
            f.write("Amplicon\tFailure_Rate_Percent\tMedian_Depth\n")
            
            systematic_failures = []
            
            for amplicon in data.columns:
                depths = data[amplicon]
                
                # Calculate stats
                fail_count = (depths < threshold).sum()
                fail_rate = fail_count / total_samples
                median_depth = depths.median()
                
                # Only report if it exceeds the failure cutoff
                if fail_rate > failure_cutoff:
                    systematic_failures.append((amplicon, fail_rate, median_depth))

            # Sort by failure rate (descending)
            systematic_failures.sort(key=lambda x: x[1], reverse=True)
            
            # Write Data Rows
            if systematic_failures:
                for amp, rate, med in systematic_failures:
                    f.write(f"{amp}\t{rate*100:.2f}\t{med:.2f}\n")
            else:
                pass # Empty file with header implies no systematic failures
                
        logging.info(f"Dropout report generated: {report_path}")

    except Exception as e:
        logging.error(f"Failed to write dropout report: {e}")

def generate_masking_beds(min_df, amplicons_list, out_dir, threshold=10):
    """
    Creates a BED file for EACH sample listing regions with coverage < threshold.
    """
    # Create Map: Amplicon Name -> (Chrom, Start, End)
    amp_map = {a['name']: (a['chrom'], a['start'], a['end']) for a in amplicons_list}
    
    mask_dir = os.path.join(out_dir, "masking_files")
    os.makedirs(mask_dir, exist_ok=True)
    
    count = 0
    try:
        # Iterate rows (samples)
        iterator = min_df.iterrows()
        
        for _, row in iterator:
            sample_name = row['bam']
            mask_file = os.path.join(mask_dir, f"{sample_name}_mask.bed")
            
            with open(mask_file, "w") as f:
                for amp_name, depth in row.items():
                    if amp_name == 'bam': continue
                    
                    if depth < threshold:
                        coords = amp_map.get(amp_name)
                        if coords:
                            f.write(f"{coords[0]}\t{coords[1]}\t{coords[2]}\t{amp_name}_low_cov\n")
            count += 1
            
        logging.info(f"Generated masking BED files for {count} samples in {mask_dir}/")

    except Exception as e:
        logging.error(f"Failed to generate masking files: {e}")

def generate_uniformity_report(max_df, out_dir):
    """
    Generates two reports:
    1. sample_uniformity_report.tsv: Gini Score (Evenness) per sample.
    2. amplicon_efficiency_matrix.csv: Matrix showing % of total reads per amplicon.
    
    Returns:
        pd.DataFrame: The efficiency matrix (for plotting).
    """
    if 'bam' in max_df.columns:
        data = max_df.set_index('bam')
    else:
        data = max_df

    # --- Report 1: Amplicon Efficiency (% of Reads) ---
    # Normalize rows so they sum to 100%
    # Answers: "What percent of Sample A's reads were Amplicon X?"
    efficiency_df = data.div(data.sum(axis=1), axis=0) * 100
    
    eff_path = os.path.join(out_dir, "amplicon_efficiency_matrix.csv")
    efficiency_df.to_csv(eff_path)
    logging.info(f"Efficiency matrix saved: {eff_path}")

    # --- Report 2: Evenness (Gini Coefficient) ---
    summary_path = os.path.join(out_dir, "sample_uniformity_report.tsv")
    
    try:
        with open(summary_path, "w") as f:
            f.write("Sample\tTotal_Reads\tMean_Depth\tGini_Coefficient\tStatus\n")
            
            for sample_name, row in data.iterrows():
                depths = row.values
                
                total_reads = depths.sum()
                mean_depth = depths.mean()
                gini_score = calculate_gini(depths)
                
                # Interpret Gini
                if gini_score < 0.3:
                    status = "Excellent_Evenness"
                elif gini_score < 0.5:
                    status = "Acceptable"
                else:
                    status = "High_Inequality"

                f.write(f"{sample_name}\t{total_reads:.0f}\t{mean_depth:.1f}\t{gini_score:.3f}\t{status}\n")
                
        logging.info(f"Uniformity report saved: {summary_path}")

    except Exception as e:
        logging.error(f"Failed to generate uniformity report: {e}")
        return None

    return efficiency_df