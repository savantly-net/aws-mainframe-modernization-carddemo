#!/usr/bin/env python3
"""
Comprehensive Requirements Extractor for G-Eval Framework

This module extracts ALL sections from the CardDemo requirements JSON file
and creates analyzable objects for comprehensive validation.

Author: Savantly
Date: 2025
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveExtractor:
    """
    Extracts all sections from the CardDemo requirements JSON file
    for comprehensive G-Eval validation.
    """
    
    def __init__(self, requirements_file: str):
        """
        Initialize the comprehensive extractor.
        
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
    
    def extract_all_sections(self) -> Dict[str, Any]:
        """
        Extract all sections from the requirements JSON.
        
        Returns:
            Dictionary containing all extracted sections with metadata
        """
        self.load_requirements()
        
        data = self.requirements_data.get('data', {})
        
        extraction_result = {
            "metadata": {
                "extraction_date": str(Path.cwd()),
                "source_file": self.requirements_file,
                "total_sections": 0,
                "sections_extracted": []
            },
            "sections": {}
        }
        
        # Extract each major section
        sections_to_extract = [
            'user_stories',
            'data_models', 
            'user_interface',
            'integration_points',
            'system_architecture',
            'security_considerations',
            'interface_specifications'
        ]
        
        for section_name in sections_to_extract:
            if section_name in data:
                logger.info(f"Extracting section: {section_name}")
                section_data = data[section_name]
                extracted_section = self._extract_section(section_name, section_data)
                
                if extracted_section:
                    extraction_result["sections"][section_name] = extracted_section
                    extraction_result["metadata"]["sections_extracted"].append(section_name)
                    extraction_result["metadata"]["total_sections"] += 1
        
        logger.info(f"Extracted {extraction_result['metadata']['total_sections']} sections")
        return extraction_result
    
    def _extract_section(self, section_name: str, section_data: Any) -> Dict[str, Any]:
        """
        Extract a specific section and create analyzable objects.
        
        Args:
            section_name: Name of the section being extracted
            section_data: Raw data for the section
            
        Returns:
            Dictionary containing extracted section with analyzable objects
        """
        extraction_methods = {
            'user_stories': self._extract_user_stories,
            'data_models': self._extract_data_models,
            'user_interface': self._extract_user_interface,
            'integration_points': self._extract_integration_points,
            'system_architecture': self._extract_system_architecture,
            'security_considerations': self._extract_security_considerations,
            'interface_specifications': self._extract_interface_specifications
        }
        
        if section_name in extraction_methods:
            return extraction_methods[section_name](section_data)
        else:
            logger.warning(f"No extraction method for section: {section_name}")
            return {"raw_data": section_data, "analyzable_objects": []}
    
    def _extract_user_stories(self, user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract user stories and create analyzable objects."""
        analyzable_objects = []
        
        for i, story in enumerate(user_stories):
            story_objects = {
                "story_id": i,
                "title": story.get('title', ''),
                "description": story.get('description', ''),
                "feature_name": story.get('feature_name', ''),
                "business_rules": story.get('business_rules', []),
                "technical_requirements": self._extract_technical_requirements(story.get('technical_requirements', {})),
                "priority": story.get('priority', 'Medium'),
                "story_points": story.get('story_points', 0),
                "acceptance_criteria": story.get('acceptance_criteria', [])
            }
            analyzable_objects.append(story_objects)
        
        return {
            "section_type": "user_stories",
            "total_count": len(user_stories),
            "analyzable_objects": analyzable_objects,
            "extraction_metadata": {
                "business_rules_count": sum(len(obj.get('business_rules', [])) for obj in analyzable_objects),
                "technical_requirements_count": sum(len(obj.get('technical_requirements', [])) for obj in analyzable_objects),
                "features_identified": len(set(obj.get('feature_name', '') for obj in analyzable_objects if obj.get('feature_name')))
            }
        }
    
    def _extract_technical_requirements(self, tech_req: Dict[str, Any]) -> List[str]:
        """Extract and parse technical requirements into individual requirements."""
        requirements = []
        
        if isinstance(tech_req, dict) and 'requirement' in tech_req:
            req_text = tech_req['requirement']
            # Parse the large requirement text into individual requirements
            requirements = self._parse_technical_requirements_text([req_text])
        
        return requirements
    
    def _parse_technical_requirements_text(self, technical_requirements: List[str]) -> List[str]:
        """Parse technical requirements text into individual requirements."""
        parsed_requirements = []
        
        for req_text in technical_requirements:
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
                            parsed_requirements.append(requirement)
                    elif line and not any(line.startswith(f"{i}.") for i in range(1, 11)):
                        if len(line) > 10:
                            parsed_requirements.append(line)
        
        return parsed_requirements
    
    def _extract_data_models(self, data_models: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data models and create analyzable objects."""
        analyzable_objects = []
        
        if 'entities' in data_models:
            entities = data_models['entities']
            for entity in entities:
                entity_object = {
                    "entity_name": entity.get('name', ''),
                    "attributes": entity.get('attributes', []),
                    "description": entity.get('description', ''),
                    "relationships": entity.get('relationships', []),
                    "entity_type": "database_entity"
                }
                analyzable_objects.append(entity_object)
        
        return {
            "section_type": "data_models",
            "total_count": len(analyzable_objects),
            "analyzable_objects": analyzable_objects,
            "extraction_metadata": {
                "entities_count": len(analyzable_objects),
                "total_attributes": sum(len(obj.get('attributes', [])) for obj in analyzable_objects),
                "total_relationships": sum(len(obj.get('relationships', [])) for obj in analyzable_objects)
            }
        }
    
    def _extract_user_interface(self, user_interface: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user interface specifications and create analyzable objects."""
        analyzable_objects = []
        
        # Handle error case
        if 'error' in user_interface:
            analyzable_objects.append({
                "ui_type": "error",
                "error_message": user_interface['error'],
                "status": "failed_generation"
            })
        else:
            # Extract UI components if available
            for key, value in user_interface.items():
                if key != 'error':
                    ui_object = {
                        "ui_component": key,
                        "specifications": value,
                        "ui_type": "interface_component"
                    }
                    analyzable_objects.append(ui_object)
        
        return {
            "section_type": "user_interface",
            "total_count": len(analyzable_objects),
            "analyzable_objects": analyzable_objects,
            "extraction_metadata": {
                "ui_components_count": len(analyzable_objects),
                "generation_status": "failed" if 'error' in user_interface else "success"
            }
        }
    
    def _extract_integration_points(self, integration_points: Dict[str, Any]) -> Dict[str, Any]:
        """Extract integration points and create analyzable objects."""
        analyzable_objects = []
        
        if 'external_systems' in integration_points:
            external_systems = integration_points['external_systems']
            for system in external_systems:
                system_object = {
                    "system_name": system.get('name', ''),
                    "description": system.get('description', ''),
                    "integration_type": system.get('type', ''),
                    "endpoints": system.get('endpoints', []),
                    "protocol": system.get('protocol', ''),
                    "authentication": system.get('authentication', ''),
                    "integration_type": "external_system"
                }
                analyzable_objects.append(system_object)
        
        return {
            "section_type": "integration_points",
            "total_count": len(analyzable_objects),
            "analyzable_objects": analyzable_objects,
            "extraction_metadata": {
                "external_systems_count": len(analyzable_objects),
                "total_endpoints": sum(len(obj.get('endpoints', [])) for obj in analyzable_objects)
            }
        }
    
    def _extract_system_architecture(self, system_architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Extract system architecture and create analyzable objects."""
        analyzable_objects = []
        
        if 'components' in system_architecture:
            components = system_architecture['components']
            for component in components:
                component_object = {
                    "component_name": component.get('name', ''),
                    "description": component.get('description', ''),
                    "responsibilities": component.get('responsibilities', []),
                    "dependencies": component.get('dependencies', []),
                    "component_type": "system_component"
                }
                analyzable_objects.append(component_object)
        
        return {
            "section_type": "system_architecture",
            "total_count": len(analyzable_objects),
            "analyzable_objects": analyzable_objects,
            "extraction_metadata": {
                "components_count": len(analyzable_objects),
                "total_responsibilities": sum(len(obj.get('responsibilities', [])) for obj in analyzable_objects)
            }
        }
    
    def _extract_security_considerations(self, security: Dict[str, Any]) -> Dict[str, Any]:
        """Extract security considerations and create analyzable objects."""
        analyzable_objects = []
        
        security_categories = ['authorization', 'authentication', 'data_protection']
        
        for category in security_categories:
            if category in security:
                category_data = security[category]
                if isinstance(category_data, list):
                    for item in category_data:
                        if isinstance(item, dict):
                            security_object = {
                                "security_category": category,
                                "requirement": item.get('requirement', ''),
                                "description": item.get('description', ''),
                                "implementation": item.get('implementation', ''),
                                "security_type": category
                            }
                        else:
                            security_object = {
                                "security_category": category,
                                "requirement": str(item),
                                "description": "",
                                "implementation": "",
                                "security_type": category
                            }
                        analyzable_objects.append(security_object)
                elif isinstance(category_data, dict):
                    security_object = {
                        "security_category": category,
                        "specifications": category_data,
                        "security_type": category
                    }
                    analyzable_objects.append(security_object)
        
        return {
            "section_type": "security_considerations",
            "total_count": len(analyzable_objects),
            "analyzable_objects": analyzable_objects,
            "extraction_metadata": {
                "security_categories_count": len(set(obj.get('security_category', '') for obj in analyzable_objects)),
                "total_security_requirements": len(analyzable_objects)
            }
        }
    
    def _extract_interface_specifications(self, interface_specs: Dict[str, Any]) -> Dict[str, Any]:
        """Extract interface specifications and create analyzable objects."""
        analyzable_objects = []
        
        if 'interface_types' in interface_specs:
            interface_types = interface_specs['interface_types']
            for interface_type in interface_types:
                if isinstance(interface_type, dict):
                    interface_object = {
                        "interface_name": interface_type.get('name', ''),
                        "description": interface_type.get('description', ''),
                        "specifications": interface_type.get('specifications', {}),
                        "interface_type": "api_interface"
                    }
                else:
                    interface_object = {
                        "interface_name": str(interface_type),
                        "description": "",
                        "specifications": {},
                        "interface_type": "api_interface"
                    }
                analyzable_objects.append(interface_object)
        
        return {
            "section_type": "interface_specifications",
            "total_count": len(analyzable_objects),
            "analyzable_objects": analyzable_objects,
            "extraction_metadata": {
                "interface_types_count": len(analyzable_objects)
            }
        }
    
    def save_extraction_result(self, extraction_result: Dict[str, Any], output_file: str) -> None:
        """Save the extraction result to a JSON file."""
        try:
            with open(output_file, 'w') as f:
                json.dump(extraction_result, f, indent=2)
            logger.info(f"Saved comprehensive extraction result to {output_file}")
        except Exception as e:
            logger.error(f"Error saving extraction result: {e}")
            raise

def main():
    """Main function for testing the comprehensive extractor."""
    import sys
    
    # Get requirements file path from command line or use default
    requirements_file = sys.argv[1] if len(sys.argv) > 1 else "data/CD-Requirements.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "comprehensive_extraction_result.json"
    
    # Create extractor and extract all sections
    extractor = ComprehensiveExtractor(requirements_file)
    
    logger.info(f"Starting comprehensive extraction from {requirements_file}")
    
    # Extract all sections
    extraction_result = extractor.extract_all_sections()
    
    # Save result
    extractor.save_extraction_result(extraction_result, output_file)
    
    # Print summary
    print(f"\n=== Comprehensive Extraction Summary ===")
    print(f"Total sections extracted: {extraction_result['metadata']['total_sections']}")
    print(f"Sections: {', '.join(extraction_result['metadata']['sections_extracted'])}")
    
    for section_name, section_data in extraction_result['sections'].items():
        print(f"\n{section_name}:")
        print(f"  Total objects: {section_data['total_count']}")
        if 'extraction_metadata' in section_data:
            for key, value in section_data['extraction_metadata'].items():
                print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
