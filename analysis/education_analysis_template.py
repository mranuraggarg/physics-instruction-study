#!/usr/bin/env python3
"""
Template for education research analysis.
Includes common functions for educational data analysis.
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import pingouin as pg
import researchpy as rp
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class EducationAnalyzer:
    """A class for common education research analyses"""
    
    def __init__(self, data_path=None):
        self.data = None
        if data_path:
            self.load_data(data_path)
        
        # Set plotting style for education research
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("colorblind")
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Colorblind-friendly
    
    def load_data(self, data_path):
        """Load educational dataset"""
        self.data = pd.read_csv(data_path)
        print(f"Loaded dataset with {len(self.data)} records")
        return self.data
    
    def descriptive_stats_by_group(self, score_col, group_col):
        """Calculate descriptive statistics by group"""
        print(f"Descriptive Statistics for {score_col} by {group_col}")
        print("=" * 50)
        
        summary = self.data.groupby(group_col)[score_col].agg([
            'count', 'mean', 'std', 'min', 'max', 'median'
        ]).round(2)
        
        print(summary)
        return summary
    
    def anova_analysis(self, score_col, group_col):
        """Perform ANOVA with post-hoc tests"""
        print(f"\nANOVA Analysis: {score_col} by {group_col}")
        print("=" * 40)
        
        # One-way ANOVA
        anova_result = pg.anova(data=self.data, dv=score_col, between=group_col, detailed=True)
        print("One-Way ANOVA:")
        print(anova_result.round(4))
        
        # Post-hoc tests if significant
        if anova_result['p-unc'][0] < 0.05:
            print("\nPost-hoc Tests (Tukey HSD):")
            posthoc = pg.pairwise_tukey(data=self.data, dv=score_col, between=group_col)
            print(posthoc.round(4))
        
        return anova_result
    
    def effect_size_calculation(self, score_col, group_col, group1, group2):
        """Calculate effect sizes between groups"""
        print(f"\nEffect Size: {group1} vs {group2} on {score_col}")
        print("=" * 45)
        
        data1 = self.data[self.data[group_col] == group1][score_col]
        data2 = self.data[self.data[group_col] == group2][score_col]
        
        # Cohen's d
        cohens_d = pg.compute_effsize(data1, data2, eftype='cohen')
        
        # Hedges' g (small sample correction)
        hedges_g = pg.compute_effsize(data1, data2, eftype='hedges')
        
        print(f"Cohen's d: {cohens_d:.3f}")
        print(f"Hedges' g: {hedges_g:.3f}")
        
        return {'cohens_d': cohens_d, 'hedges_g': hedges_g}
    
    def plot_score_distributions(self, score_col, group_col, save_path=None):
        """Plot score distributions by group"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Violin plot
        sns.violinplot(data=self.data, x=group_col, y=score_col, 
                       ax=ax1, palette=self.colors)
        ax1.set_title(f'{score_col} Distribution by {group_col}')
        ax1.set_ylabel(score_col)
        
        # Box plot with individual points
        sns.boxplot(data=self.data, x=group_col, y=score_col, 
                    ax=ax2, palette=self.colors)
        sns.stripplot(data=self.data, x=group_col, y=score_col, 
                      ax=ax2, color='black', alpha=0.5, size=3)
        ax2.set_title(f'{score_col} by {group_col} (with individual scores)')
        ax2.set_ylabel(score_col)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {save_path}")
        
        plt.show()
    
    def reliability_analysis(self, items):
        """Calculate reliability metrics (Cronbach's alpha)"""
        if all(item in self.data.columns for item in items):
            print("\nReliability Analysis")
            print("=" * 30)
            
            # Note: For actual Cronbach's alpha, you'd use:
            # from pingouin import cronbach_alpha
            # alpha = cronbach_alpha(self.data[items])
            
            print(f"Items analyzed: {len(items)}")
            print("Note: Install pingouin for Cronbach's alpha calculation")
        else:
            print("Some items not found in dataset")
    
    def pre_post_analysis(self, pre_col, post_col, group_col=None):
        """Analyze pre-post test improvements"""
        print("\nPre-Post Test Analysis")
        print("=" * 30)
        
        self.data['improvement'] = self.data[post_col] - self.data[pre_col]
        
        # Overall improvement
        t_stat, p_value = stats.ttest_rel(self.data[pre_col], self.data[post_col])
        print(f"Overall improvement: t({len(self.data)-1}) = {t_stat:.3f}, p = {p_value:.3f}")
        print(f"Mean improvement: {self.data['improvement'].mean():.2f} ± {self.data['improvement'].std():.2f}")
        
        # By group if specified
        if group_col:
            groups = self.data[group_col].unique()
            for group in groups:
                group_data = self.data[self.data[group_col] == group]
                t_stat, p_value = stats.ttest_rel(group_data[pre_col], group_data[post_col])
                print(f"{group} improvement: t({len(group_data)-1}) = {t_stat:.3f}, p = {p_value:.3f}")
        
        return self.data

# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = EducationAnalyzer()
    
    print("Education Research Analysis Template")
    print("Customize this template for your specific educational research project!")
