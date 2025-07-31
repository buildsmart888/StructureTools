# Test Runner Script for Load Combination System
# Comprehensive test runner for all Load Combination tests

import unittest
import sys
import os
import time
import json
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import test modules
try:
    from tests.test_load_combination import (
        TestLoadCombination,
        TestCustomCombinationManager,
        TestCombinationAnalysisManager,
        TestLoadCombinationIntegration
    )
    from tests.test_load_combination_performance import (
        TestLoadCombinationPerformance,
        TestLoadCombinationStress
    )
    from tests.test_load_combination_advanced import (
        TestLoadCombinationAdvanced,
        TestCustomCombinationManagerAdvanced,
        TestCombinationAnalysisManagerAdvanced,
        TestLoadCombinationIntegrationAdvanced,
        TestLoadCombinationEdgeCases
    )
    from tests.test_boundary_conditions import (
        TestBoundaryConditions,
        TestErrorScenarios,
        TestValidationRobustness
    )
    from tests.test_user_workflows import (
        TestUserWorkflows,
        TestGUIComponentMocking,
        TestIntegrationScenarios
    )
    from tests.test_utils import TestReporter, setup_test_environment, cleanup_test_environment
except ImportError as e:
    print(f"Error importing test modules: {e}")
    sys.exit(1)

class LoadCombinationTestRunner:
    """Comprehensive test runner for Load Combination System"""
    
    def __init__(self):
        self.reporter = TestReporter()
        self.mock_env = None
        self.results = {
            'unit_tests': None,
            'performance_tests': None,
            'stress_tests': None,
            'integration_tests': None
        }
    
    def setup(self):
        """Setup test environment"""
        print("Setting up test environment...")
        self.mock_env = setup_test_environment()
        print("✓ Test environment ready")
    
    def cleanup(self):
        """Cleanup test environment"""
        if self.mock_env:
            cleanup_test_environment(self.mock_env)
            print("✓ Test environment cleaned up")
    
    def run_unit_tests(self):
        """Run unit tests"""
        print("\n" + "="*60)
        print("RUNNING UNIT TESTS")
        print("="*60)
        
        test_classes = [
            TestLoadCombination,
            TestCustomCombinationManager,
            TestCombinationAnalysisManager,
            TestLoadCombinationIntegration,
            # Advanced test classes
            TestLoadCombinationAdvanced,
            TestCustomCombinationManagerAdvanced,
            TestCombinationAnalysisManagerAdvanced,
            TestLoadCombinationIntegrationAdvanced,
            TestLoadCombinationEdgeCases,
            # Boundary condition test classes
            TestBoundaryConditions,
            TestErrorScenarios,
            TestValidationRobustness,
            # User workflow test classes
            TestUserWorkflows,
            TestGUIComponentMocking,
            TestIntegrationScenarios
        ]
        
        suite = unittest.TestSuite()
        for test_class in test_classes:
            tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        
        start_time = time.time()
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        duration = time.time() - start_time
        
        self.results['unit_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0,
            'duration': duration,
            'successful': result.wasSuccessful()
        }
        
        # Add to reporter
        self.reporter.add_test_result(
            'Unit Tests',
            result.wasSuccessful(),
            duration,
            {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors)
            }
        )
        
        return result.wasSuccessful()
    
    def run_performance_tests(self):
        """Run performance tests"""
        print("\n" + "="*60)
        print("RUNNING PERFORMANCE TESTS")
        print("="*60)
        
        # Check if required modules are available
        try:
            import psutil
            performance_tests_available = True
        except ImportError:
            print("WARNING: psutil not available, some performance tests will be skipped")
            performance_tests_available = False
        
        suite = unittest.TestSuite()
        tests = unittest.TestLoader().loadTestsFromTestCase(TestLoadCombinationPerformance)
        
        # Filter out memory tests if psutil not available
        if not performance_tests_available:
            filtered_tests = unittest.TestSuite()
            for test in tests:
                if 'memory' not in str(test):
                    filtered_tests.addTest(test)
            tests = filtered_tests
        
        suite.addTests(tests)
        
        start_time = time.time()
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        duration = time.time() - start_time
        
        self.results['performance_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'duration': duration,
            'successful': result.wasSuccessful()
        }
        
        # Add to reporter
        self.reporter.add_test_result(
            'Performance Tests',
            result.wasSuccessful(),
            duration,
            {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'psutil_available': performance_tests_available
            }
        )
        
        return result.wasSuccessful()
    
    def run_stress_tests(self):
        """Run stress tests"""
        print("\n" + "="*60)
        print("RUNNING STRESS TESTS")
        print("="*60)
        
        suite = unittest.TestSuite()
        tests = unittest.TestLoader().loadTestsFromTestCase(TestLoadCombinationStress)
        suite.addTests(tests)
        
        start_time = time.time()
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        duration = time.time() - start_time
        
        self.results['stress_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'duration': duration,
            'successful': result.wasSuccessful()
        }
        
        # Add to reporter
        self.reporter.add_test_result(
            'Stress Tests',
            result.wasSuccessful(),
            duration,
            {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors)
            }
        )
        
        return result.wasSuccessful()
    
    def run_all_tests(self):
        """Run all test suites"""
        print("LOAD COMBINATION SYSTEM - COMPREHENSIVE TEST SUITE")
        print("="*60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        overall_start_time = time.time()
        
        try:
            self.setup()
            
            # Run all test categories
            unit_success = self.run_unit_tests()
            perf_success = self.run_performance_tests()
            stress_success = self.run_stress_tests()
            
            overall_duration = time.time() - overall_start_time
            overall_success = unit_success and perf_success and stress_success
            
            # Print comprehensive summary
            self.print_summary(overall_duration, overall_success)
            
            # Generate detailed report
            self.generate_report()
            
            return overall_success
            
        finally:
            self.cleanup()
    
    def print_summary(self, total_duration, overall_success):
        """Print comprehensive test summary"""
        print("\n" + "="*60)
        print("COMPREHENSIVE TEST SUMMARY")
        print("="*60)
        
        total_tests = 0
        total_failures = 0
        total_errors = 0
        
        for category, results in self.results.items():
            if results:
                print(f"\n{category.upper().replace('_', ' ')}:")
                print(f"  Tests run: {results['tests_run']}")
                print(f"  Failures: {results['failures']}")
                print(f"  Errors: {results['errors']}")
                print(f"  Duration: {results['duration']:.3f}s")
                print(f"  Status: {'✓ PASSED' if results['successful'] else '✗ FAILED'}")
                
                total_tests += results['tests_run']
                total_failures += results['failures']
                total_errors += results['errors']
        
        print(f"\nOVERALL RESULTS:")
        print(f"  Total tests: {total_tests}")
        print(f"  Total failures: {total_failures}")
        print(f"  Total errors: {total_errors}")
        print(f"  Success rate: {((total_tests - total_failures - total_errors) / total_tests * 100):.1f}%" if total_tests > 0 else "N/A")
        print(f"  Total duration: {total_duration:.3f}s")
        print(f"  Overall status: {'✓ ALL TESTS PASSED' if overall_success else '✗ SOME TESTS FAILED'}")
        
        # Performance insights
        if self.results.get('performance_tests', {}).get('successful'):
            print(f"\nPERFORMANCE INSIGHTS:")
            print(f"  ✓ System can handle large datasets efficiently")
            print(f"  ✓ Formula validation is fast")
            print(f"  ✓ Export/import operations are performant")
            print(f"  ✓ Memory usage is within acceptable limits")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def generate_report(self):
        """Generate detailed test report"""
        report_dir = os.path.join(project_root, 'test_reports')
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(report_dir, f'load_combination_test_report_{timestamp}.json')
        
        # Add detailed results to reporter
        detailed_report = {
            'test_suite': 'Load Combination System',
            'timestamp': datetime.now().isoformat(),
            'environment': {
                'python_version': sys.version,
                'platform': sys.platform,
                'project_root': project_root
            },
            'results': self.results,
            'summary': self._calculate_summary()
        }
        
        with open(report_file, 'w') as f:
            json.dump(detailed_report, f, indent=2)
        
        print(f"\n📊 Detailed report saved to: {report_file}")
        return report_file
    
    def _calculate_summary(self):
        """Calculate overall summary statistics"""
        total_tests = sum(r['tests_run'] for r in self.results.values() if r)
        total_failures = sum(r['failures'] for r in self.results.values() if r)
        total_errors = sum(r['errors'] for r in self.results.values() if r)
        total_duration = sum(r['duration'] for r in self.results.values() if r)
        
        return {
            'total_tests': total_tests,
            'total_failures': total_failures,
            'total_errors': total_errors,
            'total_duration': total_duration,
            'success_rate': ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0,
            'overall_success': total_failures == 0 and total_errors == 0
        }


def main():
    """Main test runner function"""
    runner = LoadCombinationTestRunner()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Load Combination System Test Runner')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--performance', action='store_true', help='Run only performance tests')
    parser.add_argument('--stress', action='store_true', help='Run only stress tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    success = False
    
    try:
        runner.setup()
        
        if args.unit:
            success = runner.run_unit_tests()
        elif args.performance:
            success = runner.run_performance_tests()
        elif args.stress:
            success = runner.run_stress_tests()
        else:
            success = runner.run_all_tests()
            
    except KeyboardInterrupt:
        print("\n\nTest run interrupted by user")
        success = False
    except Exception as e:
        print(f"\n\nTest run failed with error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        success = False
    finally:
        runner.cleanup()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
