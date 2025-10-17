import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# === DATA INTEGRATION FIX WITH CORRECT PATHS ===
print("Fixing data integration...")

# Read the experimental post-test data from raw folder
exp_post = pd.read_csv('../data/raw/post_test_experimental.csv')

# Fix the column name typo (you mentioned you already did this manually, but keeping for safety)
exp_post = exp_post.rename(columns={'istudent_id': 'student_id'})

# Read the main dataset from processed folder
main_data = pd.read_csv('../data/processed/analysis_ready.csv')

# Merge the experimental post-test scores
df = main_data.merge(
    exp_post[['student_id', 'total_score']], 
    on='student_id', 
    how='left'
)

# Update post_test_score and score_improvement for experimental group
experimental_mask = df['group'] == 'experimental'
df.loc[experimental_mask, 'post_test_score'] = df.loc[experimental_mask, 'total_score']
df.loc[experimental_mask, 'score_improvement'] = (
    df.loc[experimental_mask, 'post_test_score'] - 
    df.loc[experimental_mask, 'pre_test_score']
)

# Drop the temporary total_score column
df = df.drop('total_score', axis=1)

print(f"✅ Data integration complete! Total records: {len(df)}")

# Save the corrected dataset to processed folder
df.to_csv('../data/processed/analysis_ready_corrected.csv', index=False)
print("✅ Saved corrected data to: ../data/processed/analysis_ready_corrected.csv")

# === CONTINUE WITH STATISTICAL ANALYSIS ===
# Separate groups
control = df[df['group'] == 'control']
experimental = df[df['group'] == 'experimental']

print("\n=== DESCRIPTIVE STATISTICS ===")
print("\nControl Group (n=21):")
print(f"Pre-test:  {control['pre_test_score'].mean():.2f} ± {control['pre_test_score'].std():.2f}")
print(f"Post-test: {control['post_test_score'].mean():.2f} ± {control['post_test_score'].std():.2f}")
print(f"Improvement: {control['score_improvement'].mean():.2f} ± {control['score_improvement'].std():.2f}")

print("\nExperimental Group (n=20):")
print(f"Pre-test:  {experimental['pre_test_score'].mean():.2f} ± {experimental['pre_test_score'].std():.2f}")
print(f"Post-test: {experimental['post_test_score'].mean():.2f} ± {experimental['post_test_score'].std():.2f}")
print(f"Improvement: {experimental['score_improvement'].mean():.2f} ± {experimental['score_improvement'].std():.2f}")

print("\n=== NORMALITY TESTS (Shapiro-Wilk) ===")
# Test normality of improvements
control_improvement_norm = stats.shapiro(control['score_improvement'])
exp_improvement_norm = stats.shapiro(experimental['score_improvement'])

print(f"Control improvement normality: p-value = {control_improvement_norm.pvalue:.4f}")
print(f"Experimental improvement normality: p-value = {exp_improvement_norm.pvalue:.4f}")

print("\n=== INDEPENDENT T-TESTS ===")
# T-test for post-test scores
post_test_t = stats.ttest_ind(control['post_test_score'], experimental['post_test_score'])
print(f"Post-test scores t-test: t = {post_test_t.statistic:.3f}, p = {post_test_t.pvalue:.4f}")

# T-test for improvements
improvement_t = stats.ttest_ind(control['score_improvement'], experimental['score_improvement'])
print(f"Improvement t-test: t = {improvement_t.statistic:.3f}, p = {improvement_t.pvalue:.4f}")

print("\n=== EFFECT SIZES (Cohen's d) ===")
def cohens_d(group1, group2):
    """Calculate Cohen's d for effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1 + n2 - 2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# Effect sizes
post_test_d = cohens_d(experimental['post_test_score'], control['post_test_score'])
improvement_d = cohens_d(experimental['score_improvement'], control['score_improvement'])

print(f"Post-test effect size (d): {post_test_d:.3f}")
print(f"Improvement effect size (d): {improvement_d:.3f}")

print("\n=== CONFIDENCE INTERVALS ===")
# 95% CI for mean difference in improvements
def mean_ci(group1, group2, alpha=0.05):
    n1, n2 = len(group1), len(group2)
    mean_diff = np.mean(group1) - np.mean(group2)
    se = np.sqrt(np.var(group1, ddof=1)/n1 + np.var(group2, ddof=1)/n2)
    t_critical = stats.t.ppf(1 - alpha/2, n1 + n2 - 2)
    return mean_diff - t_critical * se, mean_diff + t_critical * se

improvement_ci = mean_ci(experimental['score_improvement'], control['score_improvement'])
print(f"95% CI for improvement difference: ({improvement_ci[0]:.3f}, {improvement_ci[1]:.3f})")

print("\n=== NON-PARAMETRIC TEST (Mann-Whitney U) ===")
# If data isn't normal, use Mann-Whitney U test
improvement_mw = stats.mannwhitneyu(control['score_improvement'], experimental['score_improvement'])
print(f"Mann-Whitney U test for improvements: U = {improvement_mw.statistic:.1f}, p = {improvement_mw.pvalue:.4f}")

# Create summary visualization
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Improvement comparison
sns.boxplot(data=df, x='group', y='score_improvement', ax=axes[0])
axes[0].set_title('Score Improvement by Group')
axes[0].set_ylabel('Improvement (Post-test - Pre-test)')

# Post-test scores comparison
sns.boxplot(data=df, x='group', y='post_test_score', ax=axes[1])
axes[1].set_title('Post-test Scores by Group')
axes[1].set_ylabel('Post-test Score')

plt.tight_layout()
plt.savefig('statistical_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n=== INTERPRETATION GUIDE ===")
print("Cohen's d effect sizes:")
print("0.2 = Small effect")
print("0.5 = Medium effect") 
print("0.8 = Large effect")
print(f"\nOur improvement effect size: {improvement_d:.3f} ({'small' if abs(improvement_d) < 0.5 else 'medium' if abs(improvement_d) < 0.8 else 'large'} effect)")
