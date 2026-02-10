# TI - Technical Intelligence: PRD Analysis Tool

A Python-based tool for analyzing Product Requirements Documents (PRDs). This tool helps evaluate the completeness, quality, and structure of your PRDs, providing actionable feedback and recommendations.

## Features

- 📄 **Parse PRD Documents**: Supports Markdown and plain text formats
- 🔍 **Completeness Analysis**: Check for required sections (Overview, Goals, Requirements, Success Metrics)
- 📊 **Quality Metrics**: Evaluate detail level, word counts, and section organization
- 💡 **Recommendations**: Get actionable suggestions to improve your PRD
- 🎯 **Scoring System**: Overall score based on completeness and quality
- 📈 **Statistics**: Word counts, section counts, and detailed breakdowns
- 🔧 **Configurable**: Customize analysis rules via YAML configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/firsthandassoc/ti.git
cd ti
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze a PRD file:
```bash
python main.py examples/sample_prd.md
```

### Advanced Usage

With verbose output:
```bash
python main.py examples/sample_prd.md --verbose
```

With custom configuration:
```bash
python main.py my_prd.md --config custom_config.yaml
```

Output as JSON:
```bash
python main.py examples/sample_prd.md --output json
```

Save results to file:
```bash
python main.py examples/sample_prd.md --output json --output-file results.json
```

### Command Line Options

```
usage: main.py [-h] [--config CONFIG] [--output {text,json,yaml}]
               [--output-file OUTPUT_FILE] [--verbose]
               prd_file

positional arguments:
  prd_file              Path to the PRD file to analyze

optional arguments:
  -h, --help            Show this help message and exit
  --config CONFIG       Path to configuration file (default: config.yaml)
  --output {text,json,yaml}
                        Output format (default: text)
  --output-file OUTPUT_FILE
                        Save results to file instead of stdout
  --verbose             Show detailed analysis results
```

## Configuration

The tool uses a `config.yaml` file to define analysis parameters:

```yaml
analysis:
  # Required sections that should be in every PRD
  required_sections:
    - "Overview"
    - "Goals"
    - "Requirements"
    - "Success Metrics"
  
  # Optional sections that enhance PRD quality
  optional_sections:
    - "User Stories"
    - "Technical Specifications"
    - "Timeline"
    - "Risks"
    - "Dependencies"
  
  # Minimum word count thresholds for key sections
  min_word_count:
    overview: 50
    goals: 30
    requirements: 100

output:
  format: "json"  # Options: json, yaml, text
  verbose: true
```

## Project Structure

```
ti/
├── main.py                 # Main entry point and CLI
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── src/
│   ├── __init__.py
│   ├── prd_parser.py     # PRD parsing logic
│   └── prd_analyzer.py   # PRD analysis logic
└── examples/
    ├── sample_prd.md     # Comprehensive example PRD
    └── minimal_prd.md    # Minimal example PRD
```

## Analysis Scoring

The tool provides three main scores:

1. **Completeness Score (0-100)**: Based on presence of required sections
2. **Quality Score (0-100)**: Based on word counts and detail level
3. **Overall Score (0-100)**: Weighted average (60% completeness, 40% quality)

### Score Interpretation

- **90-100**: Excellent - PRD is comprehensive and detailed
- **70-89**: Good - PRD covers essentials but could use more detail
- **50-69**: Fair - PRD needs significant improvements
- **0-49**: Poor - PRD is missing critical sections or lacks detail

## Examples

### Example 1: Complete PRD

```bash
$ python main.py examples/sample_prd.md --verbose
```

Output:
```
Loading PRD from: examples/sample_prd.md
Parsing PRD content...
Analyzing PRD...

============================================================
PRD ANALYSIS RESULTS
============================================================

📊 Overall Score: 92.0/100

✓ Completeness Score: 100.0/100
  ✓ Required sections present: Overview, Goals, Requirements, Success Metrics
  + Optional sections present: User Stories, Technical Specifications, Timeline, Risks, Dependencies

✓ Quality Score: 80.0/100

📈 Statistics:
  - Total words: 782
  - Total sections: 10
  - Average section length: 78.2 words

💡 Recommendations:
  1. PRD looks good! No major recommendations.

============================================================
```

### Example 2: Minimal PRD

```bash
$ python main.py examples/minimal_prd.md
```

This will show lower scores and specific recommendations for improvement.

## Development

### Running Tests

The tool includes example PRDs for testing:

```bash
# Test with comprehensive PRD
python main.py examples/sample_prd.md

# Test with minimal PRD
python main.py examples/minimal_prd.md
```

### Adding New Analysis Rules

1. Update `config.yaml` with new section requirements or thresholds
2. Modify `src/prd_analyzer.py` to implement new analysis logic
3. Test with example PRDs

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

First Hand Association