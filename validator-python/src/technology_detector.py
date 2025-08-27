#!/usr/bin/env python3
"""
CardDemo Technology Detector for G-Eval Framework

This module automatically detects the technology stack of a codebase
and configures appropriate patterns for G-Eval validation.

Author: Savantly
Date: 2025
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TechnologyDetector:
    """
    Automatically detects technology stack and configures analysis patterns.
    """

    def __init__(self, templates_file: str = "config/technology_templates.json"):
        """
        Initialize the technology detector.

        Args:
            templates_file: Path to the technology templates configuration file
        """
        self.templates_file = templates_file
        self.templates = self._load_templates()
        self.detection_config = self.templates.get('auto_detection', {})
        self.fallback_config = self.templates.get('fallback_config', {})

    def _load_templates(self) -> Dict[str, Any]:
        """Load technology templates from configuration file."""
        try:
            with open(self.templates_file, 'r') as f:
                templates = json.load(f)
            logger.info(f"Loaded technology templates from {self.templates_file}")
            return templates
        except Exception as e:
            logger.error(f"Error loading technology templates: {e}")
            raise

    def detect_technology_stack(self, codebase_root: str) -> Dict[str, Any]:
        """
        Detect the technology stack of the codebase.

        Args:
            codebase_root: Root directory of the codebase to analyze

        Returns:
            Dictionary containing detected technology and configuration
        """
        logger.info(f"Detecting technology stack for codebase: {codebase_root}")
        
        # Get all files in the codebase
        all_files = self._get_all_files(codebase_root)
        
        # Analyze using different detection methods
        detection_results = {}
        
        # Method 1: File extensions
        if self.detection_config.get('enabled', True):
            ext_results = self._detect_by_file_extensions(all_files)
            detection_results['file_extensions'] = ext_results
            
        # Method 2: Configuration files
        config_results = self._detect_by_configuration_files(all_files)
        detection_results['configuration_files'] = config_results
        
        # Method 3: Directory structure
        dir_results = self._detect_by_directory_structure(codebase_root)
        detection_results['directory_structure'] = dir_results
        
        # Calculate confidence scores
        confidence_scores = self._calculate_confidence_scores(detection_results)
        
        # Determine the best match
        best_match = self._determine_best_match(confidence_scores)
        
        # Get configuration for the detected technology
        if best_match:
            technology_config = self._get_technology_config(best_match['technology'])
            result = {
                'detected_technology': best_match['technology'],
                'confidence': best_match['confidence'],
                'detection_methods': detection_results,
                'configuration': technology_config,
                'fallback_used': False
            }
        else:
            # Use fallback configuration
            result = {
                'detected_technology': 'generic',
                'confidence': 0.0,
                'detection_methods': detection_results,
                'configuration': self.fallback_config,
                'fallback_used': True
            }
        
        logger.info(f"Technology detection complete: {result['detected_technology']} (confidence: {result['confidence']:.2f})")
        return result

    def _get_all_files(self, codebase_root: str) -> List[Path]:
        """Get all files in the codebase."""
        files = []
        try:
            for file_path in Path(codebase_root).rglob('*'):
                if file_path.is_file():
                    files.append(file_path)
            logger.info(f"Found {len(files)} files in codebase")
        except Exception as e:
            logger.error(f"Error scanning codebase: {e}")
        
        return files

    def _detect_by_file_extensions(self, files: List[Path]) -> Dict[str, float]:
        """Detect technology by analyzing file extensions."""
        extension_counts = {}
        
        for file_path in files:
            extension = file_path.suffix.lower()
            extension_counts[extension] = extension_counts.get(extension, 0) + 1
        
        # Match against known patterns
        detection_methods = self.detection_config.get('detection_methods', {})
        file_ext_patterns = detection_methods.get('file_extensions', {}).get('patterns', {})
        
        technology_scores = {}
        total_files = len(files)
        
        for technology, extensions in file_ext_patterns.items():
            score = 0
            for ext in extensions:
                if ext in extension_counts:
                    score += extension_counts[ext]
            
            if total_files > 0:
                technology_scores[technology] = score / total_files
            else:
                technology_scores[technology] = 0.0
        
        return technology_scores

    def _detect_by_configuration_files(self, files: List[Path]) -> Dict[str, float]:
        """Detect technology by looking for configuration files."""
        detection_methods = self.detection_config.get('detection_methods', {})
        config_patterns = detection_methods.get('configuration_files', {}).get('patterns', {})
        
        technology_scores = {}
        
        for technology, config_files in config_patterns.items():
            score = 0
            for config_file in config_files:
                for file_path in files:
                    if file_path.name == config_file or file_path.match(config_file):
                        score += 1
                        break  # Found this config file, move to next
            
            # Normalize score (0-1 range)
            max_possible = len(config_files)
            if max_possible > 0:
                technology_scores[technology] = score / max_possible
            else:
                technology_scores[technology] = 0.0
        
        return technology_scores

    def _detect_by_directory_structure(self, codebase_root: str) -> Dict[str, float]:
        """Detect technology by analyzing directory structure."""
        detection_methods = self.detection_config.get('detection_methods', {})
        dir_patterns = detection_methods.get('directory_structure', {}).get('patterns', {})
        
        technology_scores = {}
        
        for technology, dir_patterns_list in dir_patterns.items():
            score = 0
            for pattern in dir_patterns_list:
                if Path(codebase_root).glob(pattern):
                    score += 1
            
            # Normalize score (0-1 range)
            max_possible = len(dir_patterns_list)
            if max_possible > 0:
                technology_scores[technology] = score / max_possible
            else:
                technology_scores[technology] = 0.0
        
        return technology_scores

    def _calculate_confidence_scores(self, detection_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate confidence scores for each technology."""
        detection_methods = self.detection_config.get('detection_methods', {})
        weights = {
            'file_extensions': detection_methods.get('file_extensions', {}).get('weight', 0.3),
            'configuration_files': detection_methods.get('configuration_files', {}).get('weight', 0.4),
            'directory_structure': detection_methods.get('directory_structure', {}).get('weight', 0.3)
        }
        
        # Collect all unique technologies
        all_technologies = set()
        for method_results in detection_results.values():
            all_technologies.update(method_results.keys())
        
        # Calculate weighted scores
        technology_scores = []
        for technology in all_technologies:
            weighted_score = 0
            for method, weight in weights.items():
                if method in detection_results and technology in detection_results[method]:
                    weighted_score += detection_results[method][technology] * weight
            
            technology_scores.append({
                'technology': technology,
                'confidence': weighted_score,
                'method_scores': {
                    method: detection_results.get(method, {}).get(technology, 0)
                    for method in weights.keys()
                }
            })
        
        # Sort by confidence (highest first)
        technology_scores.sort(key=lambda x: x['confidence'], reverse=True)
        
        return technology_scores

    def _determine_best_match(self, confidence_scores: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Determine the best technology match based on confidence threshold."""
        threshold = self.detection_config.get('confidence_threshold', 0.7)
        
        if confidence_scores and confidence_scores[0]['confidence'] >= threshold:
            return confidence_scores[0]
        
        return None

    def _get_technology_config(self, technology: str) -> Dict[str, Any]:
        """Get configuration for the specified technology."""
        technology_templates = self.templates.get('technology_templates', {})
        
        if technology in technology_templates:
            return technology_templates[technology]
        else:
            logger.warning(f"Technology '{technology}' not found in templates, using fallback")
            return self.fallback_config

    def get_configured_patterns(self, detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get configured patterns for the detected technology.

        Args:
            detection_result: Result from detect_technology_stack()

        Returns:
            Dictionary containing configured patterns for analysis
        """
        config = detection_result['configuration']
        
        # Extract patterns from the configuration
        patterns = {
            'file_patterns': config.get('file_patterns', {}),
            'regex_patterns': config.get('regex_patterns', {}),
            'integration_points': config.get('integration_points', {}),
            'analysis_config': self._generate_analysis_config(config)
        }
        
        return patterns

    def _generate_analysis_config(self, technology_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis configuration from technology config."""
        analysis_config = {}
        
        file_patterns = technology_config.get('file_patterns', {})
        for pattern_type, pattern_config in file_patterns.items():
            analysis_type = pattern_config.get('analysis_type', 'generic_analysis')
            analysis_config[analysis_type] = {
                'enabled': True,
                'file_patterns': pattern_config.get('patterns', []),
                'directories': pattern_config.get('directories', []),
                'description': pattern_config.get('description', '')
            }
        
        return analysis_config

    def validate_detection(self, detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the detection result and provide recommendations.

        Args:
            detection_result: Result from detect_technology_stack()

        Returns:
            Validation result with recommendations
        """
        validation = {
            'is_valid': True,
            'confidence_level': 'high' if detection_result['confidence'] >= 0.8 else 'medium' if detection_result['confidence'] >= 0.6 else 'low',
            'recommendations': [],
            'warnings': []
        }
        
        # Check confidence level
        if detection_result['confidence'] < 0.5:
            validation['is_valid'] = False
            validation['warnings'].append("Low confidence in technology detection")
            validation['recommendations'].append("Consider manually specifying the technology stack")
        
        # Check if fallback was used
        if detection_result.get('fallback_used', False):
            validation['warnings'].append("Using generic fallback configuration")
            validation['recommendations'].append("Technology-specific patterns may not be optimal")
        
        # Check detection methods
        detection_methods = detection_result.get('detection_methods', {})
        if not detection_methods.get('configuration_files'):
            validation['warnings'].append("No configuration files detected")
            validation['recommendations'].append("Consider adding configuration files for better detection")
        
        return validation

def main():
    """Main function for testing the technology detector."""
    import sys
    
    # Get codebase path from command line or use current directory
    if len(sys.argv) > 1:
        codebase_path = sys.argv[1]
    else:
        codebase_path = str(Path.cwd())
    
    # Example usage
    detector = TechnologyDetector()
    
    logger.info(f"Testing technology detection on: {codebase_path}")
    
    # Detect technology
    detection_result = detector.detect_technology_stack(codebase_path)
    
    # Print results
    print(f"\nTechnology Detection Results:")
    print(f"Detected Technology: {detection_result['detected_technology']}")
    print(f"Confidence: {detection_result['confidence']:.2f}")
    print(f"Fallback Used: {detection_result['fallback_used']}")
    
    # Get configured patterns
    patterns = detector.get_configured_patterns(detection_result)
    print(f"\nConfigured Patterns:")
    print(f"File Pattern Types: {list(patterns['file_patterns'].keys())}")
    print(f"Regex Pattern Types: {list(patterns['regex_patterns'].keys())}")
    
    # Validate detection
    validation = detector.validate_detection(detection_result)
    print(f"\nValidation:")
    print(f"Valid: {validation['is_valid']}")
    print(f"Confidence Level: {validation['confidence_level']}")
    if validation['warnings']:
        print(f"Warnings: {validation['warnings']}")
    if validation['recommendations']:
        print(f"Recommendations: {validation['recommendations']}")

if __name__ == "__main__":
    main()
