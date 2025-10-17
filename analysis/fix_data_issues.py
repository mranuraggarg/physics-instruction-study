#!/usr/bin/env python3
"""Fix common data issues"""

import pandas as pd
import numpy as np
from pathlib import Path

def fix_data_issues():
    """Fix common data problems"""
    data_dir = Path('../data/processed')
    
    # Load and clean analysis_ready.csv
    analysis_df = pd.read_csv(data_dir / 'analysis_ready.csv')
    
    print("Before cleaning:")
    print(f"Total records: {len(analysis_df)}")
    print(f"Missing post-test scores: {analysis_df['post_test_score'].isna().sum()}")
    
    # Remove rows with missing critical data
    analysis_df = analysis_df.dropna(subset=['pre_test_score', 'post_test_score'])
    
    # Fix infinite values in improvement
    analysis_df['score_improvement'] = analysis_df['post_test_score'] - analysis_df['pre_test_score']
    analysis_df = analysis_df.replace([np.inf, -np.inf], np.nan)
    analysis_df = analysis_df.dropna(subset=['score_improvement'])
    
    print("\nAfter cleaning:")
    print(f"Total records: {len(analysis_df)}")
    print(f"Control group: {len(analysis_df[analysis_df['group'] == 'control'])}")
    print(f"Experimental group: {len(analysis_df[analysis_df['group'] == 'experimental'])}")
    
    # Save cleaned data
    analysis_df.to_csv(data_dir / 'analysis_ready_cleaned.csv', index=False)
    print(f"\nSaved cleaned data to: {data_dir / 'analysis_ready_cleaned.csv'}")
    
    return analysis_df

if __name__ == "__main__":
    fix_data_issues()
