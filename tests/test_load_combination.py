# Unit Tests for Load Combination System
# Test suite for StructureTools Load Combination functionality

import unittest
import sys
import os
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock

# Add the StructureTools path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestLoadCombination(unittest.TestCase):
    """Test cases for LoadCombination class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        # Mock all FreeCAD modules
        self.mock_freecad = Mock()
        self.mock_app = Mock()
        self.mock_freecadgui = Mock()
        self.mock_part = Mock()
        
        sys.modules['FreeCAD'] = self.mock_freecad
        sys.modules['App'] = self.mock_app
        sys.modules['FreeCADGui'] = self.mock_freecadgui
        sys.modules['Part'] = self.mock_part
        
        # Mock PySide modules  
        self.mock_pyside = Mock()
        self.mock_qtwidgets = Mock()
        self.mock_qtcore = Mock()
        self.mock_qtgui = Mock()
        
        sys.modules['PySide'] = self.mock_pyside
        sys.modules['PySide.QtWidgets'] = self.mock_qtwidgets
        sys.modules['PySide.QtCore'] = self.mock_qtcore
        sys.modules['PySide.QtGui'] = self.mock_qtgui
        
        # Mock PySide2 modules as well
        sys.modules['PySide2'] = Mock()
        sys.modules['PySide2.QtWidgets'] = self.mock_qtwidgets
        sys.modules['PySide2.QtCore'] = self.mock_qtcore
        sys.modules['PySide2.QtGui'] = self.mock_qtgui
        
        # Import after mocking all dependencies
        from freecad.StructureTools.load_combination import LoadCombination
        self.LoadCombination = LoadCombination
        
        # Create test object
        self.mock_obj = Mock()
        self.mock_obj.CombinationName = "Test Combination"
        self.mock_obj.CombinationType = "ACI 318"
        self.mock_obj.Description = "Test description"
        self.mock_obj.CombinationFormula = "1.2DL + 1.6LL"
        self.mock_obj.IsCustomFormula = False
        self.mock_obj.CustomFormula = ""
        self.mock_obj.IncludeInAnalysis = True
        self.mock_obj.MaxMoment = 0.0
        self.mock_obj.MaxShear = 0.0
        self.mock_obj.MaxAxial = 0.0
        self.mock_obj.MaxDeflection = 0.0
        self.mock_obj.CriticalMember = ""
        self.mock_obj.IsCritical = False
        
        # Create LoadCombination instance with required parameters
        combination_data = {
            'name': 'Test Combination',
            'type': 'Custom',
            'description': 'Test description'
        }
        self.combination = self.LoadCombination(self.mock_obj, combination_data)
    
    def test_initialization(self):
        """Test LoadCombination initialization"""
        self.assertIsNotNone(self.combination)
        self.assertTrue(hasattr(self.combination, 'execute'))
        self.assertTrue(hasattr(self.combination, 'onChanged'))
    
    def test_get_standard_combinations_aci318(self):
        """Test ACI 318 standard combinations"""
        self.mock_obj.CombinationType = "ACI 318"
        self.mock_obj.CombinationIndex = 0
        
        combinations = self.combination.get_standard_combinations(self.mock_obj)
        
        self.assertIsInstance(combinations, list)
        self.assertGreater(len(combinations), 0)
        # Check if first combination is strength combination (ACI 318 standard)
        self.assertIn("1.4DL", combinations[0])
    
    def test_get_standard_combinations_aisc360(self):
        """Test AISC 360 standard combinations"""
        self.mock_obj.CombinationType = "AISC 360"
        self.mock_obj.CombinationIndex = 0
        
        combinations = self.combination.get_standard_combinations(self.mock_obj)
        
        self.assertIsInstance(combinations, list)
        self.assertGreater(len(combinations), 0)
        # Check if first combination is basic LRFD
        self.assertIn("1.4DL", combinations[0])
    
    def test_get_standard_combinations_eurocode(self):
        """Test Eurocode standard combinations"""
        self.mock_obj.CombinationType = "Eurocode"
        self.mock_obj.CombinationIndex = 0
        
        combinations = self.combination.get_standard_combinations(self.mock_obj)
        
        self.assertIsInstance(combinations, list)
        self.assertGreater(len(combinations), 0)
        # Check if first combination is ULS (Eurocode standard)
        self.assertIn("1.35DL", combinations[0])
    
    def test_get_standard_combinations_ibc2018(self):
        """Test IBC 2018 standard combinations"""
        self.mock_obj.CombinationType = "IBC 2018"
        self.mock_obj.CombinationIndex = 0
        
        combinations = self.combination.get_standard_combinations(self.mock_obj)
        
        self.assertIsInstance(combinations, list)
        self.assertGreater(len(combinations), 0)
        # Check if first combination is basic (IBC 2018 standard)
        self.assertIn("1.4DL", combinations[0])
    
    def test_execute(self):
        """Test execute method"""
        # Mock successful execution
        result = self.combination.execute(self.mock_obj)
        # Should not raise any exceptions
        self.assertIsNone(result)
    
    @patch('freecad.StructureTools.load_combination.FreeCAD')
    def test_run_analysis_no_document(self, mock_freecad):
        """Test run_analysis with no active document"""
        mock_freecad.ActiveDocument = None
        
        success, message = self.combination.run_analysis(self.mock_obj)
        
        self.assertFalse(success)
        self.assertIn("No active document", message)
    
    @patch('freecad.StructureTools.load_combination.FreeCAD')
    def test_run_analysis_no_calc_object(self, mock_freecad):
        """Test run_analysis with no calc object"""
        mock_doc = Mock()
        mock_doc.Objects = []
        mock_freecad.ActiveDocument = mock_doc
        
        success, message = self.combination.run_analysis(self.mock_obj)
        
        self.assertFalse(success)
        self.assertIn("No calc object found", message)


class TestCustomCombinationManager(unittest.TestCase):
    """Test cases for CustomCombinationManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock FreeCAD
        self.mock_freecad = Mock()
        sys.modules['FreeCAD'] = self.mock_freecad
        
        from freecad.StructureTools.custom_combinations import CustomCombinationManager
        self.manager = CustomCombinationManager()
    
    def test_initialization(self):
        """Test CustomCombinationManager initialization"""
        self.assertIsNotNone(self.manager)
        self.assertIsInstance(self.manager.combinations, dict)
    
    def test_validate_formula_valid(self):
        """Test formula validation with valid formulas"""
        valid_formulas = [
            "1.2DL + 1.6LL",
            "1.0DL + 0.5LL + 1.0WL",
            "0.9DL + 1.0EQ",
            "1.2*DL + 1.6*LL",
            "1.35DL + 1.5LL + 0.9WL"
        ]
        
        for formula in valid_formulas:
            with self.subTest(formula=formula):
                is_valid, message = self.manager.validate_formula(formula)
                self.assertTrue(is_valid, f"Formula '{formula}' should be valid: {message}")
    
    def test_validate_formula_invalid(self):
        """Test formula validation with invalid formulas"""
        invalid_formulas = [
            "",  # Empty formula
            "1.2XL + 1.6LL",  # Invalid load type
            "DL + LL",  # Missing factors
            "-1.2DL + 1.6LL",  # Negative factor
            "1.2DL +",  # Incomplete formula
            "1.2DL 1.6LL",  # Missing operator
        ]
        
        for formula in invalid_formulas:
            with self.subTest(formula=formula):
                is_valid, message = self.manager.validate_formula(formula)
                self.assertFalse(is_valid, f"Formula '{formula}' should be invalid")
    
    def test_add_combination(self):
        """Test adding custom combinations"""
        name = "Test Combo"
        formula = "1.2DL + 1.6LL"
        description = "Test combination"
        
        success, message = self.manager.add_combination(name, formula, description)
        
        self.assertTrue(success)
        self.assertIn(name, self.manager.combinations)
        self.assertEqual(self.manager.combinations[name]['formula'], formula)
        self.assertEqual(self.manager.combinations[name]['description'], description)
    
    def test_add_combination_invalid_formula(self):
        """Test adding combination with invalid formula"""
        name = "Invalid Combo"
        formula = "invalid formula"
        description = "Test"
        
        success, message = self.manager.add_combination(name, formula, description)
        
        self.assertFalse(success)
        self.assertNotIn(name, self.manager.combinations)
    
    def test_get_combinations(self):
        """Test getting all combinations"""
        # Add test combinations
        self.manager.add_combination("Combo1", "1.2DL + 1.6LL", "Test 1")
        self.manager.add_combination("Combo2", "1.0DL + 1.0WL", "Test 2")
        
        combinations = self.manager.get_combinations()
        
        # Now expects list format
        self.assertIsInstance(combinations, list)
        self.assertEqual(len(combinations), 2)
        
        # Check that combinations exist by name
        combo_names = [c['name'] for c in combinations]
        self.assertIn("Combo1", combo_names)
        self.assertIn("Combo2", combo_names)
    
    def test_export_import_combinations(self):
        """Test export and import functionality"""
        # Add test data
        self.manager.add_combination("Test1", "1.2DL + 1.6LL", "Description 1")
        self.manager.add_combination("Test2", "1.0DL + 1.0WL", "Description 2")
        
        # Test export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            success, message = self.manager.export_combinations(filepath)
            self.assertTrue(success)
            self.assertTrue(os.path.exists(filepath))
            
            # Test import
            new_manager = self.manager.__class__()
            success, message = new_manager.import_combinations(filepath)
            self.assertTrue(success)
            
            # Verify imported data
            imported_combinations = new_manager.get_combinations()
            combo_names = [c['name'] for c in imported_combinations]
            self.assertIn("Test1", combo_names)
            self.assertIn("Test2", combo_names)
            
            # Find Test1 combination and verify
            test1_combo = next((c for c in imported_combinations if c['name'] == 'Test1'), None)
            self.assertIsNotNone(test1_combo)
            self.assertEqual(test1_combo['formula'], "1.2DL + 1.6LL")
            
        finally:
            os.unlink(filepath)


class TestCombinationAnalysisManager(unittest.TestCase):
    """Test cases for CombinationAnalysisManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock FreeCAD
        self.mock_freecad = Mock()
        sys.modules['FreeCAD'] = self.mock_freecad
        
        from freecad.StructureTools.combination_analysis import CombinationAnalysisManager
        self.manager = CombinationAnalysisManager()
        
        # Create mock combination object
        self.mock_combination = Mock()
        self.mock_combination.CombinationName = "Test Combo"
        self.mock_combination.CombinationFormula = "1.2DL + 1.6LL"
        self.mock_combination.MaxMoment = 0.0
        self.mock_combination.MaxShear = 0.0
        self.mock_combination.MaxAxial = 0.0
        self.mock_combination.MaxDeflection = 0.0
        self.mock_combination.CriticalMember = ""
        self.mock_combination.IsCritical = False
        
        # Create mock calc object
        self.mock_calc = Mock()
        self.mock_calc.Proxy = Mock()
        self.mock_calc.Proxy.execute = Mock()
    
    def test_initialization(self):
        """Test CombinationAnalysisManager initialization"""
        self.assertIsNotNone(self.manager)
        self.assertIsInstance(self.manager.analysis_results, dict)
        self.assertIsInstance(self.manager.critical_combinations, dict)
    
    def test_parse_combination_formula(self):
        """Test parsing combination formulas"""
        formula = "1.2DL + 1.6LL + 0.5WL"
        
        factors = self.manager.parse_combination_formula(formula)
        
        self.assertIsInstance(factors, dict)
        self.assertEqual(factors.get("DL"), 1.2)
        self.assertEqual(factors.get("LL"), 1.6)
        self.assertEqual(factors.get("WL"), 0.5)
    
    def test_parse_combination_formula_with_multiplication(self):
        """Test parsing formulas with explicit multiplication"""
        formula = "1.2*DL + 1.6*LL"
        
        factors = self.manager.parse_combination_formula(formula)
        
        self.assertIsInstance(factors, dict)
        self.assertEqual(factors.get("DL"), 1.2)
        self.assertEqual(factors.get("LL"), 1.6)
    
    def test_store_results(self):
        """Test storing analysis results"""
        results = {
            'max_moment': 1500.0,
            'max_shear': 800.0,
            'max_axial': 2000.0,
            'max_deflection': 0.03,
            'critical_member': 'B1'
        }
        
        self.manager.store_results(self.mock_combination, results)
        
        # Verify results are stored in combination object
        self.assertEqual(self.mock_combination.MaxMoment, 1500.0)
        self.assertEqual(self.mock_combination.MaxShear, 800.0)
        self.assertEqual(self.mock_combination.MaxAxial, 2000.0)
        self.assertEqual(self.mock_combination.MaxDeflection, 0.03)
        self.assertEqual(self.mock_combination.CriticalMember, 'B1')
        
        # Verify results are stored in internal tracking
        self.assertIn(self.mock_combination.CombinationName, self.manager.analysis_results)
    
    def test_find_critical_combination_moment(self):
        """Test finding critical combination based on moment"""
        # Create multiple combinations with different results
        combo1 = Mock()
        combo1.CombinationName = "Combo1"
        combo1.MaxMoment = 1000.0
        combo1.IsCritical = False
        
        combo2 = Mock()
        combo2.CombinationName = "Combo2"
        combo2.MaxMoment = 1500.0  # This should be critical
        combo2.IsCritical = False
        
        combo3 = Mock()
        combo3.CombinationName = "Combo3"
        combo3.MaxMoment = 1200.0
        combo3.IsCritical = False
        
        combinations = [combo1, combo2, combo3]
        
        critical_combo, message = self.manager.find_critical_combination(combinations, 'moment')
        
        self.assertIsNotNone(critical_combo)
        # Updated assertion for new format
        if isinstance(critical_combo, dict):
            self.assertEqual(critical_combo.get('combination_name'), "Combo2")
        else:
            self.assertEqual(critical_combo.CombinationName, "Combo2")
            # Check if IsCritical was set (may not be available in test mode)
            if hasattr(critical_combo, 'IsCritical'):
                self.assertTrue(critical_combo.IsCritical)
    
    def test_find_critical_combination_empty_list(self):
        """Test finding critical combination with empty list"""
        critical_combo, message = self.manager.find_critical_combination([], 'moment')
        
        self.assertIsNone(critical_combo)
        self.assertIn("No combinations provided", message)
    
    def test_export_analysis_report(self):
        """Test exporting analysis report"""
        # Setup test data
        combo1 = Mock()
        combo1.CombinationName = "Test1"
        combo1.CombinationFormula = "1.2DL + 1.6LL"
        combo1.CombinationType = "ACI 318"
        combo1.MaxMoment = 1000.0
        combo1.MaxShear = 500.0
        combo1.MaxAxial = 1500.0
        combo1.MaxDeflection = 0.02
        combo1.CriticalMember = "B1"
        combo1.IsCritical = False
        
        combinations = [combo1]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            # Use corrected parameter order
            success, message = self.manager.export_analysis_report(filepath, combinations)
            
            self.assertTrue(success)
            self.assertTrue(os.path.exists(filepath))
            
            # Verify exported data
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.assertIn('project', data)
            self.assertIn('combinations', data)
            self.assertEqual(len(data['combinations']), 1)
            self.assertEqual(data['combinations'][0]['name'], "Test1")
            
        finally:
            os.unlink(filepath)


class TestLoadCombinationIntegration(unittest.TestCase):
    """Integration tests for the complete Load Combination System"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        # Mock FreeCAD and related modules
        self.mock_freecad = Mock()
        sys.modules['FreeCAD'] = self.mock_freecad
        
        # Mock document
        self.mock_doc = Mock()
        self.mock_doc.Objects = []
        self.mock_freecad.ActiveDocument = self.mock_doc
        self.mock_freecad.newDocument = Mock(return_value=self.mock_doc)
    
    @patch('freecad.StructureTools.load_combination.FreeCAD')
    def test_create_and_analyze_combination(self, mock_freecad):
        """Test creating and analyzing a complete combination"""
        mock_freecad.ActiveDocument = self.mock_doc
        
        # Import modules after mocking
        from freecad.StructureTools.load_combination import makeLoadCombination
        from freecad.StructureTools.combination_analysis import combination_analysis_manager
        
        # Create combination
        combo = makeLoadCombination()
        self.assertIsNotNone(combo)
        
        # Mock calc object
        mock_calc = Mock()
        mock_calc.Proxy = Mock()
        mock_calc.Proxy.execute = Mock()
        
        # Test analysis (this will use placeholder results)
        success, message = combination_analysis_manager.run_combination_analysis(combo, mock_calc)
        
        # Should succeed with mock data
        self.assertTrue(success)
    
    def test_full_workflow_with_export(self):
        """Test complete workflow including export"""
        from freecad.StructureTools.custom_combinations import CustomCombinationManager
        from freecad.StructureTools.combination_analysis import combination_analysis_manager
        
        # Create custom combination manager
        manager = CustomCombinationManager()
        
        # Add combinations
        success1, _ = manager.add_combination("Combo1", "1.2DL + 1.6LL", "Test combo 1")
        success2, _ = manager.add_combination("Combo2", "1.0DL + 1.0WL", "Test combo 2")
        
        self.assertTrue(success1)
        self.assertTrue(success2)
        
        # Test export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name
        
        try:
            success, message = manager.export_combinations(filepath)
            self.assertTrue(success)
            
            # Test import
            new_manager = CustomCombinationManager()
            success, message = new_manager.import_combinations(filepath)
            self.assertTrue(success)
            
            # Verify data consistency
            original_combos = manager.get_combinations()
            imported_combos = new_manager.get_combinations()
            self.assertEqual(len(original_combos), len(imported_combos))
            
        finally:
            os.unlink(filepath)


def run_all_tests():
    """Run all unit tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestLoadCombination,
        TestCustomCombinationManager,
        TestCombinationAnalysisManager,
        TestLoadCombinationIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split()[-1] if traceback else 'Unknown failure'}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split()[-1] if traceback else 'Unknown error'}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Print test information
    print("=" * 60)
    print("LOAD COMBINATION SYSTEM - UNIT TESTS")
    print("=" * 60)
    print("Testing all components of the Load Combination System:")
    print("- LoadCombination class functionality")
    print("- CustomCombinationManager operations")
    print("- CombinationAnalysisManager analysis")
    print("- Integration and workflow tests")
    print("=" * 60)
    
    # Run all tests
    success = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
