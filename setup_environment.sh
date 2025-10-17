#!/bin/bash
# setup_environment.sh - Sets up education research environment

echo "Setting up Education Research Environment..."
echo "============================================="

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed. Please install Miniconda or Anaconda first."
    exit 1
fi

# Create environment from YAML
echo "Creating conda environment from environment.yml..."
conda env create -f environment.yml

# Activate environment
echo "Activating environment..."
conda activate edu-research

# Install any additional pip packages
echo "Installing additional education research packages..."
pip install -r analysis/requirements.txt

echo ""
echo "✅ Environment setup complete!"
echo "🎓 You can now activate with: conda activate edu-research"
echo "📊 Run analyses with: python analysis/statistical_analysis.py"
