#!/usr/bin/env python3
"""
CardDemo DeepEval Report Generator

This script orchestrates the DeepEval validation process and generates comprehensive reports
with semantic understanding and intelligent analysis of AI-generated requirements.

Key Features:
1. Semantic validation using DeepEval's LLM capabilities
2. Intelligent false positive detection
3. Context-aware component validation
4. Detailed improvement suggestions
5. Enhanced coverage analysis with hallucination detection

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
    Main function to run DeepEval validation and generate reports.
    """
    print("CardDemo DeepEval Requirements Validator - Enhanced Report Generator")
    print("=" * 70)
    
    # Check for command line arguments
    enable_deepeval = True
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['--no-deepeval', '--basic', '--disable-deepeval']:
            enable_deepeval = False
            print("🔧 Running in basic validation mode (DeepEval disabled)")
        elif sys.argv[1].lower() in ['--help', '-h']:
            print("Usage: python generate_deepeval_reports.py [--no-deepeval]")
            print("  --no-deepeval: Run in basic validation mode without DeepEval")
            print("  --help: Show this help message")
            sys.exit(0)
    
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
    
    print("🔍 Initializing DeepEval validator...")
    
    try:
        # Initialize the DeepEval validator
        validator = CardDemoDeepEvalValidator(
            requirements_file=requirements_file,
            codebase_path=codebase_path,
            llm_model="gpt-4o",  # You can change this to "claude-3-sonnet-20240229" or "gemini-pro"
            enable_deepeval=enable_deepeval  # Use command line argument
        )
        
        print("📊 Running DeepEval validation...")
        
        # Run the complete validation process
        print("   ⏳ This may take a few minutes...")
        results = validator.run_deepeval_validation()
        
        # Display validation summary
        print("\n📈 DEEPEVAL VALIDATION SUMMARY:")
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
        
        print("\n📄 GENERATING DEEPEVAL REPORTS:")
        print("-" * 40)
        
        # Generate DeepEval report
        print("1. Generating DeepEval report...")
        deepeval_report_file = "../reports/CardDemo_DeepEval_Validation_Report.md"
        validator.generate_deepeval_report(deepeval_report_file)
        print(f"   ✅ DeepEval report saved: {deepeval_report_file}")
        
        # Generate text version
        print("2. Generating text report...")
        text_report_file = "../reports/CardDemo_DeepEval_Validation_Report.txt"
        validator.generate_deepeval_report(text_report_file)
        print(f"   ✅ Text report saved: {text_report_file}")
        
        print("\n🎉 DEEPEVAL REPORT GENERATION COMPLETE!")
        print("=" * 70)
        print("Generated files:")
        print(f"   📄 {deepeval_report_file}")
        print(f"   📝 {text_report_file}")
        
        print("\n💡 Key DeepEval Improvements:")
        print("   • Semantic understanding of mainframe terminology")
        print("   • Intelligent false positive detection")
        print("   • Context-aware component validation")
        print("   • Detailed improvement suggestions")
        print("   • Hallucination detection and scoring")
        
        print("\n🔧 Next steps:")
        print("   • Review the DeepEval report for semantic insights")
        print("   • Focus on requirements with high hallucination scores")
        print("   • Implement improvement suggestions")
        print("   • Use semantic accuracy metrics for quality assessment")
        
    except Exception as e:
        print(f"❌ Error during DeepEval validation: {e}")
        logger.error(f"DeepEval validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
