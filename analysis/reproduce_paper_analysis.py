#!/usr/bin/env python3
"""
Master script to reproduce all analyses and figures from the research paper.
Run this to completely replicate the study results.
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name):
    """Run a Python script and handle errors"""
    print(f"\n▶ Running {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {script_name} failed with error:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False
    return True

def main():
    print("=" * 60)
    print("REPRODUCING CARTOON PHYSICS INSTRUCTION STUDY ANALYSIS")
    print("=" * 60)
    
    # Ensure figures directory exists
    figures_dir = Path('../figures')
    figures_dir.mkdir(exist_ok=True)
    
    # Run all analysis steps
    steps = [
        "statistical_analysis.py",
        "visualization.py"
    ]
    
    success_count = 0
    for step in steps:
        if run_script(step):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"ANALYSIS COMPLETE: {success_count}/{len(steps)} steps successful")
    
    if success_count == len(steps):
        print("🎉 All analyses reproduced successfully!")
        print("📊 Check the '../figures/' folder for generated plots")
        print("📈 Statistical results printed above")
    else:
        print("⚠️  Some analyses failed. Check the errors above.")

if __name__ == "__main__":
    main()
