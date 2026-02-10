"""
PRD Analyzer Module

This module analyzes parsed PRD content and provides insights on completeness,
quality, and adherence to best practices.
"""

from typing import Dict, List, Tuple
from src.prd_parser import PRDParser


class PRDAnalyzer:
    """Analyzer for Product Requirements Documents."""
    
    def __init__(self, parser: PRDParser, config: Dict = None):
        """
        Initialize the PRD analyzer.
        
        Args:
            parser: PRDParser instance with loaded PRD
            config: Configuration dictionary with analysis parameters
        """
        self.parser = parser
        self.config = config or {}
        self.analysis_results = {}
        
    def analyze(self) -> Dict:
        """
        Perform comprehensive analysis of the PRD.
        
        Returns:
            Dictionary containing analysis results
        """
        completeness = self._analyze_completeness()
        quality = self._analyze_quality()
        statistics = self._gather_statistics()
        
        results = {
            "completeness": completeness,
            "quality": quality,
            "statistics": statistics,
            "recommendations": self._generate_recommendations(completeness, quality, statistics)
        }
        
        self.analysis_results = results
        return results
    
    def _analyze_completeness(self) -> Dict:
        """
        Analyze if PRD has required sections.
        
        Returns:
            Dictionary with completeness analysis
        """
        required_sections = self.config.get('analysis', {}).get('required_sections', [])
        optional_sections = self.config.get('analysis', {}).get('optional_sections', [])
        
        prd_sections = self.parser.get_all_sections()
        
        # Check required sections
        missing_required = []
        present_required = []
        
        for section in required_sections:
            # Case-insensitive matching
            found = any(section.lower() in s.lower() for s in prd_sections)
            if found:
                present_required.append(section)
            else:
                missing_required.append(section)
        
        # Check optional sections
        present_optional = []
        for section in optional_sections:
            found = any(section.lower() in s.lower() for s in prd_sections)
            if found:
                present_optional.append(section)
        
        completeness_score = 0
        if required_sections:
            completeness_score = (len(present_required) / len(required_sections)) * 100
        
        return {
            "score": round(completeness_score, 2),
            "required_sections_present": present_required,
            "required_sections_missing": missing_required,
            "optional_sections_present": present_optional,
            "total_sections": len(prd_sections)
        }
    
    def _analyze_quality(self) -> Dict:
        """
        Analyze quality metrics like word count, detail level.
        
        Returns:
            Dictionary with quality analysis
        """
        min_word_counts = self.config.get('analysis', {}).get('min_word_count', {})
        quality_issues = []
        quality_score = 100
        
        # Check word counts for key sections
        for section_key, min_count in min_word_counts.items():
            section_name = section_key.capitalize()
            
            # Find matching section (case-insensitive)
            matching_section = None
            for s in self.parser.get_all_sections():
                if section_name.lower() in s.lower():
                    matching_section = s
                    break
            
            if matching_section:
                word_count = self.parser.get_word_count(matching_section)
                if word_count < min_count:
                    quality_issues.append(
                        f"Section '{matching_section}' has {word_count} words (minimum: {min_count})"
                    )
                    quality_score -= 15
            else:
                quality_issues.append(f"Section '{section_name}' not found")
                quality_score -= 20
        
        quality_score = max(0, quality_score)
        
        return {
            "score": quality_score,
            "issues": quality_issues
        }
    
    def _gather_statistics(self) -> Dict:
        """
        Gather statistical information about the PRD.
        
        Returns:
            Dictionary with statistics
        """
        total_words = self.parser.get_word_count()
        sections = self.parser.get_all_sections()
        
        section_word_counts = {}
        for section in sections:
            section_word_counts[section] = self.parser.get_word_count(section)
        
        return {
            "total_word_count": total_words,
            "total_sections": len(sections),
            "section_names": sections,
            "section_word_counts": section_word_counts,
            "average_section_length": round(total_words / len(sections), 2) if sections else 0
        }
    
    def _generate_recommendations(self, completeness: Dict, quality: Dict, stats: Dict) -> List[str]:
        """
        Generate recommendations for improving the PRD.
        
        Args:
            completeness: Completeness analysis results
            quality: Quality analysis results
            stats: Statistics results
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Recommendations based on missing sections
        if completeness["required_sections_missing"]:
            recommendations.append(
                f"Add the following required sections: {', '.join(completeness['required_sections_missing'])}"
            )
        
        # Recommendations based on quality
        if quality["score"] < 70:
            recommendations.append(
                "Consider adding more detail to key sections to improve quality score"
            )
        
        # Recommendations based on statistics
        if stats["total_word_count"] < 500:
            recommendations.append(
                "PRD appears brief. Consider expanding with more details, examples, and context"
            )
        
        if stats["total_sections"] < 3:
            recommendations.append(
                "Consider organizing content into more sections for better readability"
            )
        
        if not recommendations:
            recommendations.append("PRD looks good! No major recommendations.")
        
        return recommendations
    
    def get_overall_score(self) -> float:
        """
        Calculate an overall score for the PRD.
        
        Returns:
            Overall score (0-100)
        """
        if not self.analysis_results:
            self.analyze()
        
        completeness_score = self.analysis_results["completeness"]["score"]
        quality_score = self.analysis_results["quality"]["score"]
        
        # Weighted average: 60% completeness, 40% quality
        overall = (completeness_score * 0.6) + (quality_score * 0.4)
        return round(overall, 2)
