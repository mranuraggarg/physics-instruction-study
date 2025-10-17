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

print("\n=== INDEPENDENT T-TESTS ===")
# Clean arrays (drop NaNs) for post-test scores and improvements
post_ctrl = control['post_test_score'].astype(float).dropna()
post_exp  = experimental['post_test_score'].astype(float).dropna()
imp_ctrl  = control['score_improvement'].astype(float).dropna()
imp_exp   = experimental['score_improvement'].astype(float).dropna()

# === Welch's t-tests (robust to unequal variances & sizes) ===
# Post-test
t_post, p_post = stats.ttest_ind(post_exp, post_ctrl, equal_var=False, nan_policy='omit')
# Welch-Satterthwaite df for post-test
s2c, s2e = post_ctrl.var(ddof=1), post_exp.var(ddof=1)
nc, ne   = len(post_ctrl), len(post_exp)
se_post  = np.sqrt(s2c/nc + s2e/ne)
df_post  = (s2c/nc + s2e/ne)**2 / ((s2c**2)/(nc**2*(nc-1)) + (s2e**2)/(ne**2*(ne-1)))
print(f"Post-test (Welch) t({df_post:.2f}) = {t_post:.3f}, p = {p_post:.4f}")

# Improvements
t_imp, p_imp = stats.ttest_ind(imp_exp, imp_ctrl, equal_var=False, nan_policy='omit')
s2c_i, s2e_i = imp_ctrl.var(ddof=1), imp_exp.var(ddof=1)
nc_i, ne_i   = len(imp_ctrl), len(imp_exp)
se_imp       = np.sqrt(s2c_i/nc_i + s2e_i/ne_i)
df_imp       = (s2c_i/nc_i + s2e_i/ne_i)**2 / ((s2c_i**2)/(nc_i**2*(nc_i-1)) + (s2e_i**2)/(ne_i**2*(ne_i-1)))
print(f"Improvement (Welch) t({df_imp:.2f}) = {t_imp:.3f}, p = {p_imp:.4f}")

print("\n=== EFFECT SIZES (Cohen's d) ===")
# Cohen's d (pooled SD) using cleaned arrays
pooled_post = np.sqrt((post_ctrl.var(ddof=1) + post_exp.var(ddof=1)) / 2)
post_d = (post_exp.mean() - post_ctrl.mean()) / pooled_post
pooled_imp = np.sqrt((imp_ctrl.var(ddof=1) + imp_exp.var(ddof=1)) / 2)
imp_d  = (imp_exp.mean() - imp_ctrl.mean()) / pooled_imp
print(f"Post-test effect size (d): {post_d:.3f}")
print(f"Improvement effect size (d): {imp_d:.3f}")

print("\n=== CONFIDENCE INTERVALS (Welch) ===")
alpha = 0.05
# 95% CI for mean difference (exp - ctrl)
from scipy.stats import t as tdist

# Post-test CI
md_post = post_exp.mean() - post_ctrl.mean()
ci_half_post = tdist.ppf(1 - alpha/2, df_post) * se_post
print(f"95% CI for post-test difference: ({md_post - ci_half_post:.3f}, {md_post + ci_half_post:.3f})")

# Improvement CI
md_imp = imp_exp.mean() - imp_ctrl.mean()
ci_half_imp = tdist.ppf(1 - alpha/2, df_imp) * se_imp
print(f"95% CI for improvement difference: ({md_imp - ci_half_imp:.3f}, {md_imp + ci_half_imp:.3f})")

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
print(f"\nOur improvement effect size: {imp_d:.3f} (" + ("small" if abs(imp_d) < 0.5 else "medium" if abs(imp_d) < 0.8 else "large") + " effect)")
