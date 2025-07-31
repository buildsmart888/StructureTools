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
    
    def validate_formula(self, formula):
        """Validate a custom combination formula"""
        # Basic validation - check for valid load types
        valid_loads = ['DL', 'LL', 'WL', 'EQ', 'SL', 'RL']
        
        # Remove spaces and split by + and -
        formula_clean = formula.replace(' ', '').replace('-', '+-')
        terms = [term.strip() for term in formula_clean.split('+') if term.strip()]
        
        for term in terms:
            # Extract load type from term (remove factor)
            load_type = ''.join([c for c in term if c.isalpha()])
            if load_type not in valid_loads:
                return False, f"Invalid load type: {load_type}"
        
        return True, "Formula is valid"
    
    def export_combinations(self, standard, filename):
        """Export combinations to a file"""
        combinations = self.get_all_combinations(standard)
        
        try:
            with open(filename, 'w') as f:
                f.write(f"# {standard} Load Combinations\n")
                f.write("# Format: Formula | Description | Type\n\n")
                
                for combo in combinations:
                    combo_type = "Custom" if combo['is_custom'] else "Standard"
                    f.write(f"{combo['formula']} | {combo['description']} | {combo_type}\n")
            
            return True, f"Exported to {filename}"
        
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def import_combinations(self, standard, filename):
        """Import combinations from a file"""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            imported_count = 0
            for line in lines:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                
                parts = line.split('|')
                if len(parts) >= 3:
                    formula = parts[0].strip()
                    description = parts[1].strip()
                    combo_type = parts[2].strip()
                    
                    if combo_type == "Custom":
                        is_valid, msg = self.validate_formula(formula)
                        if is_valid:
                            self.add_custom_combination(standard, formula, description)
                            imported_count += 1
            
            return True, f"Imported {imported_count} custom combinations"
        
        except Exception as e:
            return False, f"Import failed: {str(e)}"


# Global instance for use throughout the application
custom_combination_manager = CustomCombinationManager()
