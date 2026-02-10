"""
PRD Parser Module

This module handles parsing and extracting content from Product Requirements Documents.
Supports markdown and plain text formats.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional


class PRDParser:
    """Parser for Product Requirements Documents."""
    
    def __init__(self, file_path: str):
        """
        Initialize the PRD parser.
        
        Args:
            file_path: Path to the PRD file
        """
        self.file_path = Path(file_path)
        self.content = ""
        self.sections = {}
        
    def load(self) -> bool:
        """
        Load the PRD file content.
        
        Returns:
            True if file loaded successfully, False otherwise
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except FileNotFoundError:
            print(f"Error: File not found: {self.file_path}")
            return False
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def parse(self) -> Dict[str, str]:
        """
        Parse the PRD content into sections.
        
        Returns:
            Dictionary mapping section names to their content
        """
        if not self.content:
            return {}
        
        # Parse markdown-style headers (# Header, ## Header, etc.)
        sections = {}
        current_section = "Introduction"
        current_content = []
        
        lines = self.content.split('\n')
        
        for line in lines:
            # Check if line is a header
            header_match = re.match(r'^#{1,6}\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = header_match.group(1).strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        self.sections = sections
        return sections
    
    def get_section(self, section_name: str) -> Optional[str]:
        """
        Get content of a specific section.
        
        Args:
            section_name: Name of the section to retrieve
            
        Returns:
            Section content or None if not found
        """
        return self.sections.get(section_name)
    
    def get_all_sections(self) -> List[str]:
        """
        Get list of all section names in the PRD.
        
        Returns:
            List of section names
        """
        return list(self.sections.keys())
    
    def get_word_count(self, section_name: Optional[str] = None) -> int:
        """
        Get word count for a section or entire document.
        
        Args:
            section_name: Name of section, or None for entire document
            
        Returns:
            Word count
        """
        if section_name:
            content = self.sections.get(section_name, "")
        else:
            content = self.content
        
        # Simple word count (split on whitespace)
        words = content.split()
        return len(words)
