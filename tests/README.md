# Load Combination System Test Suite

This directory contains comprehensive tests for the Load Combination System in StructureTools.

## Test Structure

### Core Test Files

1. **`test_load_combination.py`** - Main unit tests
   - `TestLoadCombination` - Core load combination functionality
   - `TestCustomCombinationManager` - Custom combination management
   - `TestCombinationAnalysisManager` - Analysis integration
   - `TestLoadCombinationIntegration` - Integration tests

2. **`test_load_combination_performance.py`** - Performance tests
   - `TestLoadCombinationPerformance` - Performance benchmarks
   - `TestLoadCombinationStress` - Stress testing and edge cases

3. **`test_utils.py`** - Test utilities and helpers
   - `TestConfig` - Configuration and test data
   - `MockFreeCADEnvironment` - FreeCAD mocking utilities
   - `TestDataGenerator` - Test data generation
   - `TestValidator` - Validation utilities
   - `TestReporter` - Test reporting tools

4. **`run_tests.py`** - Comprehensive test runner
   - Command-line test execution
   - Detailed reporting
   - Performance monitoring

## Running Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Specific Test Categories
```bash
# Unit tests only
python tests/run_tests.py --unit

# Performance tests only
python tests/run_tests.py --performance

# Stress tests only
python tests/run_tests.py --stress
```

### Run Individual Test Files
```bash
# Unit tests
python -m unittest tests.test_load_combination

# Performance tests
python -m unittest tests.test_load_combination_performance

# Test utilities
python tests/test_utils.py
```

## Test Coverage

### Unit Tests (test_load_combination.py)

#### TestLoadCombination
- ✅ Initialization and basic functionality
- ✅ Standard combination generation (ACI 318, AISC 360, Eurocode, IBC 2018)
- ✅ Execute method functionality
- ✅ Analysis integration with error handling
- ✅ Property management and validation

#### TestCustomCombinationManager
- ✅ Formula validation (valid and invalid cases)
- ✅ Custom combination addition and management
- ✅ Export/import functionality
- ✅ Data persistence and retrieval

#### TestCombinationAnalysisManager
- ✅ Formula parsing and factor extraction
- ✅ Analysis result storage and retrieval
- ✅ Critical combination identification
- ✅ Analysis report generation

#### TestLoadCombinationIntegration
- ✅ End-to-end workflow testing
- ✅ Component integration verification
- ✅ Data consistency across operations

### Performance Tests (test_load_combination_performance.py)

#### TestLoadCombinationPerformance
- ✅ Large dataset handling (1000+ combinations)
- ✅ Formula validation performance (1000 validations < 1s)
- ✅ Formula parsing performance (10000 parsings < 2s)
- ✅ Memory usage testing (5000 combinations < 100MB)
- ✅ Concurrent access testing (10 threads)
- ✅ Export/import performance (1000 combinations < 5s each)

#### TestLoadCombinationStress
- ✅ Maximum formula complexity testing
- ✅ Boundary condition testing
- ✅ Error recovery and system stability
- ✅ Edge case handling

## Test Data and Fixtures

### Standard Test Combinations
```python
# ACI 318 combinations
"1.0DL + 1.0LL"          # Service
"1.2DL + 1.6LL"          # Ultimate basic
"1.2DL + 1.0LL + 1.0WL"  # Ultimate with wind
"0.9DL + 1.0EQ"          # Seismic

# AISC 360 combinations
"1.4DL"                  # LRFD basic
"1.2DL + 1.6LL"          # LRFD with live load
"0.9DL + 1.0WL"          # Wind critical

# Eurocode combinations
"1.35DL + 1.5LL"         # ULS fundamental
"1.0DL + 1.0LL"          # SLS characteristic

# IBC 2018 combinations
"1.4DL + 1.6LL"          # Basic strength
"1.2DL + 1.0EQ + 1.0LL"  # Seismic
```

### Test Formula Patterns
```python
# Valid formulas
"1.2DL + 1.6LL"                    # Basic
"1.2*DL + 1.6*LL"                  # With multiplication
"1.0DL + 0.5LL + 1.0WL + 0.2EQ"    # Complex

# Invalid formulas (for validation testing)
""                      # Empty
"1.2XL + 1.6LL"        # Invalid load type
"DL + LL"              # Missing factors
"-1.2DL + 1.6LL"       # Negative factors
```

## Performance Benchmarks

### Target Performance Metrics
- **Combination Creation**: 1000 combinations < 10 seconds
- **Formula Validation**: 1000 validations < 1 second
- **Formula Parsing**: 10000 parsings < 2 seconds
- **Memory Usage**: 5000 combinations < 100 MB
- **Export Operation**: 1000 combinations < 5 seconds
- **Import Operation**: 1000 combinations < 5 seconds

### Typical Results
```
Created 1000 combinations in 2.145 seconds
Average time per combination: 2.145 ms

Validated 1000 formulas in 0.234 seconds
Average validation time: 0.234 ms

Parsed complex formula 10000 times in 0.892 seconds
Average parsing time: 0.089 ms

Memory usage:
Initial: 45.23 MB
Final: 67.45 MB
Increase: 22.22 MB
Memory per combination: 4.66 KB
```

## Mock Environment

### FreeCAD Mocking
The test suite uses comprehensive mocking to simulate the FreeCAD environment:

```python
# Mock FreeCAD module
mock_freecad = Mock()
mock_freecad.Vector = Mock(side_effect=lambda x, y, z: (x, y, z))
mock_freecad.ActiveDocument = Mock()
sys.modules['FreeCAD'] = mock_freecad

# Mock structural objects
mock_combination.CombinationName = "Test Combination"
mock_combination.CombinationType = "ACI 318"
mock_combination.CombinationFormula = "1.2DL + 1.6LL"
```

## Error Handling Tests

### Test Coverage for Error Conditions
- ✅ Invalid formula syntax
- ✅ Missing required parameters
- ✅ File I/O errors during export/import
- ✅ Memory constraints with large datasets
- ✅ Concurrent access race conditions
- ✅ Analysis integration failures
- ✅ System recovery after errors

## Dependencies

### Required Packages
- `unittest` (built-in)
- `json` (built-in)
- `tempfile` (built-in)
- `threading` (built-in)
- `sys`, `os` (built-in)

### Optional Packages
- `psutil` - For memory usage testing (install with `pip install psutil`)

## Test Reports

### Report Generation
Tests automatically generate detailed reports in JSON format:

```bash
test_reports/
├── load_combination_test_report_20240131_143022.json
├── load_combination_test_report_20240131_151545.json
└── ...
```

### Report Contents
- Test execution summary
- Performance metrics
- Failure analysis
- Environment information
- Detailed test results

## Continuous Integration

### Running Tests in CI
```yaml
# Example GitHub Actions workflow
- name: Run Load Combination Tests
  run: |
    cd StructureTools
    python tests/run_tests.py --unit
    python tests/run_tests.py --performance
```

### Test Exit Codes
- `0` - All tests passed
- `1` - Some tests failed or errors occurred

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   Error importing test modules: No module named 'freecad'
   ```
   **Solution**: Tests use mocking, ensure test files are in correct directory structure.

2. **Performance Test Failures**
   ```
   AssertionError: Creating 1000 combinations took too long
   ```
   **Solution**: Performance tests may fail on slower systems. Adjust thresholds in `TestConfig`.

3. **Memory Test Skipped**
   ```
   WARNING: psutil not available, memory tests will be skipped
   ```
   **Solution**: Install psutil: `pip install psutil`

### Debug Mode
```bash
python tests/run_tests.py --verbose
```

## Contributing

### Adding New Tests
1. Add test methods to appropriate test class
2. Follow naming convention: `test_feature_description`
3. Include both positive and negative test cases
4. Add performance considerations for new features
5. Update this README with new test coverage

### Test Guidelines
- Use descriptive test names
- Include docstrings explaining test purpose
- Mock external dependencies
- Test edge cases and error conditions
- Maintain performance benchmarks
- Keep tests independent and isolated

## License

Tests are part of the StructureTools project and follow the same license terms.
