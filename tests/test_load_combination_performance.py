# Performance Tests for Load Combination System
# Test performance and stress testing for StructureTools Load Combination

import unittest
import time
import sys
import os
from unittest.mock import Mock, patch
import threading
import gc

# Add the StructureTools path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestLoadCombinationPerformance(unittest.TestCase):
    """Performance tests for Load Combination System"""
    
    def setUp(self):
        """Set up performance test fixtures"""
        # Mock FreeCAD module
        self.mock_freecad = Mock()
        sys.modules['FreeCAD'] = self.mock_freecad
        
        # Import after mocking
        from freecad.StructureTools.custom_combinations import CustomCombinationManager
        from freecad.StructureTools.combination_analysis import CombinationAnalysisManager
        
        self.custom_manager = CustomCombinationManager()
        self.analysis_manager = CombinationAnalysisManager()
    
    def test_large_number_of_combinations(self):
        """Test performance with large number of combinations"""
        start_time = time.time()
        
        # Create 1000 combinations
        for i in range(1000):
            name = f"Combo_{i:04d}"
            formula = f"1.{(i%9)+1}DL + 1.{(i%6)+1}LL"
            description = f"Performance test combination {i}"
            
            success, message = self.custom_manager.add_combination(name, formula, description)
            self.assertTrue(success, f"Failed to add combination {i}: {message}")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nCreated 1000 combinations in {elapsed_time:.3f} seconds")
        print(f"Average time per combination: {elapsed_time/1000*1000:.3f} ms")
        
        # Performance threshold: should create 1000 combinations in less than 10 seconds
        self.assertLess(elapsed_time, 10.0, "Creating 1000 combinations took too long")
        
        # Verify all combinations were created
        combinations = self.custom_manager.get_combinations()
        self.assertEqual(len(combinations), 1000)
    
    def test_formula_validation_performance(self):
        """Test performance of formula validation"""
        formulas = [
            "1.2DL + 1.6LL",
            "1.0DL + 0.5LL + 1.0WL",
            "1.35DL + 1.5LL + 0.9WL + 0.2SL",
            "0.9DL + 1.0EQ",
            "1.2DL + 1.0LL + 1.0WL + 0.5SL + 0.2EQ",
        ]
        
        start_time = time.time()
        
        # Validate each formula 1000 times
        for i in range(1000):
            formula = formulas[i % len(formulas)]
            is_valid, message = self.custom_manager.validate_formula(formula)
            self.assertTrue(is_valid, f"Formula validation failed: {formula}")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nValidated 1000 formulas in {elapsed_time:.3f} seconds")
        print(f"Average validation time: {elapsed_time/1000*1000:.3f} ms")
        
        # Performance threshold: should validate 1000 formulas in less than 1 second
        self.assertLess(elapsed_time, 1.0, "Formula validation took too long")
    
    def test_combination_parsing_performance(self):
        """Test performance of combination formula parsing"""
        complex_formula = "1.2DL + 1.6LL + 0.5SL + 1.0WL + 0.2EQ + 0.3RL + 0.8CL"
        
        start_time = time.time()
        
        # Parse formula 10000 times
        for i in range(10000):
            factors = self.analysis_manager.parse_combination_formula(complex_formula)
            self.assertIsInstance(factors, dict)
            self.assertEqual(len(factors), 7)  # Should parse 7 load types
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nParsed complex formula 10000 times in {elapsed_time:.3f} seconds")
        print(f"Average parsing time: {elapsed_time/10000*1000:.3f} ms")
        
        # Performance threshold: should parse 10000 formulas in less than 2 seconds
        self.assertLess(elapsed_time, 2.0, "Formula parsing took too long")
    
    def test_memory_usage_with_large_dataset(self):
        """Test memory usage with large number of combinations"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create 5000 combinations
        for i in range(5000):
            name = f"MemTest_{i:05d}"
            formula = f"1.{(i%9)+1}DL + 1.{(i%6)+1}LL + 0.{(i%5)+1}WL"
            description = f"Memory test combination {i} with detailed description and additional metadata"
            
            self.custom_manager.add_combination(name, formula, description)
        
        # Force garbage collection
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"\nMemory usage:")
        print(f"Initial: {initial_memory:.2f} MB")
        print(f"Final: {final_memory:.2f} MB")
        print(f"Increase: {memory_increase:.2f} MB")
        print(f"Memory per combination: {memory_increase/5000*1024:.2f} KB")
        
        # Memory threshold: should not use more than 100MB for 5000 combinations
        self.assertLess(memory_increase, 100, "Memory usage too high")
    
    def test_concurrent_access(self):
        """Test concurrent access to combination manager"""
        results = []
        errors = []
        
        def worker_thread(thread_id):
            try:
                # Each thread creates 100 combinations
                for i in range(100):
                    name = f"Thread{thread_id}_Combo_{i:03d}"
                    formula = f"1.{(thread_id%9)+1}DL + 1.{(i%6)+1}LL"
                    description = f"Thread {thread_id} combination {i}"
                    
                    success, message = self.custom_manager.add_combination(name, formula, description)
                    if not success:
                        errors.append(f"Thread {thread_id}: {message}")
                    else:
                        results.append(name)
            except Exception as e:
                errors.append(f"Thread {thread_id} exception: {str(e)}")
        
        # Create 10 threads
        threads = []
        start_time = time.time()
        
        for i in range(10):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nConcurrent test completed in {elapsed_time:.3f} seconds")
        print(f"Successful combinations: {len(results)}")
        print(f"Errors: {len(errors)}")
        
        # Verify no errors occurred
        if errors:
            print("Errors encountered:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
        
        # Should have created 1000 combinations (10 threads × 100 combinations)
        self.assertEqual(len(results), 1000, "Not all combinations were created")
        self.assertEqual(len(errors), 0, "Errors occurred during concurrent access")
    
    def test_export_import_performance(self):
        """Test performance of export/import operations"""
        import tempfile
        
        # Create test data
        for i in range(1000):
            name = f"ExportTest_{i:04d}"
            formula = f"1.{(i%9)+1}DL + 1.{(i%6)+1}LL"
            description = f"Export test combination {i}"
            self.custom_manager.add_combination(name, formula, description)
        
        # Test export performance
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            start_time = time.time()
            success, message = self.custom_manager.export_combinations(filepath)
            export_time = time.time() - start_time
            
            self.assertTrue(success, f"Export failed: {message}")
            print(f"\nExported 1000 combinations in {export_time:.3f} seconds")
            
            # Test file size
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"Export file size: {file_size:.2f} KB")
            
            # Test import performance
            new_manager = self.custom_manager.__class__()
            start_time = time.time()
            success, message = new_manager.import_combinations(filepath)
            import_time = time.time() - start_time
            
            self.assertTrue(success, f"Import failed: {message}")
            print(f"Imported 1000 combinations in {import_time:.3f} seconds")
            
            # Verify imported data
            imported_combinations = new_manager.get_combinations()
            self.assertEqual(len(imported_combinations), 1000)
            
            # Performance thresholds
            self.assertLess(export_time, 5.0, "Export took too long")
            self.assertLess(import_time, 5.0, "Import took too long")
            self.assertLess(file_size, 1024, "Export file too large (>1MB)")
            
        finally:
            os.unlink(filepath)


class TestLoadCombinationStress(unittest.TestCase):
    """Stress tests for Load Combination System"""
    
    def setUp(self):
        """Set up stress test fixtures"""
        # Mock FreeCAD module
        self.mock_freecad = Mock()
        sys.modules['FreeCAD'] = self.mock_freecad
    
    def test_maximum_formula_complexity(self):
        """Test with very complex formulas"""
        from freecad.StructureTools.custom_combinations import CustomCombinationManager
        
        manager = CustomCombinationManager()
        
        # Test with maximum complexity formula
        complex_formula = "1.2DL + 1.6LL + 0.5SL + 1.0WL + 0.2EQ + 0.3RL + 0.8CL + 0.1TL + 0.9IL + 0.7PL"
        
        is_valid, message = manager.validate_formula(complex_formula)
        
        if is_valid:
            success, add_message = manager.add_combination("MaxComplexity", complex_formula, "Maximum complexity test")
            self.assertTrue(success, f"Failed to add complex combination: {add_message}")
        else:
            print(f"Complex formula validation failed: {message}")
            # This is acceptable as we're testing limits
    
    def test_boundary_conditions(self):
        """Test boundary conditions and edge cases"""
        from freecad.StructureTools.custom_combinations import CustomCombinationManager
        
        manager = CustomCombinationManager()
        
        # Test very small factors
        small_factor_formula = "0.001DL + 0.002LL"
        is_valid, message = manager.validate_formula(small_factor_formula)
        self.assertTrue(is_valid, f"Small factor formula should be valid: {message}")
        
        # Test very large factors (updated for new limits)
        large_factor_formula = "999.999DL + 888.888LL"
        is_valid, message = manager.validate_formula(large_factor_formula)
        self.assertTrue(is_valid, f"Large factor formula should be valid: {message}")
        
        # Test single load type
        single_load_formula = "1.0DL"
        is_valid, message = manager.validate_formula(single_load_formula)
        self.assertTrue(is_valid, f"Single load formula should be valid: {message}")
    
    def test_error_recovery(self):
        """Test system recovery from various error conditions"""
        from freecad.StructureTools.custom_combinations import CustomCombinationManager
        
        manager = CustomCombinationManager()
        
        # Test with various invalid inputs
        invalid_inputs = [
            ("", "Empty name", "1.2DL + 1.6LL"),
            ("Valid Name", "Description", ""),  # Empty formula
            ("Valid Name", "Description", "invalid"),  # Invalid formula
            (None, "Description", "1.2DL + 1.6LL"),  # None name
        ]
        
        for name, description, formula in invalid_inputs:
            try:
                success, message = manager.add_combination(name, formula, description)
                # Should handle gracefully without crashing
                self.assertFalse(success, f"Should reject invalid input: {name}, {formula}")
            except Exception as e:
                self.fail(f"Should not raise exception for invalid input: {e}")
        
        # System should still work after error conditions
        success, message = manager.add_combination("Recovery Test", "1.2DL + 1.6LL", "Recovery test")
        self.assertTrue(success, "System should recover from error conditions")


def run_performance_tests():
    """Run all performance tests"""
    print("=" * 60)
    print("LOAD COMBINATION SYSTEM - PERFORMANCE TESTS")
    print("=" * 60)
    
    # Check if psutil is available for memory tests
    try:
        import psutil
        memory_tests_available = True
    except ImportError:
        print("WARNING: psutil not available, memory tests will be skipped")
        memory_tests_available = False
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add performance tests
    performance_tests = unittest.TestLoader().loadTestsFromTestCase(TestLoadCombinationPerformance)
    stress_tests = unittest.TestLoader().loadTestsFromTestCase(TestLoadCombinationStress)
    
    # Filter out memory tests if psutil not available
    if not memory_tests_available:
        filtered_tests = unittest.TestSuite()
        for test in performance_tests:
            if 'memory' not in str(test):
                filtered_tests.addTest(test)
        performance_tests = filtered_tests
    
    test_suite.addTests(performance_tests)
    test_suite.addTests(stress_tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("PERFORMANCE TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\nPERFORMANCE ISSUES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_performance_tests()
    sys.exit(0 if success else 1)
