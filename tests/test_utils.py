# Test Configuration and Utilities for Load Combination System
# Supporting utilities and configuration for test suite

import os
import sys
import json
import tempfile
from unittest.mock import Mock, MagicMock

class TestConfig:
    """Configuration for Load Combination tests"""
    
    # Performance test thresholds
    MAX_COMBINATION_CREATION_TIME = 10.0  # seconds for 1000 combinations
    MAX_FORMULA_VALIDATION_TIME = 1.0     # seconds for 1000 validations
    MAX_FORMULA_PARSING_TIME = 2.0        # seconds for 10000 parsings
    MAX_MEMORY_USAGE = 100                 # MB for 5000 combinations
    MAX_EXPORT_TIME = 5.0                  # seconds for 1000 combinations
    MAX_IMPORT_TIME = 5.0                  # seconds for 1000 combinations
    MAX_FILE_SIZE = 1024                   # KB for 1000 combinations
    
    # Test data
    VALID_FORMULAS = [
        "1.2DL + 1.6LL",
        "1.0DL + 0.5LL + 1.0WL",
        "0.9DL + 1.0EQ",
        "1.2*DL + 1.6*LL",
        "1.35DL + 1.5LL + 0.9WL",
        "1.2DL + 1.0LL + 1.0WL + 0.5SL",
        "1.2DL + 1.0EQ + 1.0LL + 0.2SL"
    ]
    
    INVALID_FORMULAS = [
        "",                    # Empty formula
        "1.2XL + 1.6LL",      # Invalid load type
        "DL + LL",            # Missing factors
        "-1.2DL + 1.6LL",     # Negative factor
        "1.2DL +",            # Incomplete formula
        "1.2DL 1.6LL",        # Missing operator
        "1.2DL + + 1.6LL",    # Double operator
        "abc + def",          # Non-numeric
    ]
    
    LOAD_TYPES = ["DL", "LL", "WL", "EQ", "SL", "RL", "CL"]
    
    STANDARD_COMBINATIONS = {
        "ACI 318": [
            "1.0DL + 1.0LL",
            "1.2DL + 1.6LL",
            "1.2DL + 1.0LL + 1.0WL",
            "1.2DL + 1.0LL + 1.0EQ",
            "0.9DL + 1.0WL",
            "0.9DL + 1.0EQ"
        ],
        "AISC 360": [
            "1.4DL",
            "1.2DL + 1.6LL",
            "1.2DL + 1.6LL + 0.5SL",
            "1.2DL + 1.0WL + 1.0LL",
            "1.2DL + 1.0EQ + 1.0LL",
            "0.9DL + 1.0WL",
            "0.9DL + 1.0EQ"
        ],
        "Eurocode": [
            "1.35DL + 1.5LL",
            "1.35DL + 1.5LL + 0.9WL",
            "1.0DL + 1.5LL + 1.5WL",
            "1.0DL + 0.7LL + 1.5WL",
            "1.0DL + 1.0LL"
        ],
        "IBC 2018": [
            "1.4DL + 1.6LL",
            "1.2DL + 1.6LL + 0.5SL",
            "1.2DL + 1.6SL + 1.0LL",
            "1.2DL + 1.0WL + 1.0LL + 0.5SL",
            "1.2DL + 1.0EQ + 1.0LL + 0.2SL",
            "0.9DL + 1.0WL",
            "0.9DL + 1.0EQ"
        ]
    }


class MockFreeCADEnvironment:
    """Mock FreeCAD environment for testing"""
    
    def __init__(self):
        self.setup_freecad_mocks()
        self.setup_document_mocks()
        self.setup_object_mocks()
    
    def setup_freecad_mocks(self):
        """Setup basic FreeCAD module mocks"""
        self.freecad = Mock()
        self.freecad.Vector = Mock(side_effect=lambda x, y, z: (x, y, z))
        self.freecad.getUserAppDataDir = Mock(return_value=tempfile.gettempdir())
        self.freecad.newDocument = Mock()
        
        # Add to sys.modules
        sys.modules['FreeCAD'] = self.freecad
    
    def setup_document_mocks(self):
        """Setup document-related mocks"""
        self.document = Mock()
        self.document.Name = "TestDocument"
        self.document.Objects = []
        self.freecad.ActiveDocument = self.document
        self.freecad.newDocument.return_value = self.document
    
    def setup_object_mocks(self):
        """Setup object-related mocks"""
        # Mock load combination object
        self.load_combination = Mock()
        self.load_combination.CombinationName = "Test Combination"
        self.load_combination.CombinationType = "ACI 318"
        self.load_combination.Description = "Test description"
        self.load_combination.CombinationFormula = "1.2DL + 1.6LL"
        self.load_combination.IsCustomFormula = False
        self.load_combination.CustomFormula = ""
        self.load_combination.IncludeInAnalysis = True
        self.load_combination.MaxMoment = 0.0
        self.load_combination.MaxShear = 0.0
        self.load_combination.MaxAxial = 0.0
        self.load_combination.MaxDeflection = 0.0
        self.load_combination.CriticalMember = ""
        self.load_combination.IsCritical = False
        
        # Mock calc object
        self.calc_object = Mock()
        self.calc_object.Proxy = Mock()
        self.calc_object.Proxy.execute = Mock()
        
        # Mock other structural objects
        self.material = Mock()
        self.section = Mock()
        self.member = Mock()
        self.support = Mock()
        self.load = Mock()
    
    def add_object_to_document(self, obj):
        """Add object to mock document"""
        self.document.Objects.append(obj)
    
    def get_freecad_mock(self):
        """Get the FreeCAD mock"""
        return self.freecad
    
    def cleanup(self):
        """Clean up mocks"""
        if 'FreeCAD' in sys.modules:
            del sys.modules['FreeCAD']


class TestDataGenerator:
    """Generate test data for Load Combination tests"""
    
    @staticmethod
    def generate_combinations(count, prefix="TestCombo"):
        """Generate test combinations"""
        combinations = []
        standard_types = list(TestConfig.STANDARD_COMBINATIONS.keys())
        
        for i in range(count):
            combination = {
                'name': f"{prefix}_{i:04d}",
                'type': standard_types[i % len(standard_types)] if i % 4 < len(standard_types) else "Custom",
                'formula': TestConfig.VALID_FORMULAS[i % len(TestConfig.VALID_FORMULAS)],
                'description': f"Test combination {i} generated for testing purposes",
                'is_custom': i % 3 == 0,  # Every 3rd is custom
                'include_in_analysis': i % 2 == 0,  # Every 2nd included in analysis
            }
            combinations.append(combination)
        
        return combinations
    
    @staticmethod
    def generate_analysis_results(combination_name):
        """Generate mock analysis results"""
        import random
        
        results = {
            'max_moment': random.uniform(500, 2000),
            'max_shear': random.uniform(200, 1000),
            'max_axial': random.uniform(1000, 5000),
            'max_deflection': random.uniform(0.01, 0.05),
            'critical_member': f"B{random.randint(1, 10)}",
            'max_stress': random.uniform(100, 300),
            'max_displacement': random.uniform(0.005, 0.03)
        }
        
        return results
    
    @staticmethod
    def create_test_file(data, filepath=None):
        """Create a temporary test file with data"""
        if filepath is None:
            fd, filepath = tempfile.mkstemp(suffix='.json')
            os.close(fd)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath


class TestValidator:
    """Validation utilities for tests"""
    
    @staticmethod
    def validate_combination_data(combination_data):
        """Validate combination data structure"""
        required_fields = ['name', 'type', 'formula', 'description']
        
        for field in required_fields:
            if field not in combination_data:
                return False, f"Missing required field: {field}"
        
        # Validate formula format
        formula = combination_data['formula']
        if not TestValidator.validate_formula_syntax(formula):
            return False, f"Invalid formula syntax: {formula}"
        
        return True, "Valid combination data"
    
    @staticmethod
    def validate_formula_syntax(formula):
        """Basic formula syntax validation"""
        import re
        
        if not formula or not formula.strip():
            return False
        
        # Check for valid pattern: number + load_type
        pattern = r'(\d+\.?\d*)\s*\*?\s*([A-Z]{2,3})'
        matches = re.findall(pattern, formula)
        
        if not matches:
            return False
        
        # Check load types are valid
        valid_load_types = set(TestConfig.LOAD_TYPES)
        for factor, load_type in matches:
            if load_type not in valid_load_types:
                return False
        
        return True
    
    @staticmethod
    def validate_analysis_results(results):
        """Validate analysis results structure"""
        required_fields = ['max_moment', 'max_shear', 'max_axial', 'max_deflection']
        
        for field in required_fields:
            if field not in results:
                return False, f"Missing result field: {field}"
            
            if not isinstance(results[field], (int, float)):
                return False, f"Result field {field} must be numeric"
        
        return True, "Valid analysis results"


class TestReporter:
    """Test reporting utilities"""
    
    def __init__(self):
        self.test_results = []
        self.performance_data = {}
    
    def add_test_result(self, test_name, success, duration, details=None):
        """Add a test result"""
        result = {
            'test_name': test_name,
            'success': success,
            'duration': duration,
            'details': details or {},
            'timestamp': self._get_timestamp()
        }
        self.test_results.append(result)
    
    def add_performance_data(self, metric_name, value, unit='ms'):
        """Add performance metric"""
        if metric_name not in self.performance_data:
            self.performance_data[metric_name] = []
        
        self.performance_data[metric_name].append({
            'value': value,
            'unit': unit,
            'timestamp': self._get_timestamp()
        })
    
    def generate_report(self, filepath=None):
        """Generate comprehensive test report"""
        report = {
            'summary': self._generate_summary(),
            'test_results': self.test_results,
            'performance_data': self.performance_data,
            'generated_at': self._get_timestamp()
        }
        
        if filepath:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            return filepath
        
        return report
    
    def _generate_summary(self):
        """Generate test summary"""
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r['success'])
        total_duration = sum(r['duration'] for r in self.test_results)
        
        return {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'failed_tests': total_tests - successful_tests,
            'success_rate': (successful_tests / total_tests * 100) if total_tests > 0 else 0,
            'total_duration': total_duration,
            'average_duration': total_duration / total_tests if total_tests > 0 else 0
        }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


# Test runner utilities
def setup_test_environment():
    """Setup complete test environment"""
    mock_env = MockFreeCADEnvironment()
    return mock_env

def cleanup_test_environment(mock_env):
    """Cleanup test environment"""
    mock_env.cleanup()

def run_test_with_timeout(test_func, timeout=30):
    """Run test function with timeout"""
    import threading
    import time
    
    result = {'success': False, 'error': None, 'duration': 0}
    start_time = time.time()
    
    def target():
        try:
            test_func()
            result['duration'] = time.time() - start_time
            result['success'] = True
        except Exception as e:
            result['error'] = str(e)
            result['duration'] = time.time() - start_time
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        result['error'] = f"Test timed out after {timeout} seconds"
        result['duration'] = timeout
    
    return result


if __name__ == '__main__':
    # Test the test utilities
    print("Testing Load Combination Test Utilities")
    print("=" * 50)
    
    # Test mock environment
    mock_env = setup_test_environment()
    print("✓ Mock environment created")
    
    # Test data generator
    test_data = TestDataGenerator.generate_combinations(5)
    print(f"✓ Generated {len(test_data)} test combinations")
    
    # Test validator
    for combo in test_data:
        valid, message = TestValidator.validate_combination_data(combo)
        if not valid:
            print(f"✗ Validation failed: {message}")
            break
    else:
        print("✓ All test data validated successfully")
    
    # Test reporter
    reporter = TestReporter()
    reporter.add_test_result("Sample Test", True, 0.123)
    reporter.add_performance_data("sample_metric", 42.5)
    
    report = reporter.generate_report()
    print(f"✓ Test report generated with {len(report['test_results'])} results")
    
    # Cleanup
    cleanup_test_environment(mock_env)
    print("✓ Test environment cleaned up")
    
    print("\nAll test utilities working correctly!")
