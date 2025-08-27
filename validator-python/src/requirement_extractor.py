#!/usr/bin/env python3
"""
CardDemo Requirement Extractor for G-Eval Framework

This module extracts individual requirements from the CardDemo requirements JSON file
and creates focused test files for G-Eval validation.

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

class RequirementExtractor:
    """
    Extracts individual requirements from the CardDemo requirements JSON file
    for focused G-Eval validation testing.
    """
    
    def __init__(self, requirements_file: str):
        """
        Initialize the requirement extractor.
        
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
        """Extract user stories from the JSON structure."""
        stories = []
        if 'data' in self.requirements_data and 'user_stories' in self.requirements_data['data']:
            stories = self.requirements_data['data']['user_stories']
        return stories
    
    def _extract_technical_requirements_from_story(self, story: Dict[str, Any]) -> List[str]:
        """Extract technical requirements from a user story."""
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
    
    def create_single_requirement_json(self, requirement_index: int = 0) -> Dict[str, Any]:
        """
        Extract one requirement from the original JSON and create a focused test file.
        
        Args:
            requirement_index: Index of the requirement to extract (0-based)
            
        Returns:
            Dictionary containing the single requirement with its metadata
        """
        # Load requirements
        self.load_requirements()
        
        # Extract user stories
        user_stories = self._extract_user_stories()
        
        if not user_stories:
            logger.error("No user stories found in the requirements file")
            return {}
        
        if requirement_index >= len(user_stories):
            logger.error(f"Requirement index {requirement_index} out of range. Total stories: {len(user_stories)}")
            return {}
        
        # Get the specific requirement
        selected_story = user_stories[requirement_index]
        logger.info(f"Extracting requirement {requirement_index}: {selected_story.get('title', 'No title')}")
        
        # Extract technical requirements
        technical_requirements = self._extract_technical_requirements_from_story(selected_story)
        
        # Create focused requirement structure
        single_requirement = {
            "metadata": {
                "extraction_date": str(Path.cwd()),
                "requirement_index": requirement_index,
                "total_requirements": len(user_stories),
                "source_file": self.requirements_file
            },
            "requirement": {
                "user_story": selected_story,
                "technical_requirements": technical_requirements
            }
        }
        
        return single_requirement
    
    def save_single_requirement(self, requirement_data: Dict[str, Any], output_file: str = None) -> str:
        """
        Save a single requirement to a JSON file.
        
        Args:
            requirement_data: The requirement data to save
            output_file: Output file path (optional, will generate if not provided)
            
        Returns:
            Path to the saved file
        """
        if output_file is None:
            req_index = requirement_data.get('metadata', {}).get('requirement_index', 0)
            output_file = f"single_requirement_test_{req_index}.json"
        
        # Ensure output directory exists
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w') as f:
                json.dump(requirement_data, f, indent=2)
            logger.info(f"Saved single requirement to {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error saving requirement file: {e}")
            raise
    
    def list_available_requirements(self) -> List[Dict[str, Any]]:
        """
        List all available requirements with their titles and indices.
        
        Returns:
            List of requirement summaries
        """
        self.load_requirements()
        user_stories = self._extract_user_stories()
        
        requirements_list = []
        for i, story in enumerate(user_stories):
            requirements_list.append({
                "index": i,
                "title": story.get('title', 'No title'),
                "feature_name": story.get('feature_name', 'No feature name'),
                "priority": story.get('priority', 'Not specified'),
                "story_points": story.get('story_points', 'Not specified')
            })
        
        return requirements_list

def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python requirement_extractor.py <requirements_file> [requirement_index] [output_file]")
        sys.exit(1)
    
    requirements_file = sys.argv[1]
    requirement_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        extractor = RequirementExtractor(requirements_file)
        
        # List available requirements
        print("Available requirements:")
        requirements_list = extractor.list_available_requirements()
        for req in requirements_list:
            print(f"  {req['index']}: {req['title']} (Feature: {req['feature_name']}, Priority: {req['priority']})")
        
        # Extract specific requirement
        print(f"\nExtracting requirement {requirement_index}...")
        requirement_data = extractor.create_single_requirement_json(requirement_index)
        
        if requirement_data:
            output_path = extractor.save_single_requirement(requirement_data, output_file)
            print(f"Successfully extracted requirement to: {output_path}")
        else:
            print("Failed to extract requirement")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
