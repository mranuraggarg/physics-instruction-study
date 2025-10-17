# Comparative Study: Traditional vs. Cartoon-Based Physics Instruction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A randomized controlled trial comparing the effectiveness of traditional physics instruction versus cartoon-enhanced curriculum on student learning outcomes.

## 🔬 Key Finding

**No significant difference** in learning outcomes was found between traditional instruction and cartoon-based physics curriculum:
- Improvement difference: 0.54 points (p=0.77, Cohen's d=0.09)
- Both groups showed substantial learning gains (≈10 points improvement)
- 95% confidence interval for difference: (-3.09, 4.17)

## 📁 Project Structure
.
├── README.md
├── analysis
│   ├── README.md
│   ├── comparision_post.py
│   ├── comparision_pre.py
│   ├── debug_data.py
│   ├── education_analysis_template.py
│   ├── fix_data_issues.py
│   ├── reproduce_paper_analysis.py
│   ├── requirements.txt
│   ├── statistical_analysis.py
│   ├── statistical_comparison.png
│   └── visualization.py
├── data
│   ├── README.md
│   ├── group1.txt
│   ├── group2.txt
│   ├── processed
│   │   ├── analysis_ready.csv
│   │   ├── analysis_ready_cleaned.csv
│   │   ├── analysis_ready_corrected.csv
│   │   ├── combined_scores.csv
│   │   └── summary_statistics.csv
│   ├── raw
│   │   ├── post_test_control.csv
│   │   ├── post_test_experimental.csv
│   │   ├── pre_test_scores.csv
│   │   └── student_mapping.csv
│   └── validate_data.py
├── environment.yml
├── figures
│   ├── improvement_scores.png
│   ├── post_test_comparison.png
│   └── pre_test_distributions.png
├── manuscript
└── setup_environment.sh


## 🚀 Quick Start

### 1. Set Up Environment
```bash
# Using conda (recommended)
conda env create -f environment.yml
conda activate physics-instruction

# Or using pip
pip install -r analysis/requirements.txt

### 2. Validate Data
```bash

cd data
python validate_data.py

### 3. Reproduce Analysis

```bash
cd analysis

# Reproduce main analysis pipeline
python reproduce_paper_analysis.py

# Run statistical tests
python statistical_analysis.py

# Generate visualizations
python visualization.py

## 📊 Dataset Description

### Raw Data Files

- pre_test_scores.csv: Pre-intervention assessment scores
- post_test_control.csv: Post-test scores for control group
- post_test_experimental.csv: Post-test scores for experimental group
- student_mapping.csv: Anonymous student identifiers

### Processed Data

- analysis_ready.csv: Merged dataset for analysis
- analysis_ready_corrected.csv: Complete dataset with integrated experimental scores
- combined_scores.csv: All scores with improvement metrics

## 🔍 Research Design

### Participants

- Total: 41 secondary education students
- Control group: 21 students (traditional instruction)
- Experimental group: 20 students (cartoon-enhanced instruction)

### Intervention

- Control: Standard physics instruction
- Experimental: Physics instruction integrated with educational cartoons
- Duration: Equivalent instructional time for both groups

### Measures

- Pre-test and post-test physics assessments
- Score improvement (post-test - pre-test)
- Statistical comparison using t-tests, effect sizes, and confidence intervals


## 📈 Key Results

### Learning Improvements

Group|Pre-test Mean|Post-test Mean|Improvement|
--|--|--|--|
Control|3.93 ± 2.13|13.69 ± 6.90|9.76 ± 5.78|
Experimental|3.83 ± 1.74|14.12 ± 6.06|10.30 ± 5.71|

### Statistical Analysis

- Post-test comparison: t = -0.214, p = 0.832
- Improvement comparison: t = -0.300, p = 0.766
- Effect size (improvement): Cohen's d = 0.094 (small)
- Non-parametric test: Mann-Whitney U = 198.0, p = 0.764

## 🎯 Implications

1. **Educational Practice:** Traditional and cartoon-enhanced methods produce equivalent learning outcomes
2. **Resource Allocation:** Questions cost-effectiveness of developing multimedia enhancements for basic physics concepts
3. **Research Direction:** Suggests need to identify specific contexts where multimedia enhancements provide added value

## 📝 Citation

If you use this research or code, please cite:

```bibtex
@article{physics2024,
  title = {Comparative Effectiveness of Traditional vs. Cartoon-Based Physics Instruction: A Randomized Controlled Trial},
  author = {[Your Name] and [Collaborators]},
  year = {2024},
  url = {https://github.com/yourusername/physics-instruction-study}
}

## 🤝 Contributing

This repository contains the complete data and analysis code for reproducibility. For questions or collaborations, please open an issue or contact the corresponding author.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Participants and educational institution partners
- Research assistants and collaborators
- Open-source scientific Python community

