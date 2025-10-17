#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
from pathlib import Path

def validate_datasets():
    """Validate the anonymized datasets"""
    
    # Load datasets with proper paths
    pre_test = pd.read_csv('raw/pre_test_scores.csv')
    post_control = pd.read_csv('raw/post_test_control.csv')
    post_experimental = pd.read_csv('raw/post_test_experimental.csv')
    
    print("=== DATA VALIDATION REPORT ===")
    
    # Check student counts
    print(f"\n1. Student Counts:")
    print(f"   Pre-test: {len(pre_test)} students")
    print(f"   Control group (post): {len(post_control)} students") 
    print(f"   Experimental group (post): {len(post_experimental)} students")
    
    # Check group assignments
    print(f"\n2. Group Distribution:")
    print(f"   Control group: {len(pre_test[pre_test['group']=='control'])} students")
    print(f"   Experimental group: {len(pre_test[pre_test['group']=='experimental'])} students")
    
    # Check score ranges
    print(f"\n3. Score Ranges:")
    print(f"   Pre-test: {pre_test['total_score'].min()} to {pre_test['total_score'].max()}")
    print(f"   Control post-test: {post_control['total_score'].min()} to {post_control['total_score'].max()}")
    print(f"   Experimental post-test: {post_experimental['total_score'].min()} to {post_experimental['total_score'].max()}")
    
    # Check for missing values
    print(f"\n4. Missing Values:")
    print(f"   Pre-test: {pre_test.isnull().sum().sum()} missing values")
    print(f"   Control post: {post_control.isnull().sum().sum()} missing values")
    print(f"   Experimental post: {post_experimental.isnull().sum().sum()} missing values")
    
    print(f"\n✅ All datasets validated successfully!")
    return pre_test, post_control, post_experimental

def create_processed_files():
    """Create processed datasets for analysis"""
    
    print("\n=== CREATING PROCESSED DATASETS ===")
    
    # Load raw data
    pre_test = pd.read_csv('raw/pre_test_scores.csv')
    post_control = pd.read_csv('raw/post_test_control.csv')
    post_experimental = pd.read_csv('raw/post_test_experimental.csv')
    
    # Create processed directory if it doesn't exist
    processed_dir = Path('processed')
    processed_dir.mkdir(exist_ok=True)
    
    # 1. Create combined_scores.csv (pre + post scores together)
    print("1. Creating combined_scores.csv...")
    
    # Add group info to post-test data
    post_control['group'] = 'control'
    post_experimental['group'] = 'experimental'
    
    # Combine all post-test data
    post_combined = pd.concat([post_control, post_experimental], ignore_index=True)
    
    # Merge pre and post scores
    combined_scores = pd.merge(
        pre_test[['student_id', 'total_score', 'group']].rename(columns={'total_score': 'pre_test_score'}),
        post_combined[['student_id', 'total_score']].rename(columns={'total_score': 'post_test_score'}),
        on='student_id',
        how='left'
    )
    
    # Calculate score improvement
    combined_scores['score_improvement'] = combined_scores['post_test_score'] - combined_scores['pre_test_score']
    combined_scores['improvement_percentage'] = (combined_scores['score_improvement'] / combined_scores['pre_test_score'].replace(0, 0.1)) * 100
    
    combined_scores.to_csv(processed_dir / 'combined_scores.csv', index=False)
    print(f"   ✅ Created: {processed_dir}/combined_scores.csv")
    print(f"   Records: {len(combined_scores)}")
    
    # 2. Create analysis_ready.csv (minimal columns for statistical analysis)
    print("2. Creating analysis_ready.csv...")
    
    analysis_ready = combined_scores[['student_id', 'group', 'pre_test_score', 'post_test_score', 'score_improvement']].copy()
    
    # Add some basic analytics
    analysis_summary = analysis_ready.groupby('group').agg({
        'pre_test_score': ['mean', 'std', 'count'],
        'post_test_score': ['mean', 'std'],
        'score_improvement': ['mean', 'std']
    }).round(2)
    
    analysis_ready.to_csv(processed_dir / 'analysis_ready.csv', index=False)
    print(f"   ✅ Created: {processed_dir}/analysis_ready.csv")
    
    # 3. Create summary statistics file
    print("3. Creating summary statistics...")
    
    summary_stats = {
        'dataset': ['Pre-test', 'Post-test Control', 'Post-test Experimental'],
        'n_students': [len(pre_test), len(post_control), len(post_experimental)],
        'mean_score': [
            pre_test['total_score'].mean(),
            post_control['total_score'].mean(), 
            post_experimental['total_score'].mean()
        ],
        'std_dev': [
            pre_test['total_score'].std(),
            post_control['total_score'].std(),
            post_experimental['total_score'].std()
        ]
    }
    
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv(processed_dir / 'summary_statistics.csv', index=False)
    print(f"   ✅ Created: {processed_dir}/summary_statistics.csv")
    
    # Print quick summary
    print(f"\n📊 QUICK SUMMARY:")
    print(f"   Pre-test mean: {pre_test['total_score'].mean():.2f} ± {pre_test['total_score'].std():.2f}")
    print(f"   Control post mean: {post_control['total_score'].mean():.2f} ± {post_control['total_score'].std():.2f}")
    print(f"   Experimental post mean: {post_experimental['total_score'].mean():.2f} ± {post_experimental['total_score'].std():.2f}")
    
    return combined_scores, analysis_ready

if __name__ == "__main__":
    # Run validation
    pre_test, post_control, post_experimental = validate_datasets()
    
    # Create processed files
    combined_scores, analysis_ready = create_processed_files()
    
    print(f"\n🎉 All processed files created successfully!")
    print(f"   Check the 'processed/' folder for:")
    print(f"   - combined_scores.csv")
    print(f"   - analysis_ready.csv") 
    print(f"   - summary_statistics.csv")