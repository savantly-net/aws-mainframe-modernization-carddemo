#!/usr/bin/env python3
"""
CardDemo Analyzable Object Creator for G-Eval Framework

This module extracts and categorizes analyzable objects from requirements
for G-Eval validation and codebase comparison.

Author: Savantly
Date: 2025
"""

import json
import re
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalyzableObjectCreator:
    """
    Creates analyzable objects from requirements for G-Eval validation.
    """
    
    def __init__(self):
        """Initialize the analyzable object creator."""
        self.logger = logging.getLogger(__name__)
    
    def create_analyzable_objects(self, requirement_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and categorize analyzable objects from the requirement.
        
        Args:
            requirement_data: Dictionary containing requirement data
            
        Returns:
            Dictionary of categorized analyzable objects
        """
        user_story = requirement_data.get('requirement', {}).get('user_story', {})
        technical_requirements = requirement_data.get('requirement', {}).get('technical_requirements', [])
        
        analyzable_objects = {
            "business_rules": self._extract_business_rules(user_story),
            "technical_requirements": self._parse_technical_requirements(technical_requirements),
            "architecture_components": self._extract_architecture_components(user_story, technical_requirements),
            "integration_points": self._identify_integration_points(user_story, technical_requirements),
            "data_entities": self._extract_data_entities(user_story, technical_requirements),
            "validation_rules": self._extract_validation_rules(user_story, technical_requirements)
        }
        
        return analyzable_objects
    
    def _extract_business_rules(self, user_story: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract business rules from user story.
        
        Args:
            user_story: User story dictionary
            
        Returns:
            List of categorized business rules
        """
        business_rules = []
        
        # Extract business rules from user story
        if 'business_rules' in user_story:
            rules = user_story['business_rules']
            if isinstance(rules, list):
                for rule in rules:
                    business_rules.append({
                        "rule_text": rule,
                        "category": self._categorize_business_rule(rule),
                        "priority": self._assess_business_priority(rule),
                        "testable": self._is_testable_criteria(rule)
                    })
        
        return business_rules
    
    def _parse_technical_requirements(self, technical_requirements: List[str]) -> List[Dict[str, Any]]:
        """
        Parse technical requirements into individual analyzable requirements.
        
        Args:
            technical_requirements: List of technical requirement strings
            
        Returns:
            List of parsed technical requirements
        """
        parsed_requirements = []
        
        for req_text in technical_requirements:
            # Parse the large technical requirement text into individual requirements
            sections = req_text.split('\n\n')
            for section in sections:
                lines = section.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('**') or line.startswith('#'):
                        continue
                    if line.startswith('- ') and ':' in line and len(line.split(':')) == 2:
                        continue
                    if line.startswith('- '):
                        requirement = line[2:].strip()
                        if requirement and len(requirement) > 10:
                            parsed_requirements.append({
                                "requirement_text": requirement,
                                "category": self._categorize_technical_requirement(requirement),
                                "complexity": self._assess_technical_complexity(requirement),
                                "implementation_type": self._identify_implementation_type(requirement)
                            })
                    elif line and not any(line.startswith(f"{i}.") for i in range(1, 11)):
                        if len(line) > 10:
                            parsed_requirements.append({
                                "requirement_text": line,
                                "category": self._categorize_technical_requirement(line),
                                "complexity": self._assess_technical_complexity(line),
                                "implementation_type": self._identify_implementation_type(line)
                            })
        
        return parsed_requirements
    
    def _extract_architecture_components(self, user_story: Dict[str, Any], technical_requirements: List[str]) -> List[Dict[str, Any]]:
        """
        Extract architecture components from user story and technical requirements.
        
        Args:
            user_story: User story dictionary
            technical_requirements: List of technical requirement strings
            
        Returns:
            List of architecture components
        """
        components = []
        
        # Extract from user story
        story_text = f"{user_story.get('title', '')} {user_story.get('description', '')}"
        components.extend(self._identify_architecture_components(story_text))
        
        # Extract from technical requirements
        for req in technical_requirements:
            components.extend(self._identify_architecture_components(req))
        
        # Remove duplicates and categorize
        unique_components = []
        seen = set()
        for component in components:
            if component['name'] not in seen:
                seen.add(component['name'])
                unique_components.append(component)
        
        return unique_components
    
    def _identify_integration_points(self, user_story: Dict[str, Any], technical_requirements: List[str]) -> List[Dict[str, Any]]:
        """
        Identify integration points from user story and technical requirements.
        
        Args:
            user_story: User story dictionary
            technical_requirements: List of technical requirement strings
            
        Returns:
            List of integration points
        """
        integration_points = []
        
        # Extract from user story
        story_text = f"{user_story.get('title', '')} {user_story.get('description', '')}"
        integration_points.extend(self._find_integration_patterns(story_text))
        
        # Extract from technical requirements
        for req in technical_requirements:
            integration_points.extend(self._find_integration_patterns(req))
        
        return integration_points
    
    def _extract_data_entities(self, user_story: Dict[str, Any], technical_requirements: List[str]) -> List[Dict[str, Any]]:
        """
        Extract data entities from user story and technical requirements.
        
        Args:
            user_story: User story dictionary
            technical_requirements: List of technical requirement strings
            
        Returns:
            List of data entities
        """
        data_entities = []
        
        # Extract from user story
        story_text = f"{user_story.get('title', '')} {user_story.get('description', '')}"
        data_entities.extend(self._identify_data_entities(story_text))
        
        # Extract from technical requirements
        for req in technical_requirements:
            data_entities.extend(self._identify_data_entities(req))
        
        return data_entities
    
    def _extract_validation_rules(self, user_story: Dict[str, Any], technical_requirements: List[str]) -> List[Dict[str, Any]]:
        """
        Extract validation rules from user story and technical requirements.
        
        Args:
            user_story: User story dictionary
            technical_requirements: List of technical requirement strings
            
        Returns:
            List of validation rules
        """
        validation_rules = []
        
        # Extract from user story
        story_text = f"{user_story.get('title', '')} {user_story.get('description', '')}"
        validation_rules.extend(self._identify_validation_rules(story_text))
        
        # Extract from technical requirements
        for req in technical_requirements:
            validation_rules.extend(self._identify_validation_rules(req))
        
        return validation_rules
    
    # Helper methods for categorization and analysis
    
    def _categorize_business_rule(self, rule: str) -> str:
        """Categorize a business rule based on its content."""
        rule_lower = rule.lower()
        if any(word in rule_lower for word in ['must', 'required', 'mandatory']):
            return "mandatory"
        elif any(word in rule_lower for word in ['should', 'recommended', 'preferred']):
            return "recommended"
        elif any(word in rule_lower for word in ['cannot', 'forbidden', 'prohibited']):
            return "prohibited"
        else:
            return "informational"
    
    def _assess_business_priority(self, rule: str) -> str:
        """Assess the business priority of a rule."""
        rule_lower = rule.lower()
        if any(word in rule_lower for word in ['critical', 'essential', 'must']):
            return "high"
        elif any(word in rule_lower for word in ['important', 'should']):
            return "medium"
        else:
            return "low"
    
    def _is_testable_criteria(self, rule: str) -> bool:
        """Determine if a business rule is testable."""
        rule_lower = rule.lower()
        testable_indicators = ['must', 'should', 'cannot', 'required', 'valid', 'invalid', 'match', 'equal']
        return any(indicator in rule_lower for indicator in testable_indicators)
    
    def _categorize_technical_requirement(self, requirement: str) -> str:
        """Categorize a technical requirement."""
        req_lower = requirement.lower()
        if any(word in req_lower for word in ['database', 'db2', 'ims', 'vsam']):
            return "database"
        elif any(word in req_lower for word in ['cics', 'transaction', 'screen']):
            return "transaction_processing"
        elif any(word in req_lower for word in ['mq', 'message', 'queue']):
            return "messaging"
        elif any(word in req_lower for word in ['security', 'authentication', 'authorization']):
            return "security"
        elif any(word in req_lower for word in ['validation', 'verify', 'check']):
            return "validation"
        else:
            return "general"
    
    def _assess_technical_complexity(self, requirement: str) -> str:
        """Assess the technical complexity of a requirement."""
        req_lower = requirement.lower()
        complexity_indicators = ['complex', 'advanced', 'sophisticated', 'multiple', 'integration']
        simple_indicators = ['simple', 'basic', 'straightforward', 'single']
        
        if any(indicator in req_lower for indicator in complexity_indicators):
            return "high"
        elif any(indicator in req_lower for indicator in simple_indicators):
            return "low"
        else:
            return "medium"
    
    def _identify_implementation_type(self, requirement: str) -> str:
        """Identify the implementation type for a requirement."""
        req_lower = requirement.lower()
        if any(word in req_lower for word in ['cobol', 'program', 'module']):
            return "cobol_program"
        elif any(word in req_lower for word in ['jcl', 'job', 'batch']):
            return "jcl_job"
        elif any(word in req_lower for word in ['screen', 'bms', 'map']):
            return "screen_map"
        elif any(word in req_lower for word in ['database', 'table', 'schema']):
            return "database_object"
        else:
            return "general"
    
    def _identify_architecture_components(self, text: str) -> List[Dict[str, Any]]:
        """Identify architecture components in text."""
        components = []
        
        # Look for specific technology patterns
        patterns = {
            'cobol_program': r'\b[A-Z]{2,8}\d{2,3}[A-Z]?\b',  # COBOL program names
            'database': r'\b(db2|ims|vsam|database|table)\b',
            'transaction': r'\b(cics|transaction|screen)\b',
            'messaging': r'\b(mq|message|queue)\b',
            'security': r'\b(racf|security|authentication)\b'
        }
        
        for component_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                components.append({
                    "name": match.group(),
                    "type": component_type,
                    "context": text[max(0, match.start()-20):match.end()+20]
                })
        
        return components
    
    def _find_integration_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Find integration patterns in text."""
        integration_points = []
        
        # Look for integration patterns
        patterns = {
            'database_integration': r'\b(connect|query|insert|update|delete)\b.*\b(database|db2|ims|vsam)\b',
            'message_integration': r'\b(send|receive|put|get)\b.*\b(message|mq|queue)\b',
            'transaction_integration': r'\b(call|link|transfer)\b.*\b(transaction|program)\b',
            'external_integration': r'\b(ftp|http|api|web\s*service)\b'
        }
        
        for pattern_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                integration_points.append({
                    "type": pattern_type,
                    "description": match.group(),
                    "context": text[max(0, match.start()-30):match.end()+30]
                })
        
        return integration_points
    
    def _identify_data_entities(self, text: str) -> List[Dict[str, Any]]:
        """Identify data entities in text."""
        data_entities = []
        
        # Look for data entity patterns
        patterns = {
            'file': r'\b(file|dataset|ksds|esds|rrds)\b',
            'table': r'\b(table|segment|record)\b',
            'field': r'\b(field|column|attribute)\b',
            'data_structure': r'\b(copybook|record\s*layout|data\s*structure)\b'
        }
        
        for entity_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                data_entities.append({
                    "name": match.group(),
                    "type": entity_type,
                    "context": text[max(0, match.start()-20):match.end()+20]
                })
        
        return data_entities
    
    def _identify_validation_rules(self, text: str) -> List[Dict[str, Any]]:
        """Identify validation rules in text."""
        validation_rules = []
        
        # Look for validation patterns
        patterns = {
            'input_validation': r'\b(validate|check|verify)\b.*\b(input|field|data)\b',
            'business_validation': r'\b(must|should|cannot|required)\b',
            'format_validation': r'\b(format|pattern|structure)\b',
            'range_validation': r'\b(between|range|min|max)\b'
        }
        
        for rule_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                validation_rules.append({
                    "type": rule_type,
                    "rule": match.group(),
                    "context": text[max(0, match.start()-30):match.end()+30]
                })
        
        return validation_rules

def main():
    """Main function for testing the analyzable object creator."""
    # Example usage
    creator = AnalyzableObjectCreator()
    
    # Load a sample requirement (you would load this from your requirement extractor)
    sample_requirement = {
        "requirement": {
            "user_story": {
                "title": "Sample User Story",
                "description": "As a user, I want to authenticate securely",
                "business_rules": [
                    "User ID must not be empty",
                    "Password must be at least 8 characters"
                ]
            },
            "technical_requirements": [
                "The system must validate user credentials against RACF database",
                "CICS transaction COSGN00 must handle authentication"
            ]
        }
    }
    
    # Create analyzable objects
    analyzable_objects = creator.create_analyzable_objects(sample_requirement)
    
    # Print results
    print("Analyzable Objects Created:")
    for category, objects in analyzable_objects.items():
        print(f"\n{category.upper()}:")
        for obj in objects:
            print(f"  - {obj}")

if __name__ == "__main__":
    main()
