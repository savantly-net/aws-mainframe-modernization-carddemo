#!/usr/bin/env python3
"""
CardDemo First User Story Extractor

This script extracts the first user story and its embedded technical requirements
from the CardDemo requirements JSON file, using the same logic as the deepeval_validator
for iterating through user stories.

Author: Savantly
Date: 2025
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CardDemoUserStoryExtractor:
    """
    Extractor that finds and extracts the first user story and its technical requirements
    from the CardDemo requirements JSON file.
    """
    
    def __init__(self, requirements_file: str):
        """
        Initialize the user story extractor.
        
        Args:
            requirements_file: Path to the JSON file containing AI-generated requirements
        """
        self.requirements_file = requirements_file
        self.requirements_data = None
        
    def load_requirements(self) -> None:
        """Load and parse the AI-generated requirements JSON file."""
        try:
            with open(self.requirements_file, 'r') as f:
                self.requirements_data = json.load(f)
            logger.info(f"Loaded requirements from {self.requirements_file}")
        except Exception as e:
            logger.error(f"Error loading requirements file: {e}")
            raise
    
    def _extract_user_stories(self) -> List[Dict[str, Any]]:
        """
        Extract user stories from the JSON structure using the same logic as deepeval_validator.
        """
        stories = []
        if 'data' in self.requirements_data and 'user_stories' in self.requirements_data['data']:
            stories = self.requirements_data['data']['user_stories']
        return stories
    
    def _extract_technical_requirements_from_story(self, story: Dict[str, Any]) -> List[str]:
        """
        Extract technical requirements from a user story using the same logic as deepeval_validator.
        """
        requirements = []
        
        def extract_from_section(section):
            if isinstance(section, dict):
                if 'technical_requirements' in section:
                    tech_req = section['technical_requirements']
                    if isinstance(tech_req, dict) and 'requirement' in tech_req:
                        requirements.append(tech_req['requirement'])
                for key, value in section.items():
                    extract_from_section(value)
            elif isinstance(section, list):
                for item in section:
                    extract_from_section(item)
        
        extract_from_section(story)
        return requirements
    
    def extract_first_user_story(self) -> Dict[str, Any]:
        """
        Extract the first user story and its embedded technical requirements.
        
        Returns:
            Dictionary containing the first user story with its technical requirements
        """
        # Load requirements
        self.load_requirements()
        
        # Extract user stories using the same logic as deepeval_validator
        user_stories = self._extract_user_stories()
        
        if not user_stories:
            logger.error("No user stories found in the requirements file")
            return {}
        
        # Get the first user story
        first_story = user_stories[0]
        logger.info(f"Found first user story: {first_story.get('title', 'No title')}")
        
        # Extract technical requirements from the first story
        technical_requirements = self._extract_technical_requirements_from_story(first_story)
        logger.info(f"Found {len(technical_requirements)} technical requirements in first user story")
        
        # Create the extracted data structure with ALL available fields separated into analyzable objects
        extracted_data = {
            'user_story': {
                'title': first_story.get('title', ''),
                'description': first_story.get('description', ''),
                'feature_name': first_story.get('feature_name', ''),
                'business_rules': first_story.get('business_rules', []),
                'acceptance_criteria': first_story.get('acceptance_criteria', []),
                'priority': first_story.get('priority', ''),
                'story_points': first_story.get('story_points', ''),
                'technical_requirements': technical_requirements
            },
            'deepeval_analysis': {
                'fields_used_by_deepeval': [
                    'title',
                    'description'
                ],
                'fields_ignored_by_deepeval': [
                    'feature_name',
                    'business_rules', 
                    'acceptance_criteria',
                    'priority',
                    'story_points',
                    'technical_requirements'
                ],
                'deepeval_validation_text': f"Title: {first_story.get('title', '')}\nDescription: {first_story.get('description', '')}"
            },
            # Separate analyzable objects for ignored fields
            'business_rules_analysis': {
                'rules': first_story.get('business_rules', []),
                'count': len(first_story.get('business_rules', [])),
                'categories': self._categorize_business_rules(first_story.get('business_rules', [])),
                'validation_focus': self._identify_validation_rules(first_story.get('business_rules', [])),
                'data_requirements': self._extract_data_requirements(first_story.get('business_rules', []))
            },
            'acceptance_criteria_analysis': {
                'criteria': first_story.get('acceptance_criteria', []),
                'count': len(first_story.get('acceptance_criteria', [])),
                'testable_requirements': self._identify_testable_criteria(first_story.get('acceptance_criteria', [])),
                'functional_requirements': self._extract_functional_requirements(first_story.get('acceptance_criteria', []))
            },
            'feature_analysis': {
                'feature_name': first_story.get('feature_name', ''),
                'feature_category': self._categorize_feature(first_story.get('feature_name', '')),
                'related_features': self._find_related_features(user_stories, first_story.get('feature_name', ''))
            },
            'priority_analysis': {
                'priority': first_story.get('priority', ''),
                'story_points': first_story.get('story_points', ''),
                'business_value': self._assess_business_value(first_story.get('priority', ''), first_story.get('story_points', '')),
                'effort_estimate': self._estimate_effort(first_story.get('story_points', ''))
            },
            'technical_requirements_analysis': {
                'requirements': technical_requirements,
                'count': len(technical_requirements),
                'parsed_requirements': self._parse_technical_requirements_text(technical_requirements),
                'parsed_count': len(self._parse_technical_requirements_text(technical_requirements)),
                'architecture_components': self._extract_architecture_components(technical_requirements),
                'integration_points': self._identify_integration_points(technical_requirements),
                'data_entities': self._extract_data_entities(technical_requirements),
                'validation_rules': self._extract_technical_validation_rules(technical_requirements)
            },
            'metadata': {
                'source_file': self.requirements_file,
                'extraction_method': 'Same logic as deepeval_validator._extract_user_stories()',
                'total_user_stories_in_file': len(user_stories),
                'technical_requirements_count': len(technical_requirements),
                'parsed_technical_requirements_count': len(self._parse_technical_requirements_text(technical_requirements)),
                'business_rules_count': len(first_story.get('business_rules', [])),
                'acceptance_criteria_count': len(first_story.get('acceptance_criteria', []))
            }
        }
        
        return extracted_data
    
    def _categorize_business_rules(self, business_rules: List[str]) -> Dict[str, List[str]]:
        """Categorize business rules by type."""
        categories = {
            'validation_rules': [],
            'data_rules': [],
            'process_rules': [],
            'security_rules': [],
            'audit_rules': [],
            'other': []
        }
        
        for rule in business_rules:
            rule_lower = rule.lower()
            if any(word in rule_lower for word in ['validate', 'check', 'ensure', 'must be']):
                categories['validation_rules'].append(rule)
            elif any(word in rule_lower for word in ['store', 'database', 'table', 'file', 'data']):
                categories['data_rules'].append(rule)
            elif any(word in rule_lower for word in ['process', 'workflow', 'transaction', 'real-time']):
                categories['process_rules'].append(rule)
            elif any(word in rule_lower for word in ['security', 'fraud', 'authorization', 'access']):
                categories['security_rules'].append(rule)
            elif any(word in rule_lower for word in ['log', 'audit', 'record', 'track']):
                categories['audit_rules'].append(rule)
            else:
                categories['other'].append(rule)
        
        return categories
    
    def _identify_validation_rules(self, business_rules: List[str]) -> List[str]:
        """Extract validation-specific business rules."""
        validation_rules = []
        for rule in business_rules:
            if any(word in rule.lower() for word in ['validate', 'check', 'ensure', 'must be', 'format', 'length']):
                validation_rules.append(rule)
        return validation_rules
    
    def _extract_data_requirements(self, business_rules: List[str]) -> List[str]:
        """Extract data-related requirements from business rules."""
        data_requirements = []
        for rule in business_rules:
            if any(word in rule.lower() for word in ['store', 'database', 'table', 'file', 'data', 'save']):
                data_requirements.append(rule)
        return data_requirements
    
    def _identify_testable_criteria(self, acceptance_criteria: List[str]) -> List[str]:
        """Identify acceptance criteria that can be tested."""
        testable = []
        for criterion in acceptance_criteria:
            if any(word in criterion.lower() for word in ['should', 'must', 'will', 'can', 'able to']):
                testable.append(criterion)
        return testable
    
    def _extract_functional_requirements(self, acceptance_criteria: List[str]) -> List[str]:
        """Extract functional requirements from acceptance criteria."""
        functional = []
        for criterion in acceptance_criteria:
            if any(word in criterion.lower() for word in ['function', 'feature', 'capability', 'ability']):
                functional.append(criterion)
        return functional
    
    def _categorize_feature(self, feature_name: str) -> str:
        """Categorize the feature based on its name."""
        feature_lower = feature_name.lower()
        if 'authorization' in feature_lower:
            return 'Transaction Processing'
        elif 'management' in feature_lower:
            return 'Administrative'
        elif 'report' in feature_lower:
            return 'Reporting'
        elif 'inquiry' in feature_lower:
            return 'Data Access'
        elif 'fraud' in feature_lower:
            return 'Security'
        elif 'integration' in feature_lower:
            return 'System Integration'
        else:
            return 'Other'
    
    def _find_related_features(self, all_stories: List[Dict[str, Any]], current_feature: str) -> List[str]:
        """Find other user stories with the same feature name."""
        related = []
        for story in all_stories:
            if story.get('feature_name') == current_feature and story.get('title') != all_stories[0].get('title'):
                related.append(story.get('title', ''))
        return related
    
    def _assess_business_value(self, priority: str, story_points: str) -> str:
        """Assess the business value based on priority and story points."""
        if priority and story_points:
            return f"Priority: {priority}, Effort: {story_points} points"
        elif priority:
            return f"Priority: {priority}"
        elif story_points:
            return f"Effort: {story_points} points"
        else:
            return "Not specified"
    
    def _estimate_effort(self, story_points: str) -> str:
        """Estimate effort based on story points."""
        if not story_points:
            return "Not specified"
        try:
            points = int(story_points)
            if points <= 3:
                return "Low effort"
            elif points <= 8:
                return "Medium effort"
            else:
                return "High effort"
        except ValueError:
            return "Invalid story points format"
    
    def _parse_technical_requirements_text(self, technical_requirements: List[str]) -> List[str]:
        """
        Parse the large technical requirements text into individual analyzable requirements.
        """
        parsed_requirements = []
        
        for req_text in technical_requirements:
            # Split by numbered sections (1., 2., 3., etc.)
            sections = req_text.split('\n\n')
            
            for section in sections:
                # Remove section headers and extract individual requirements
                lines = section.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    
                    # Skip empty lines and section headers
                    if not line or line.startswith('**') or line.startswith('#'):
                        continue
                    
                    # Skip bullet points that are just labels
                    if line.startswith('- ') and ':' in line and len(line.split(':')) == 2:
                        continue
                    
                    # Extract actual requirements
                    if line.startswith('- '):
                        # Remove bullet point and clean up
                        requirement = line[2:].strip()
                        if requirement and len(requirement) > 10:  # Filter out very short items
                            parsed_requirements.append(requirement)
                    elif line and not line.startswith('1.') and not line.startswith('2.') and not line.startswith('3.') and not line.startswith('4.') and not line.startswith('5.') and not line.startswith('6.') and not line.startswith('7.') and not line.startswith('8.') and not line.startswith('9.') and not line.startswith('10.'):
                        # Handle non-bullet point requirements
                        if len(line) > 10:  # Filter out very short items
                            parsed_requirements.append(line)
        
        return parsed_requirements

    def _extract_architecture_components(self, technical_requirements: List[str]) -> List[str]:
        """Extract architecture components mentioned in technical requirements."""
        components = []
        for req in technical_requirements:
            req_lower = req.lower()
            if 'ims' in req_lower:
                components.append('IMS DB')
            if 'db2' in req_lower:
                components.append('DB2')
            if 'mq' in req_lower:
                components.append('MQ')
            if 'cics' in req_lower:
                components.append('CICS')
            if 'cobol' in req_lower:
                components.append('COBOL')
            if 'bms' in req_lower:
                components.append('BMS')
            if 'jcl' in req_lower:
                components.append('JCL')
        return list(set(components))
    
    def _identify_integration_points(self, technical_requirements: List[str]) -> List[str]:
        """Identify integration points mentioned in technical requirements."""
        integration_points = []
        for req in technical_requirements:
            req_lower = req.lower()
            # Look for specific integration patterns
            if 'mq' in req_lower and ('queue' in req_lower or 'message' in req_lower):
                integration_points.append("MQ Message Queues")
            if 'cics' in req_lower and 'transaction' in req_lower:
                integration_points.append("CICS Transactions")
            if 'bms' in req_lower and 'screen' in req_lower:
                integration_points.append("BMS Screen Interface")
            if 'ims' in req_lower and 'db' in req_lower:
                integration_points.append("IMS Database")
            if 'db2' in req_lower:
                integration_points.append("DB2 Database")
        return list(set(integration_points))
    
    def _extract_data_entities(self, technical_requirements: List[str]) -> List[str]:
        """Extract data entities mentioned in technical requirements."""
        entities = []
        for req in technical_requirements:
            req_lower = req.lower()
            # Look for specific data entity patterns
            if 'authfrds' in req_lower:
                entities.append("AUTHFRDS table (DB2)")
            if 'pa_authorization_details' in req_lower:
                entities.append("PA_AUTHORIZATION_DETAILS segment (IMS)")
            if 'table' in req_lower and 'db2' in req_lower:
                entities.append("DB2 Tables")
            if 'segment' in req_lower and 'ims' in req_lower:
                entities.append("IMS Segments")
            if 'file' in req_lower and 'vsam' in req_lower:
                entities.append("VSAM Files")
        return list(set(entities))
    
    def _extract_technical_validation_rules(self, technical_requirements: List[str]) -> List[str]:
        """Extract technical validation rules from requirements."""
        validation_rules = []
        for req in technical_requirements:
            req_lower = req.lower()
            # Look for specific validation patterns
            if 'validate credit card number' in req_lower:
                validation_rules.append("Credit card number format validation")
            if 'validate transaction amount' in req_lower:
                validation_rules.append("Transaction amount validation")
            if 'check expired cards' in req_lower:
                validation_rules.append("Card expiration validation")
            if 'detect potential fraud' in req_lower:
                validation_rules.append("Fraud detection validation")
            if 'validate' in req_lower and 'format' in req_lower:
                validation_rules.append("Data format validation")
            if 'validate' in req_lower and 'length' in req_lower:
                validation_rules.append("Data length validation")
        return list(set(validation_rules))
    
    def save_extracted_story(self, output_file: str, extracted_data: Dict[str, Any]) -> None:
        """
        Save the extracted user story to a JSON file.
        
        Args:
            output_file: Path to save the extracted user story
            extracted_data: The extracted user story data
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Extracted user story saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving extracted user story: {e}")
            raise
    
    def generate_markdown_report(self, extracted_data: Dict[str, Any], output_file: str = None) -> str:
        """
        Generate a markdown report of the extracted user story.
        
        Args:
            extracted_data: The extracted user story data
            output_file: Optional path to save the markdown report
            
        Returns:
            The markdown report as a string
        """
        report = []
        
        # Report header
        report.append("# CardDemo First User Story - Enhanced Analysis Report")
        report.append("")
        report.append(f"**Generated:** {self._get_timestamp()}")
        report.append(f"**Source:** {extracted_data['metadata']['source_file']}")
        report.append(f"**Extraction Method:** {extracted_data['metadata']['extraction_method']}")
        report.append("")
        report.append("---")
        report.append("")
        
        # User story details
        story = extracted_data['user_story']
        report.append("## User Story Details")
        report.append("")
        report.append(f"**Title:** {story['title']}")
        report.append("")
        report.append(f"**Description:** {story['description']}")
        report.append("")
        
        if story.get('feature_name'):
            report.append(f"**Feature Name:** {story['feature_name']}")
            report.append("")
        
        if story.get('priority'):
            report.append(f"**Priority:** {story['priority']}")
            report.append("")
        
        if story.get('story_points'):
            report.append(f"**Story Points:** {story['story_points']}")
            report.append("")
        
        # DeepEval Analysis Section
        report.append("## DeepEval Analysis")
        report.append("")
        report.append("### Fields Used by DeepEval Validator")
        report.append("")
        for field in extracted_data['deepeval_analysis']['fields_used_by_deepeval']:
            report.append(f"- **{field}**: {story.get(field, 'N/A')}")
        report.append("")
        
        report.append("### Fields Ignored by DeepEval Validator")
        report.append("")
        for field in extracted_data['deepeval_analysis']['fields_ignored_by_deepeval']:
            if field == 'business_rules' and story.get('business_rules'):
                report.append(f"- **{field}**: {len(story['business_rules'])} rules (see analysis below)")
            elif field == 'acceptance_criteria' and story.get('acceptance_criteria'):
                report.append(f"- **{field}**: {len(story['acceptance_criteria'])} criteria (see analysis below)")
            elif field == 'technical_requirements' and story.get('technical_requirements'):
                report.append(f"- **{field}**: {len(story['technical_requirements'])} requirements (see analysis below)")
            else:
                report.append(f"- **{field}**: {story.get(field, 'N/A')}")
        report.append("")
        
        report.append("### DeepEval Validation Text")
        report.append("")
        report.append("This is the exact text sent to DeepEval for validation:")
        report.append("")
        report.append("```")
        report.append(extracted_data['deepeval_analysis']['deepeval_validation_text'])
        report.append("```")
        report.append("")
        
        # Business Rules Analysis
        if extracted_data['business_rules_analysis']['rules']:
            report.append("## Business Rules Analysis")
            report.append("")
            report.append(f"**Total Rules:** {extracted_data['business_rules_analysis']['count']}")
            report.append("")
            
            # Categorized rules
            for category, rules in extracted_data['business_rules_analysis']['categories'].items():
                if rules:
                    report.append(f"### {category.replace('_', ' ').title()}")
                    report.append("")
                    for i, rule in enumerate(rules, 1):
                        report.append(f"{i}. {rule}")
                    report.append("")
            
            # Validation rules
            if extracted_data['business_rules_analysis']['validation_focus']:
                report.append("### Validation-Focused Rules")
                report.append("")
                for i, rule in enumerate(extracted_data['business_rules_analysis']['validation_focus'], 1):
                    report.append(f"{i}. {rule}")
                report.append("")
        
        # Acceptance Criteria Analysis
        if extracted_data['acceptance_criteria_analysis']['criteria']:
            report.append("## Acceptance Criteria Analysis")
            report.append("")
            report.append(f"**Total Criteria:** {extracted_data['acceptance_criteria_analysis']['count']}")
            report.append("")
            
            for i, criterion in enumerate(extracted_data['acceptance_criteria_analysis']['criteria'], 1):
                report.append(f"{i}. {criterion}")
            report.append("")
            
            if extracted_data['acceptance_criteria_analysis']['testable_requirements']:
                report.append("### Testable Requirements")
                report.append("")
                for i, req in enumerate(extracted_data['acceptance_criteria_analysis']['testable_requirements'], 1):
                    report.append(f"{i}. {req}")
                report.append("")
        
        # Feature Analysis
        if extracted_data['feature_analysis']['feature_name']:
            report.append("## Feature Analysis")
            report.append("")
            report.append(f"**Feature Name:** {extracted_data['feature_analysis']['feature_name']}")
            report.append(f"**Category:** {extracted_data['feature_analysis']['feature_category']}")
            report.append("")
            
            if extracted_data['feature_analysis']['related_features']:
                report.append("### Related Features")
                report.append("")
                for i, feature in enumerate(extracted_data['feature_analysis']['related_features'], 1):
                    report.append(f"{i}. {feature}")
                report.append("")
        
        # Priority Analysis
        if extracted_data['priority_analysis']['priority'] or extracted_data['priority_analysis']['story_points']:
            report.append("## Priority & Effort Analysis")
            report.append("")
            report.append(f"**Business Value:** {extracted_data['priority_analysis']['business_value']}")
            report.append(f"**Effort Estimate:** {extracted_data['priority_analysis']['effort_estimate']}")
            report.append("")
        
        # Technical Requirements Analysis
        if extracted_data['technical_requirements_analysis']['requirements']:
            report.append("## Technical Requirements Analysis")
            report.append("")
            report.append(f"**Total Requirements:** {extracted_data['technical_requirements_analysis']['count']}")
            report.append("")
            
            # Architecture components
            if extracted_data['technical_requirements_analysis']['architecture_components']:
                report.append("### Architecture Components")
                report.append("")
                for component in extracted_data['technical_requirements_analysis']['architecture_components']:
                    report.append(f"- {component}")
                report.append("")
            
            # Integration points
            if extracted_data['technical_requirements_analysis']['integration_points']:
                report.append("### Integration Points")
                report.append("")
                for i, point in enumerate(extracted_data['technical_requirements_analysis']['integration_points'], 1):
                    report.append(f"{i}. {point}")
                report.append("")
            
            # Data entities
            if extracted_data['technical_requirements_analysis']['data_entities']:
                report.append("### Data Entities")
                report.append("")
                for i, entity in enumerate(extracted_data['technical_requirements_analysis']['data_entities'], 1):
                    report.append(f"{i}. {entity}")
                report.append("")
            
            # Technical validation rules
            if extracted_data['technical_requirements_analysis']['validation_rules']:
                report.append("### Technical Validation Rules")
                report.append("")
                for i, rule in enumerate(extracted_data['technical_requirements_analysis']['validation_rules'], 1):
                    report.append(f"{i}. {rule}")
                report.append("")
            
            # Full technical requirements
            report.append("### Complete Technical Requirements")
            report.append("")
            for i, requirement in enumerate(extracted_data['technical_requirements_analysis']['requirements'], 1):
                report.append(f"#### Technical Requirement {i}")
                report.append("")
                report.append(requirement)
                report.append("")
        
        # Metadata
        report.append("## Extraction Metadata")
        report.append("")
        metadata = extracted_data['metadata']
        report.append(f"- **Source File:** {metadata['source_file']}")
        report.append(f"- **Extraction Method:** {metadata['extraction_method']}")
        report.append(f"- **Total User Stories in File:** {metadata['total_user_stories_in_file']}")
        report.append(f"- **Technical Requirements Count:** {metadata['technical_requirements_count']}")
        report.append(f"- **Business Rules Count:** {metadata['business_rules_count']}")
        report.append(f"- **Acceptance Criteria Count:** {metadata['acceptance_criteria_count']}")
        report.append("")
        
        # Report footer
        report.append("---")
        report.append("")
        report.append("*Report generated by Enhanced CardDemo User Story Extractor*")
        
        # Combine all report sections
        report_text = "\n".join(report)
        
        # Save to file if output path provided
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            logger.info(f"Enhanced markdown report saved to {output_file}")
        
        return report_text
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in a readable format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """Main entry point for user story extractor."""
    if len(sys.argv) != 2:
        print("Usage: python extract_first_user_story.py <requirements.json>")
        sys.exit(1)
    
    requirements_file = sys.argv[1]
    
    if not os.path.exists(requirements_file):
        print(f"Error: Requirements file {requirements_file} not found")
        sys.exit(1)
    
    # Initialize and run the extractor
    extractor = CardDemoUserStoryExtractor(requirements_file)
    
    try:
        # Extract the first user story
        print("Extracting first user story with enhanced analysis...")
        extracted_data = extractor.extract_first_user_story()
        
        if not extracted_data:
            print("No user story data extracted")
            sys.exit(1)
        
        # Save as JSON
        json_output_file = "first_user_story_enhanced.json"
        extractor.save_extracted_story(json_output_file, extracted_data)
        
        # Generate and save markdown report
        markdown_output_file = "first_user_story_enhanced_report.md"
        report = extractor.generate_markdown_report(extracted_data, markdown_output_file)
        
        # Display summary
        story = extracted_data['user_story']
        print("\n" + "=" * 60)
        print("ENHANCED USER STORY EXTRACTION COMPLETE")
        print("=" * 60)
        print(f"Title: {story['title']}")
        print(f"Feature Name: {story.get('feature_name', 'N/A')}")
        print(f"Technical Requirements: {len(story['technical_requirements'])}")
        print(f"Business Rules: {len(story.get('business_rules', []))}")
        print(f"Acceptance Criteria: {len(story.get('acceptance_criteria', []))}")
        print(f"JSON Output: {json_output_file}")
        print(f"Markdown Report: {markdown_output_file}")
        print("\n" + "=" * 60)
        print("ANALYSIS BREAKDOWN:")
        print("=" * 60)
        print(f"Business Rules Categories: {len(extracted_data['business_rules_analysis']['categories'])}")
        print(f"Architecture Components: {len(extracted_data['technical_requirements_analysis']['architecture_components'])}")
        print(f"Integration Points: {len(extracted_data['technical_requirements_analysis']['integration_points'])}")
        print(f"Data Entities: {len(extracted_data['technical_requirements_analysis']['data_entities'])}")
        print(f"Technical Validation Rules: {len(extracted_data['technical_requirements_analysis']['validation_rules'])}")
        print("\n" + "=" * 60)
        print("DEEPEVAL ANALYSIS:")
        print("=" * 60)
        print("Fields USED by DeepEval:")
        for field in extracted_data['deepeval_analysis']['fields_used_by_deepeval']:
            print(f"  - {field}")
        print("\nFields IGNORED by DeepEval (now separately analyzed):")
        for field in extracted_data['deepeval_analysis']['fields_ignored_by_deepeval']:
            print(f"  - {field}")
        
    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
