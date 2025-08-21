#!/usr/bin/env python3
"""
CardDemo Basic Requirements Validator (DeepEval Disabled)

This script runs the validation with DeepEval disabled to avoid infinite loops
and SSL certificate issues. It uses basic component validation instead.

Author: Savantly
Date: 2025
"""

import os
import sys
from pathlib import Path
import logging

# Import the DeepEval validator
from deepeval_validator import CardDemoDeepEvalValidator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to run basic validation without DeepEval.
    """
    print("CardDemo Basic Requirements Validator (DeepEval Disabled)")
    print("=" * 60)
    
    # Configuration
    requirements_file = "../data/CD-Requirements.json"
    codebase_path = "../.."
    
    # Validate file paths
    if not os.path.exists(requirements_file):
        print(f"❌ Error: Requirements file not found: {requirements_file}")
        sys.exit(1)
    
    if not os.path.exists(codebase_path):
        print(f"❌ Error: Codebase path not found: {codebase_path}")
        sys.exit(1)
    
    print("🔍 Initializing basic validator (DeepEval disabled)...")
    
    try:
        # Initialize the validator with DeepEval disabled
        validator = CardDemoDeepEvalValidator(
            requirements_file=requirements_file,
            codebase_path=codebase_path,
            enable_deepeval=False  # Disable DeepEval to avoid infinite loops
        )
        
        print("📊 Running basic validation...")
        
        # Run the complete validation process
        results = validator.run_deepeval_validation()
        
        # Display validation summary
        print("\n📈 BASIC VALIDATION SUMMARY:")
        print("-" * 40)
        print(f"Total Requirements: {results['coverage'].total_requirements}")
        print(f"Coverage: {results['coverage'].coverage_percentage:.1f}%")
        print(f"Semantic Accuracy: {results['coverage'].semantic_accuracy:.1f}%")
        print(f"Hallucination Rate: {results['coverage'].hallucination_rate:.1f}%")
        
        pass_count = len([r for r in results['validation_results'] if r.status == 'PASS'])
        partial_count = len([r for r in results['validation_results'] if r.status == 'PARTIAL'])
        fail_count = len([r for r in results['validation_results'] if r.status == 'FAIL'])
        
        print(f"✅ Pass: {pass_count}")
        print(f"⚠️  Partial: {partial_count}")
        print(f"❌ Fail: {fail_count}")
        
        print("\n📄 GENERATING BASIC REPORTS:")
        print("-" * 40)
        
        # Generate report
        print("1. Generating basic validation report...")
        report_file = "../reports/CardDemo_Basic_Validation_Report.md"
        validator.generate_deepeval_report(report_file)
        print(f"   ✅ Basic report saved: {report_file}")
        
        # Generate text version
        print("2. Generating text report...")
        text_report_file = "../reports/CardDemo_Basic_Validation_Report.txt"
        validator.generate_deepeval_report(text_report_file)
        print(f"   ✅ Text report saved: {text_report_file}")
        
        print("\n🎉 BASIC VALIDATION COMPLETE!")
        print("=" * 60)
        print("Generated files:")
        print(f"   📄 {report_file}")
        print(f"   📝 {text_report_file}")
        
        print("\n💡 Basic Validation Features:")
        print("   • Component name validation")
        print("   • Architectural consistency checking")
        print("   • Keyword-based analysis")
        print("   • No external API dependencies")
        print("   • Fast execution")
        
        print("\n🔧 To enable DeepEval semantic analysis:")
        print("   • Set enable_deepeval=True in the validator initialization")
        print("   • Configure LLM API keys (OpenAI, Azure, Anthropic, or Google)")
        print("   • DeepEval runs locally but needs LLM provider for semantic analysis")
        
    except Exception as e:
        print(f"❌ Error during basic validation: {e}")
        logger.error(f"Basic validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
