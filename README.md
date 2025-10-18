# Comparative Study: Traditional vs. Cartoon-Based Physics Instruction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17385946.svg)](https://doi.org/10.5281/zenodo.17385946)

A randomized controlled trial comparing the effectiveness of traditional physics instruction versus cartoon-enhanced curriculum on student learning outcomes.

## 🔬 Key Finding

**Cartoon-based instruction led to significantly higher post-test and improvement scores**, with large effect sizes:
  - Cartoon-based instruction produced significantly higher post-test and improvement scores.
  - Welch’s t-test: Post-test t(25.5)=2.39, p=0.0247; Improvement t(25.3)=2.90, p=0.0076.
  - Large practical effects (Cohen’s d ≈ 0.85–1.03).
  - 95% confidence intervals for the true mean differences: Post-test (0.65, 8.79); Improvement (1.33, 7.86).
  - Indicates that cartoon-based pedagogy substantially improved learning outcomes in secondary physics.

## 📁 Project Structure

- `data/` - Research datasets (anonymized)
  - `raw/` - Original data collection files
  - `processed/` - Cleaned and merged datasets  
  - `validate_data.py` - Data validation script
- `analysis/` - Statistical analysis and visualization code
- `figures/` - Generated plots and visualizations  
- `manuscript/` - Research paper (in preparation)
- `environment.yml` - Conda environment configuration
- `setup_environment.sh` - Environment setup script

## 🚀 Quick Start

### 1. Set Up Environment
```bash
# Using conda (recommended)
conda env create -f environment.yml
conda activate physics-instruction

# Or using pip
pip install -r analysis/requirements.txt
```

### 2. Validate Data
```bash

cd data
python validate_data.py
```

### 3. Reproduce Analysis

```bash
cd analysis

# Reproduce main analysis pipeline
python reproduce_paper_analysis.py

# Run statistical tests
python statistical_analysis.py

# Generate visualizations
python visualization.py
```

## 📊 Dataset Description

### Raw Data Files

- **pre_test_scores.csv:** Pre-intervention assessment scores
- **post_test_control.csv:** Post-test scores for control group
- **post_test_experimental.csv:** Post-test scores for experimental group
- **student_mapping.csv:** Anonymous student identifiers

### Processed Data

- **analysis_ready.csv:** Merged dataset for analysis
- **analysis_ready_corrected.csv:** Complete dataset with integrated experimental scores
- **combined_scores.csv:** All scores with improvement metrics

## 🔍 Research Design

### Participants

- **Total:** 41 secondary education students
- **Control group:** 21 students (traditional instruction)
- **Experimental group:** 20 students (cartoon-enhanced instruction)

### Intervention

- **Control:** Standard physics instruction
- **Experimental:** Physics instruction integrated with educational cartoons
- **Duration:** Equivalent instructional time for both groups

### Measures

- Pre-test and post-test physics assessments
- Score improvement (post-test - pre-test)
- Statistical comparison using t-tests, effect sizes, and confidence intervals


## 📈 Key Results

### Learning Improvements

Group|Pre-test Mean|Post-test Mean|Improvement|
--|--|--|--|
Control|3.93 ± 2.13|13.33 ± 6.86|9.40 ± 5.46|
Experimental|3.83 ± 1.74|18.06 ± 3.88|14.00 ± 3.13|

### Statistical Analysis

- **Post-test comparison:** t(25.5) = 2.388, p = 0.0247
- **Improvement comparison:** t(25.3) = 2.902, p = 0.0076
- **Effect sizes:** Post-test d = 0.847; Improvement d = 1.033 (large)
- **Confidence Intervals:** Post-test (0.65, 8.79); Improvement (1.33, 7.86)

## 🎯 Implications

1. **Educational Practice:** Cartoon-based physics instruction leads to significantly greater concept mastery and problem-solving performance.
2. **Pedagogical Value:** Demonstrates strong practical impact of integrating visual and narrative media in physics education.
3. **Research Direction:** Supports continued exploration of multimedia-enhanced learning environments for secondary-level science.

## 📝 Citation

If you use this research or code, please cite:

```bibtex
@article{physics2024,
  title = {Comparative Effectiveness of Traditional vs. Cartoon-Based Physics Instruction: A Randomized Controlled Trial},
  author = {Anurag Garg},
  year = {2025},
  url = {https://github.com/mranuraggarg/physics-instruction-study}
}
```
## 🤝 Contributing

This repository contains the complete data and analysis code for reproducibility. For questions or collaborations, please open an issue or contact the corresponding author.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Participants and educational institution partners
- Research assistants and collaborators
- Open-source scientific Python community
