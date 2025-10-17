#!/usr/bin/env python3
"""
Visualization functions for the cartoon physics instruction study.
Generates all figures used in the research paper.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("colorblind")

def setup_plotting():
    """Configure matplotlib for publication quality"""
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12

def clean_data(series):
    """Remove NaN and infinite values from data"""
    return series.replace([np.inf, -np.inf], np.nan).dropna()

def plot_pre_test_distributions(analysis_df, save_path=None):
    """Plot pre-test score distributions for both groups"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Control group - with data cleaning
    control_pre = clean_data(analysis_df[analysis_df['group'] == 'control']['pre_test_score'])
    if len(control_pre) > 0:
        mu_control, std_control = stats.norm.fit(control_pre)
        x_control = np.linspace(control_pre.min(), control_pre.max(), 100)
        p_control = stats.norm.pdf(x_control, mu_control, std_control) * len(control_pre)
        
        ax1.hist(control_pre, bins=8, density=False, alpha=0.7, color='blue', label='Control')
        ax1.plot(x_control, p_control, 'b-', linewidth=2, label=f'Normal fit')
        ax1.set_xlabel('Pre-test Score')
        ax1.set_ylabel('Number of Students')
        ax1.set_title(f'Control Group (n={len(control_pre)})')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
    else:
        ax1.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Control Group (No Data)')
    
    # Experimental group - with data cleaning
    experimental_pre = clean_data(analysis_df[analysis_df['group'] == 'experimental']['pre_test_score'])
    if len(experimental_pre) > 0:
        mu_exp, std_exp = stats.norm.fit(experimental_pre)
        x_exp = np.linspace(experimental_pre.min(), experimental_pre.max(), 100)
        p_exp = stats.norm.pdf(x_exp, mu_exp, std_exp) * len(experimental_pre)
        
        ax2.hist(experimental_pre, bins=8, density=False, alpha=0.7, color='red', label='Experimental')
        ax2.plot(x_exp, p_exp, 'r-', linewidth=2, label=f'Normal fit')
        ax2.set_xlabel('Pre-test Score')
        ax2.set_ylabel('Number of Students')
        ax2.set_title(f'Experimental Group (n={len(experimental_pre)})')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    else:
        ax2.text(0.5, 0.5, 'No data available', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title('Experimental Group (No Data)')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path / 'pre_test_distributions.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path / 'pre_test_distributions.png'}")
    
    plt.show()

def plot_post_test_comparison(analysis_df, save_path=None):
    """Plot post-test score comparison between groups"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Clean data first
    control_post = clean_data(analysis_df[analysis_df['group'] == 'control']['post_test_score'])
    experimental_post = clean_data(analysis_df[analysis_df['group'] == 'experimental']['post_test_score'])
    
    # Only plot if we have data
    if len(control_post) > 0 and len(experimental_post) > 0:
        # Histograms
        ax1.hist(control_post, bins=8, alpha=0.7, color='blue', label='Control', density=True)
        ax1.hist(experimental_post, bins=8, alpha=0.7, color='red', label='Experimental', density=True)
        ax1.set_xlabel('Post-test Score')
        ax1.set_ylabel('Density')
        ax1.set_title('Post-test Score Distributions')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        plot_data = []
        for group in ['control', 'experimental']:
            group_data = clean_data(analysis_df[analysis_df['group'] == group]['post_test_score'])
            for score in group_data:
                plot_data.append({'Group': group.capitalize(), 'Score': score})
        
        plot_df = pd.DataFrame(plot_data)
        sns.boxplot(data=plot_df, x='Group', y='Score', ax=ax2, palette=['blue', 'red'])
        sns.stripplot(data=plot_df, x='Group', y='Score', ax=ax2, color='black', alpha=0.5, size=4)
        ax2.set_title('Post-test Score Comparison')
        ax2.set_ylabel('Score')
        ax2.grid(True, alpha=0.3)
        
        # Add significance annotation
        control_mean = control_post.mean()
        experimental_mean = experimental_post.mean()
        ax2.text(0.5, max(plot_df['Score']) * 0.9, f'Control: {control_mean:.1f} ± {control_post.std():.1f}', 
                 ha='center', fontsize=10)
        ax2.text(1.5, max(plot_df['Score']) * 0.9, f'Experimental: {experimental_mean:.1f} ± {experimental_post.std():.1f}', 
                 ha='center', fontsize=10)
    else:
        ax1.text(0.5, 0.5, 'Insufficient data for plotting', ha='center', va='center', transform=ax1.transAxes)
        ax2.text(0.5, 0.5, 'Insufficient data for plotting', ha='center', va='center', transform=ax2.transAxes)
        ax1.set_title('Post-test Distributions')
        ax2.set_title('Post-test Comparison')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path / 'post_test_comparison.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path / 'post_test_comparison.png'}")
    
    plt.show()

def plot_improvement_scores(analysis_df, save_path=None):
    """Plot score improvements by group"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Clean the data first
    analysis_df_clean = analysis_df.copy()
    analysis_df_clean['score_improvement'] = analysis_df_clean['score_improvement'].replace([np.inf, -np.inf], np.nan)
    analysis_df_clean = analysis_df_clean.dropna(subset=['score_improvement'])
    
    # Prepare data for plotting
    plot_data = []
    for group in ['control', 'experimental']:
        group_data = analysis_df_clean[analysis_df_clean['group'] == group]
        for _, row in group_data.iterrows():
            plot_data.append({
                'Group': group.capitalize(),
                'Improvement': row['score_improvement'],
                'Student': row['student_id']
            })
    
    plot_df = pd.DataFrame(plot_data)
    
    if len(plot_df) > 0:
        # Violin plot with swarm plot overlay
        sns.violinplot(data=plot_df, x='Group', y='Improvement', 
                       palette=['blue', 'red'], inner='quartile', ax=ax)
        sns.swarmplot(data=plot_df, x='Group', y='Improvement', 
                      color='black', alpha=0.6, size=3, ax=ax)
        
        ax.set_ylabel('Score Improvement (Post - Pre)')
        ax.set_title('Learning Improvement by Instructional Method')
        ax.grid(True, alpha=0.3)
        
        # Add mean lines and annotations
        control_improve = plot_df[plot_df['Group'] == 'Control']['Improvement'].mean()
        experimental_improve = plot_df[plot_df['Group'] == 'Experimental']['Improvement'].mean()
        
        ax.axhline(0, color='gray', linestyle='--', alpha=0.7)
        ax.text(0, control_improve + 1, f'Mean: {control_improve:.1f}', 
                ha='center', va='bottom', fontweight='bold')
        ax.text(1, experimental_improve + 1, f'Mean: {experimental_improve:.1f}', 
                ha='center', va='bottom', fontweight='bold')
    else:
        ax.text(0.5, 0.5, 'No improvement data available', 
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_title('Learning Improvement by Instructional Method')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path / 'improvement_scores.png', dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path / 'improvement_scores.png'}")
    
    plt.show()

def create_data_summary(analysis_df):
    """Create a summary of data quality"""
    print("=== DATA SUMMARY ===")
    for group in ['control', 'experimental']:
        group_data = analysis_df[analysis_df['group'] == group]
        pre_scores = clean_data(group_data['pre_test_score'])
        post_scores = clean_data(group_data['post_test_score'])
        
        print(f"\n{group.capitalize()} Group:")
        print(f"  Total records: {len(group_data)}")
        print(f"  Valid pre-test scores: {len(pre_scores)}")
        print(f"  Valid post-test scores: {len(post_scores)}")
        if len(pre_scores) > 0:
            print(f"  Pre-test range: {pre_scores.min():.1f} - {pre_scores.max():.1f}")
        if len(post_scores) > 0:
            print(f"  Post-test range: {post_scores.min():.1f} - {post_scores.max():.1f}")

if __name__ == "__main__":
    setup_plotting()
    
    # Load data
    data_dir = Path('../data/processed')
    analysis_df = pd.read_csv(data_dir / 'analysis_ready.csv')
    
    # Create data summary
    create_data_summary(analysis_df)
    
    # Create figures directory
    figures_dir = Path('../figures')
    figures_dir.mkdir(exist_ok=True)
    
    # Generate all figures
    plot_pre_test_distributions(analysis_df, figures_dir)
    plot_post_test_comparison(analysis_df, figures_dir)
    plot_improvement_scores(analysis_df, figures_dir)
    
    print("✅ All visualizations generated!")
