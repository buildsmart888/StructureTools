# Load Combination System Documentation

## Overview

The Load Combination System is a comprehensive tool for creating, managing, and analyzing load combinations in structural engineering projects. It supports multiple international design standards and allows for custom load combination formulas.

## Features

### 1. Standard Load Combinations
- **ACI 318** (American Concrete Institute)
- **AISC 360** (American Institute of Steel Construction)
- **Eurocode** (European Design Standards)
- **IBC 2018** (International Building Code)

### 2. Custom Load Combinations
- User-defined combination formulas
- Flexible formula syntax
- Validation and error checking
- Integration with standard combinations

### 3. Analysis Integration
- Direct integration with calc.py analysis engine
- Automatic load factor application
- Results extraction and storage
- Critical combination identification

### 4. Export/Import Functionality
- JSON-based data exchange
- Comprehensive analysis reports
- Combination set sharing between projects

## Installation and Setup

1. **Prerequisites**
   - FreeCAD 0.19 or later
   - StructureTools workbench installed
   - Python 3.7+ with required dependencies

2. **Files Required**
   - `load_combination.py` - Main load combination module
   - `custom_combinations.py` - Custom combination manager
   - `combination_analysis.py` - Analysis integration helper
   - `load_combination_examples.py` - Usage examples

3. **Integration with FreeCAD**
   ```python
   # The system is automatically integrated when StructureTools workbench is loaded
   # Access via toolbar button or menu: StructureTools > Load Combinations
   ```

## Usage Guide

### Creating Load Combinations

#### Method 1: Using the GUI Dialog
1. Open FreeCAD with StructureTools workbench
2. Click the "Load Combination" button in the toolbar
3. Select combination type (Standard or Custom)
4. Configure parameters and formulas
5. Click "Add Combination" to create

#### Method 2: Programmatic Creation
```python
from freecad.StructureTools.load_combination import makeLoadCombination

# Create a standard ACI combination
combo = makeLoadCombination()
combo.CombinationName = "ACI Ultimate 1"
combo.CombinationType = "ACI 318"
combo.CombinationFormula = "1.2DL + 1.6LL"
combo.IncludeInAnalysis = True

# Create a custom combination
custom_combo = makeLoadCombination()
custom_combo.CombinationName = "Special Load Case"
custom_combo.CombinationType = "Custom"
custom_combo.IsCustomFormula = True
custom_combo.CustomFormula = "1.0DL + 0.5LL + 1.2WL"
```

### Standard Load Combination Types

#### ACI 318 Combinations
- **Service**: `1.0DL + 1.0LL`
- **Ultimate 1**: `1.2DL + 1.6LL`
- **Ultimate 2**: `1.2DL + 1.0LL + 1.0WL`
- **Ultimate 3**: `1.2DL + 1.0LL + 1.0EQ`
- **Ultimate 4**: `0.9DL + 1.0WL`
- **Ultimate 5**: `0.9DL + 1.0EQ`

#### AISC 360 Combinations
- **LRFD 1**: `1.4DL`
- **LRFD 2**: `1.2DL + 1.6LL + 0.5(LL or SL or RL)`
- **LRFD 3**: `1.2DL + 1.6(LL or SL or RL) + (1.0LL or 0.5WL)`
- **LRFD 4**: `1.2DL + 1.0WL + 1.0LL + 0.5(LL or SL or RL)`
- **LRFD 5**: `1.2DL + 1.0EQ + 1.0LL + 0.2SL`
- **LRFD 6**: `0.9DL + 1.0WL`
- **LRFD 7**: `0.9DL + 1.0EQ`

#### Eurocode Combinations
- **ULS 1**: `1.35DL + 1.5LL`
- **ULS 2**: `1.35DL + 1.5LL + 0.9WL`
- **ULS 3**: `1.0DL + 1.5LL + 1.5WL`
- **ULS 4**: `1.0DL + 0.7LL + 1.5WL`
- **SLS**: `1.0DL + 1.0LL`

#### IBC 2018 Combinations
- **Basic 1**: `1.4DL + 1.6LL`
- **Basic 2**: `1.2DL + 1.6LL + 0.5SL`
- **Basic 3**: `1.2DL + 1.6SL + (1.0LL or 0.5WL)`
- **Basic 4**: `1.2DL + 1.0WL + 1.0LL + 0.5SL`
- **Basic 5**: `1.2DL + 1.0EQ + 1.0LL + 0.2SL`
- **Basic 6**: `0.9DL + 1.0WL`
- **Basic 7**: `0.9DL + 1.0EQ`

### Load Type Abbreviations

| Abbreviation | Load Type | Description |
|--------------|-----------|-------------|
| DL | Dead Load | Permanent structural loads |
| LL | Live Load | Occupancy and movable loads |
| WL | Wind Load | Wind pressure and suction |
| EQ | Earthquake Load | Seismic forces |
| SL | Snow Load | Snow accumulation loads |
| RL | Rain Load | Ponding and drainage loads |
| CL | Construction Load | Temporary construction loads |

### Custom Formula Syntax

#### Basic Format
```
factor1*LoadType1 + factor2*LoadType2 + ...
```

#### Examples
```python
# Simple combination
"1.2DL + 1.6LL"

# Complex combination with multiple load types
"1.2DL + 1.0LL + 0.5SL + 1.4WL"

# Alternative notation (multiplication sign optional)
"1.2*DL + 1.6*LL"

# Seismic combination
"1.0DL + 0.3LL + 1.0EQ"
```

#### Validation Rules
- Load factors must be positive numbers
- Load type abbreviations must be recognized
- Formula must be syntactically correct
- Each load type should appear only once per combination

### Analysis Integration

#### Running Analysis
```python
from freecad.StructureTools.combination_analysis import combination_analysis_manager

# Run analysis for a specific combination
success, message = combination_analysis_manager.run_combination_analysis(combo, calc_obj)

if success:
    print(f"Analysis completed: {message}")
    print(f"Max Moment: {combo.MaxMoment} kN⋅m")
    print(f"Max Shear: {combo.MaxShear} kN")
    print(f"Critical Member: {combo.CriticalMember}")
else:
    print(f"Analysis failed: {message}")
```

#### Finding Critical Combinations
```python
# Find critical combination for different criteria
critical_moment, msg = combination_analysis_manager.find_critical_combination(combinations, 'moment')
critical_shear, msg = combination_analysis_manager.find_critical_combination(combinations, 'shear')
critical_deflection, msg = combination_analysis_manager.find_critical_combination(combinations, 'deflection')
```

### Export/Import Operations

#### Exporting Combinations
```python
# Export to JSON file
export_path = "my_combinations.json"
success, message = combination_analysis_manager.export_analysis_report(combinations, export_path)
```

#### Importing Combinations
```python
# Import from JSON file (via GUI dialog)
# File > Import Load Combinations
# Select JSON file with combination data
```

#### Export Data Format
```json
{
  "project": "StructureTools Analysis",
  "date": "2024-01-15T10:30:00",
  "analysis_summary": {
    "total_combinations": 5,
    "analyzed_combinations": 3
  },
  "combinations": [
    {
      "name": "ACI Ultimate 1",
      "type": "ACI 318",
      "formula": "1.2DL + 1.6LL",
      "results": {
        "max_moment": 1250.5,
        "max_shear": 675.2,
        "max_deflection": 0.025,
        "critical_member": "B1"
      }
    }
  ]
}
```

## API Reference

### LoadCombination Class

#### Properties
- `CombinationName` (String): Name of the combination
- `CombinationType` (String): Type/standard of combination
- `Description` (String): Detailed description
- `CombinationFormula` (String): Standard formula
- `IsCustomFormula` (Boolean): Whether using custom formula
- `CustomFormula` (String): Custom formula text
- `IncludeInAnalysis` (Boolean): Include in batch analysis
- `MaxMoment` (Float): Maximum moment result
- `MaxShear` (Float): Maximum shear result
- `MaxAxial` (Float): Maximum axial force result
- `MaxDeflection` (Float): Maximum deflection result
- `CriticalMember` (String): Member with maximum response
- `IsCritical` (Boolean): Whether this is the critical combination

#### Methods
- `execute(obj)`: Execute the load combination
- `onChanged(obj, prop)`: Handle property changes
- `run_analysis(obj)`: Run structural analysis
- `get_standard_combinations()`: Get predefined combinations

### CombinationAnalysisManager Class

#### Methods
- `run_combination_analysis(combination_obj, calc_obj)`: Run analysis
- `apply_combination_factors(combination_obj, calc_obj)`: Apply load factors
- `extract_results(calc_obj)`: Extract analysis results
- `find_critical_combination(combinations, criteria)`: Find critical case
- `export_analysis_report(combinations, filepath)`: Export report

### CustomCombinationManager Class

#### Methods
- `add_combination(name, formula, description)`: Add custom combination
- `validate_formula(formula)`: Validate formula syntax
- `get_combinations()`: Get all custom combinations
- `export_combinations(filepath)`: Export to file
- `import_combinations(filepath)`: Import from file

## Troubleshooting

### Common Issues

1. **"No calc object found" Error**
   - Solution: Create a calculation object first using the calc module
   - Ensure calc.py is properly integrated in your project

2. **Invalid Formula Error**
   - Check load type abbreviations (DL, LL, WL, EQ, SL)
   - Ensure proper syntax: "1.2DL + 1.6LL"
   - Verify load factors are positive numbers

3. **Analysis Integration Issues**
   - Verify calc.py integration is working
   - Check that loads are properly named/categorized
   - Ensure structural model is complete

4. **Export/Import Problems**
   - Check file permissions
   - Verify JSON format validity
   - Ensure all required properties are present

### Performance Considerations

- **Large Models**: For models with many combinations, use selective analysis
- **Memory Usage**: Clear analysis results periodically for large batch runs
- **File Size**: Large export files may need compression for sharing

## Examples and Tutorials

### Example 1: Basic Office Building
```python
# Service load combination for office building
service = makeLoadCombination()
service.CombinationName = "Office Service"
service.CombinationFormula = "1.0DL + 1.0LL"

# Ultimate load combination
ultimate = makeLoadCombination()
ultimate.CombinationName = "Office Ultimate"
ultimate.CombinationFormula = "1.2DL + 1.6LL"
```

### Example 2: Wind-Critical Structure
```python
# Wind load combinations
wind_combo1 = makeLoadCombination()
wind_combo1.CombinationName = "Wind Case 1"
wind_combo1.CombinationFormula = "1.2DL + 1.0LL + 1.0WL"

wind_combo2 = makeLoadCombination()
wind_combo2.CombinationName = "Wind Case 2"
wind_combo2.CombinationFormula = "0.9DL + 1.0WL"
```

### Example 3: Seismic Design
```python
# Seismic load combination
seismic = makeLoadCombination()
seismic.CombinationName = "Seismic"
seismic.CombinationType = "Custom"
seismic.IsCustomFormula = True
seismic.CustomFormula = "1.0DL + 0.3LL + 1.0EQ"
```

## Best Practices

1. **Naming Convention**
   - Use descriptive names: "ACI Ultimate 1", "Wind Case X+", etc.
   - Include design standard in name for clarity

2. **Load Organization**
   - Use consistent load type abbreviations
   - Group similar load cases together
   - Document special or unusual load cases

3. **Analysis Workflow**
   - Start with standard combinations for your design code
   - Add custom combinations for special conditions
   - Run analysis in logical sequence
   - Review and validate critical combinations

4. **Documentation**
   - Export combination sets for project records
   - Include analysis reports in design documentation
   - Document any custom formulas and their rationale

## Future Enhancements

- Integration with more international codes
- Graphical load combination editor
- Automated combination generation based on load cases
- Integration with design check modules
- Advanced result visualization
- Load combination optimization tools

## Support

For issues, questions, or contributions:
- Review the StructureTools documentation
- Check the GitHub repository for updates
- Report bugs through the issue tracking system
- Contribute improvements via pull requests
