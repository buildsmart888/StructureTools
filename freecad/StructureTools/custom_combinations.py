# Custom Load Combinations Manager
# This file provides utilities for managing custom load combinations

class CustomCombinationManager:
    """Manager for storing and retrieving custom load combinations for each standard"""
    
    def __init__(self):
        # Storage for custom combinations by standard
        self.custom_combinations = {
            'ACI_318': [],
            'AISC_360': [],
            'Eurocode': [],
            'IBC_2018': [],
            'Custom': []
        }
        # Add combinations property for backward compatibility
        self.combinations = {}
    
    def add_combination(self, name, formula, description=""):
        """Add a custom combination (for test compatibility)"""
        # Handle None and empty inputs
        if not name or not name.strip():
            return False, "Combination name cannot be empty"
        
        if not formula:
            return False, "Formula cannot be empty"
            
        # Check for duplicate names  
        if name in self.combinations:
            return False, f"Combination '{name}' already exists"
        
        is_valid, validation_message = self.validate_formula(formula)
        if not is_valid:
            return False, validation_message
        
        self.combinations[name] = {
            'formula': formula,
            'description': description,
            'is_custom': True
        }
        return True, f"Added combination '{name}'"
    
    def get_combinations(self):
        """Get all combinations (for test compatibility) - return as list"""
        return [
            {
                'name': name,
                'formula': data['formula'],
                'description': data.get('description', ''),
                'is_custom': data.get('is_custom', True)
            }
            for name, data in self.combinations.items()
        ]
    
    def validate_formula(self, formula):
        """Validate a load combination formula"""
        if not formula or not formula.strip():
            return False, "Formula cannot be empty"
        
        formula = formula.strip()
        
        # Check for incomplete formulas
        if formula.endswith(('+', '-', '*')):
            return False, "Formula is incomplete"
        
        # Check for starting with operators (but allow explicit positive sign)
        if formula.startswith('+') and not formula[1:2].isdigit():
            return False, "Formula cannot start with operator"
        if formula.startswith('-') and not formula[1:2].isdigit():
            return False, "Formula cannot start with operator"
        
        # Check for invalid load types and other issues
        import re
        
        # Valid load types - include more comprehensive list
        valid_loads = ['DL', 'LL', 'WL', 'EQ', 'SL', 'RL', 'TL', 'CL']
        
        # More flexible pattern to handle spaces and variations
        # Allow factors from 0 to 1000 for more flexibility
        pattern = r'([+-]?\d+\.?\d*)\s*\*?\s*([A-Z]+)'
        matches = re.findall(pattern, formula)
        
        if not matches:
            return False, "No valid load factors found"
        
        # Check for missing operators between terms - improved detection
        if len(matches) > 1:
            # Create a test string by replacing all valid terms
            test_formula = formula
            for factor_str, load_type in matches:
                # Handle spaced factors more precisely
                term_pattern = rf'{re.escape(factor_str)}\s*\*?\s*{re.escape(load_type)}'
                test_formula = re.sub(term_pattern, 'X', test_formula, 1)
            
            # Should now be like "X + X - X" - check for missing operators
            test_formula = test_formula.strip()
            # Remove spaces around X terms
            test_formula = re.sub(r'\s*X\s*', 'X', test_formula)
            
            # If we have multiple X's without operators between them, it's invalid
            # But allow cases like "X+X" (no spaces around operators)
            if re.search(r'X[A-Z]|[A-Z]X', test_formula):  # Letters directly adjacent to X
                return False, "Missing operator between load terms"
            if re.search(r'XX+', test_formula):  # Multiple X without operators
                return False, "Missing operator between load terms"
        
        # Check for consecutive operators (but be more lenient)
        if re.search(r'[+-]{3,}', formula):  # Only flag 3+ consecutive operators
            return False, "Too many consecutive operators"
        
        # Check each term
        for factor_str, load_type in matches:
            try:
                factor = float(factor_str)
                
                # More flexible engineering limits
                if factor < 0:
                    return False, f"Negative factor {factor} not allowed for {load_type}"
                
                # Allow larger factors (up to 1000) for special cases
                if factor > 1000.0:
                    return False, f"Factor {factor} too large for {load_type} (max 1000.0)"
                
                # Allow zero factors in some cases (like preliminary analysis)
                # Only warn for zero, don't fail
                
                # Check for invalid load types
                if load_type not in valid_loads:
                    return False, f"Invalid load type: {load_type}"
                    
            except ValueError:
                return False, f"Invalid factor '{factor_str}' for load type '{load_type}'"
        
        # Allow tabs and newlines but clean them in processing
        cleaned_formula = formula.replace('\t', ' ').replace('\n', ' ')
        
        # More comprehensive but lenient syntax check
        test_formula = cleaned_formula
        for factor_str, load_type in matches:
            # Handle spaced factors
            term_pattern = rf'{re.escape(factor_str)}\s*\*?\s*{re.escape(load_type)}'
            test_formula = re.sub(term_pattern, 'X', test_formula)
        
        # Should now be like "X + X - X" - only X, +, -, and spaces
        test_formula = test_formula.replace('X', '').replace(' ', '')
        if test_formula and not re.match(r'^[+-]*$', test_formula):
            return False, "Invalid formula syntax - missing operators or invalid characters"
        
        return True, "Formula is valid"
    
    def export_combinations(self, filename):
        """Export combinations to file"""
        try:
            import json
            export_data = {
                'custom_combinations': self.custom_combinations,
                'combinations': self.combinations
            }
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            return True, f"Exported to {filename}"
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def import_combinations(self, filename):
        """Import combinations from file"""
        try:
            import json
            import os
            
            # Check if file exists and is readable
            if not os.path.exists(filename):
                return False, f"File {filename} does not exist"
            
            with open(filename, 'r') as f:
                content = f.read().strip()
                
            # Check for empty file
            if not content:
                return False, "File is empty"
            
            # Try to parse JSON
            try:
                data = json.loads(content)
            except json.JSONDecodeError as e:
                return False, f"Invalid JSON format: {str(e)}"
            
            # Validate data structure
            if not isinstance(data, dict):
                return False, "Invalid file format: root must be object"
            
            # Import data safely
            imported_count = 0
            if 'custom_combinations' in data and isinstance(data['custom_combinations'], dict):
                self.custom_combinations.update(data['custom_combinations'])
                imported_count += len(data['custom_combinations'])
                
            if 'combinations' in data and isinstance(data['combinations'], dict):
                self.combinations.update(data['combinations'])
                imported_count += len(data['combinations'])
            
            if imported_count == 0:
                return False, "No valid combinations found in file"
            
            return True, f"Imported {imported_count} items from {filename}"
            
        except Exception as e:
            return False, f"Import failed: {str(e)}"
    
    def add_custom_combination(self, standard, formula, description=""):
        """Add a custom combination to a specific standard"""
        if standard not in self.custom_combinations:
            self.custom_combinations[standard] = []
        
        custom_combo = {
            'formula': formula,
            'description': description,
            'is_custom': True
        }
        
        self.custom_combinations[standard].append(custom_combo)
        return len(self.custom_combinations[standard]) - 1  # Return index
    
    def get_custom_combinations(self, standard):
        """Get all custom combinations for a standard"""
        return self.custom_combinations.get(standard, [])
    
    def remove_custom_combination(self, standard, index):
        """Remove a custom combination by index"""
        if standard in self.custom_combinations and 0 <= index < len(self.custom_combinations[standard]):
            del self.custom_combinations[standard][index]
            return True
        return False
    
    def get_all_combinations(self, standard):
        """Get both standard and custom combinations"""
        standard_combinations = self.get_standard_combinations(standard)
        custom_combinations = self.get_custom_combinations(standard)
        
        all_combinations = []
        
        # Add standard combinations
        for i, combo in enumerate(standard_combinations):
            all_combinations.append({
                'formula': combo,
                'description': f'{standard} Standard {i+1}',
                'is_custom': False,
                'index': i
            })
        
        # Add custom combinations
        for i, combo in enumerate(custom_combinations):
            all_combinations.append({
                'formula': combo['formula'],
                'description': combo['description'],
                'is_custom': True,
                'index': len(standard_combinations) + i
            })
        
        return all_combinations
    
    def get_standard_combinations(self, standard):
        """Get standard combinations for each code"""
        combinations = {
            'ACI_318': [
                "1.4DL",
                "1.2DL + 1.6LL",
                "1.2DL + 1.6LL + 0.5SL",
                "1.2DL + 1.0LL + 1.6SL",
                "1.2DL + 1.0LL + 1.0WL",
                "1.2DL + 1.0LL + 1.0EQ",
                "0.9DL + 1.0WL",
                "0.9DL + 1.0EQ"
            ],
            'AISC_360': [
                "1.4DL",
                "1.2DL + 1.6LL + 0.5SL",
                "1.2DL + 1.6SL + 1.0LL",
                "1.2DL + 1.0LL + 1.0WL + 0.5SL",
                "1.2DL + 1.0LL + 1.0EQ + 0.2SL",
                "0.9DL + 1.0WL",
                "0.9DL + 1.0EQ"
            ],
            'Eurocode': [
                "1.35DL",
                "1.35DL + 1.5LL",
                "1.35DL + 1.5LL + 0.9WL",
                "1.0DL + 1.5WL",
                "1.0DL + 1.0EQ"
            ],
            'IBC_2018': [
                "1.4DL",
                "1.2DL + 1.6LL + 0.5SL",
                "1.2DL + 1.6SL + 1.0LL",
                "1.2DL + 1.0LL + 1.0WL",
                "1.2DL + 1.0LL + 1.0EQ",
                "0.9DL + 1.0WL",
                "0.9DL + 1.0EQ"
            ]
        }
        
        return combinations.get(standard, [])


# Global instance for use throughout the application
custom_combination_manager = CustomCombinationManager()
