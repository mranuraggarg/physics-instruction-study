#!/usr/bin/env python3
"""Debug script to check data issues"""

import pandas as pd
import numpy as np
from pathlib import Path

def check_data_issues():
    """Check for data problems"""
    data_dir = Path('../data/processed')
    analysis_df = pd.read_csv(data_dir / 'analysis_ready.csv')
    
    print("=== DATA QUALITY CHECK ===")
    print(f"Total records: {len(analysis_df)}")
    print(f"Columns: {analysis_df.columns.tolist()}")
    
    # Check for missing values
    print("\nMissing values:")
    print(analysis_df.isnull().sum())
    
    # Check experimental group data
    experimental = analysis_df[analysis_df['group'] == 'experimental']
    print(f"\nExperimental group records: {len(experimental)}")
    print("Experimental post-test scores:")
    print(experimental['post_test_score'].describe())
    
    # Check for NaN/infinite values
    print(f"\nNaN values in experimental post-test: {experimental['post_test_score'].isna().sum()}")
    print(f"Infinite values in experimental post-test: {np.isinf(experimental['post_test_score']).sum()}")
    
    # Show problematic rows
    problematic = experimental[experimental['post_test_score'].isna() | np.isinf(experimental['post_test_score'])]
    if len(problematic) > 0:
        print("\nProblematic rows:")
        print(problematic)
    
    return analysis_df

if __name__ == "__main__":
    check_data_issues()
