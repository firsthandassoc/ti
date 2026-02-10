"""
Main entry point for the PRD Analysis Tool

This script provides a command-line interface for analyzing Product Requirements Documents.
"""

import argparse
import json
import sys
import yaml
from pathlib import Path

from src.prd_parser import PRDParser
from src.prd_analyzer import PRDAnalyzer


def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Config file not found at {config_path}, using defaults")
        return {}
    except Exception as e:
        print(f"Warning: Error loading config: {e}, using defaults")
        return {}


def print_analysis_results(results: dict, overall_score: float, verbose: bool = True):
    """
    Print analysis results in a formatted way.
    
    Args:
        results: Analysis results dictionary
        overall_score: Overall PRD score
        verbose: Whether to print detailed results
    """
    print("\n" + "="*60)
    print("PRD ANALYSIS RESULTS")
    print("="*60)
    
    print(f"\n📊 Overall Score: {overall_score}/100")
    
    # Completeness
    print(f"\n✓ Completeness Score: {results['completeness']['score']}/100")
    if verbose:
        if results['completeness']['required_sections_present']:
            print(f"  ✓ Required sections present: {', '.join(results['completeness']['required_sections_present'])}")
        if results['completeness']['required_sections_missing']:
            print(f"  ✗ Required sections missing: {', '.join(results['completeness']['required_sections_missing'])}")
        if results['completeness']['optional_sections_present']:
            print(f"  + Optional sections present: {', '.join(results['completeness']['optional_sections_present'])}")
    
    # Quality
    print(f"\n✓ Quality Score: {results['quality']['score']}/100")
    if verbose and results['quality']['issues']:
        print("  Issues:")
        for issue in results['quality']['issues']:
            print(f"    - {issue}")
    
    # Statistics
    print(f"\n📈 Statistics:")
    print(f"  - Total words: {results['statistics']['total_word_count']}")
    print(f"  - Total sections: {results['statistics']['total_sections']}")
    print(f"  - Average section length: {results['statistics']['average_section_length']} words")
    
    if verbose:
        print(f"\n  Sections found:")
        for section in results['statistics']['section_names']:
            word_count = results['statistics']['section_word_counts'][section]
            print(f"    - {section}: {word_count} words")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "="*60 + "\n")


def main():
    """Main function for the PRD analyzer CLI."""
    parser = argparse.ArgumentParser(
        description="Analyze Product Requirements Documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py examples/sample_prd.md
  python main.py my_prd.md --config custom_config.yaml
  python main.py my_prd.md --output json --output-file results.json
        """
    )
    
    parser.add_argument(
        'prd_file',
        help='Path to the PRD file to analyze'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--output',
        choices=['text', 'json', 'yaml'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output-file',
        help='Save results to file instead of stdout'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed analysis results'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Check if PRD file exists
    prd_path = Path(args.prd_file)
    if not prd_path.exists():
        print(f"Error: PRD file not found: {args.prd_file}")
        sys.exit(1)
    
    # Parse PRD
    print(f"Loading PRD from: {args.prd_file}")
    prd_parser = PRDParser(args.prd_file)
    
    if not prd_parser.load():
        print("Error: Failed to load PRD file")
        sys.exit(1)
    
    print("Parsing PRD content...")
    prd_parser.parse()
    
    # Analyze PRD
    print("Analyzing PRD...")
    analyzer = PRDAnalyzer(prd_parser, config)
    results = analyzer.analyze()
    overall_score = analyzer.get_overall_score()
    
    # Output results
    if args.output == 'text':
        print_analysis_results(results, overall_score, verbose=args.verbose)
    elif args.output == 'json':
        output_data = {
            "overall_score": overall_score,
            "analysis": results
        }
        json_output = json.dumps(output_data, indent=2)
        
        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(json_output)
            print(f"Results saved to: {args.output_file}")
        else:
            print(json_output)
    elif args.output == 'yaml':
        output_data = {
            "overall_score": overall_score,
            "analysis": results
        }
        yaml_output = yaml.dump(output_data, default_flow_style=False)
        
        if args.output_file:
            with open(args.output_file, 'w') as f:
                f.write(yaml_output)
            print(f"Results saved to: {args.output_file}")
        else:
            print(yaml_output)
    
    # Exit with appropriate code
    if overall_score >= 70:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
