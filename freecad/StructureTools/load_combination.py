import FreeCAD, App, FreeCADGui, Part, os
from PySide import QtWidgets, QtCore, QtGui

ICONPATH = os.path.join(os.path.dirname(__file__), "resources")

def show_error_message(msg):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(msg)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec_()

def show_info_message(msg):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setWindowTitle("Information")
    msg_box.setText(msg)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec_()

class LoadCombination:
    def __init__(self, obj, combination_data):
        obj.Proxy = self
        
        # Basic properties
        obj.addProperty("App::PropertyString", "CombinationName", "Basic", "Name of the load combination")
        obj.addProperty("App::PropertyEnumeration", "CombinationType", "Basic", "Type of combination standard")
        obj.CombinationType = ['Custom', 'ACI_318', 'AISC_360', 'Eurocode', 'IBC_2018']
        obj.CombinationType = combination_data.get('type', 'Custom')
        
        obj.addProperty("App::PropertyString", "Description", "Basic", "Description of the combination")
        obj.addProperty("App::PropertyFloat", "SafetyFactor", "Basic", "Overall safety factor").SafetyFactor = 1.0
        
        # Load case factors - สำหรับ Custom combinations
        obj.addProperty("App::PropertyFloat", "DeadLoadFactor", "Load Factors", "Dead Load Factor").DeadLoadFactor = 1.2
        obj.addProperty("App::PropertyFloat", "LiveLoadFactor", "Load Factors", "Live Load Factor").LiveLoadFactor = 1.6
        obj.addProperty("App::PropertyFloat", "WindLoadFactor", "Load Factors", "Wind Load Factor").WindLoadFactor = 1.6
        obj.addProperty("App::PropertyFloat", "SeismicLoadFactor", "Load Factors", "Seismic Load Factor").SeismicLoadFactor = 1.0
        obj.addProperty("App::PropertyFloat", "SnowLoadFactor", "Load Factors", "Snow Load Factor").SnowLoadFactor = 1.6
        obj.addProperty("App::PropertyFloat", "RoofLoadFactor", "Load Factors", "Roof Live Load Factor").RoofLoadFactor = 1.6
        
        # Boolean controls for including load types
        obj.addProperty("App::PropertyBool", "IncludeDeadLoad", "Include Loads", "Include Dead Load").IncludeDeadLoad = True
        obj.addProperty("App::PropertyBool", "IncludeLiveLoad", "Include Loads", "Include Live Load").IncludeLiveLoad = True
        obj.addProperty("App::PropertyBool", "IncludeWindLoad", "Include Loads", "Include Wind Load").IncludeWindLoad = False
        obj.addProperty("App::PropertyBool", "IncludeSeismicLoad", "Include Loads", "Include Seismic Load").IncludeSeismicLoad = False
        obj.addProperty("App::PropertyBool", "IncludeSnowLoad", "Include Loads", "Include Snow Load").IncludeSnowLoad = False
        obj.addProperty("App::PropertyBool", "IncludeRoofLoad", "Include Loads", "Include Roof Load").IncludeRoofLoad = False
        
        # Custom combination formula for user-defined combinations
        obj.addProperty("App::PropertyString", "CustomFormula", "Custom", "Custom combination formula")
        obj.addProperty("App::PropertyBool", "IsCustomFormula", "Custom", "Use custom formula instead of standard").IsCustomFormula = False
        
        # Analysis results
        obj.addProperty("App::PropertyString", "CombinationFormula", "Results", "Generated combination formula")
        obj.addProperty("App::PropertyBool", "IsActive", "Results", "Is this combination active for analysis").IsActive = True
        obj.addProperty("App::PropertyInteger", "CombinationIndex", "Results", "Index for standard combinations").CombinationIndex = 0
        
        # Integration with calc.py
        obj.addProperty("App::PropertyBool", "IncludeInAnalysis", "Analysis", "Include this combination in analysis").IncludeInAnalysis = True
        obj.addProperty("App::PropertyFloat", "MaxMoment", "Analysis Results", "Maximum moment from analysis").MaxMoment = 0.0
        obj.addProperty("App::PropertyFloat", "MaxShear", "Analysis Results", "Maximum shear from analysis").MaxShear = 0.0
        obj.addProperty("App::PropertyFloat", "MaxAxial", "Analysis Results", "Maximum axial force from analysis").MaxAxial = 0.0
        obj.addProperty("App::PropertyFloat", "MaxDeflection", "Analysis Results", "Maximum deflection from analysis").MaxDeflection = 0.0
        obj.addProperty("App::PropertyBool", "IsCritical", "Analysis Results", "Is this the critical combination").IsCritical = False
        obj.addProperty("App::PropertyString", "CriticalMember", "Analysis Results", "Member with critical result").CriticalMember = ""
        
        # Set initial values
        obj.CombinationName = combination_data.get('name', 'COMB1')
        obj.Description = combination_data.get('description', 'Load Combination')
        obj.CustomFormula = combination_data.get('custom_formula', '')
        obj.IsCustomFormula = combination_data.get('is_custom', False)
        obj.CombinationIndex = combination_data.get('index', 0)
        
        self.update_combination_formula(obj)
    
    def update_combination_formula(self, obj):
        """Update the combination formula based on current settings"""
        formula_parts = []
        
        if obj.IsCustomFormula:
            # Use custom formula
            obj.CombinationFormula = obj.CustomFormula if obj.CustomFormula else "Custom formula not defined"
            return
        
        if obj.CombinationType == 'Custom':
            # Custom combination based on factors
            if obj.IncludeDeadLoad:
                formula_parts.append(f"{obj.DeadLoadFactor:.1f}DL")
            if obj.IncludeLiveLoad:
                formula_parts.append(f"{obj.LiveLoadFactor:.1f}LL")
            if obj.IncludeWindLoad:
                formula_parts.append(f"{obj.WindLoadFactor:.1f}WL")
            if obj.IncludeSeismicLoad:
                formula_parts.append(f"{obj.SeismicLoadFactor:.1f}EQ")
            if obj.IncludeSnowLoad:
                formula_parts.append(f"{obj.SnowLoadFactor:.1f}SL")
            if obj.IncludeRoofLoad:
                formula_parts.append(f"{obj.RoofLoadFactor:.1f}RL")
        
        elif obj.CombinationType == 'ACI_318':
            formula_parts = self.get_aci_318_combinations(obj)
        
        elif obj.CombinationType == 'AISC_360':
            formula_parts = self.get_aisc_360_combinations(obj)
        
        elif obj.CombinationType == 'Eurocode':
            formula_parts = self.get_eurocode_combinations(obj)
        
        elif obj.CombinationType == 'IBC_2018':
            formula_parts = self.get_ibc_2018_combinations(obj)
        
        if formula_parts:
            obj.CombinationFormula = " + ".join(formula_parts)
        else:
            obj.CombinationFormula = "No loads selected"
    
    def get_aci_318_combinations(self, obj):
        """Generate ACI 318 standard combinations"""
        combinations = [
            ["1.4DL"],
            ["1.2DL", "1.6LL"],
            ["1.2DL", "1.6LL", "0.5SL"],
            ["1.2DL", "1.0LL", "1.6SL"],
            ["1.2DL", "1.0LL", "1.0WL"],
            ["1.2DL", "1.0LL", "1.0EQ"],
            ["0.9DL", "1.0WL"],
            ["0.9DL", "1.0EQ"]
        ]
        
        # Return the combination based on index for cycling through different combinations
        return combinations[obj.CombinationIndex % len(combinations)] if combinations else []
    
    def get_aisc_360_combinations(self, obj):
        """Generate AISC 360 standard combinations"""
        combinations = [
            ["1.4DL"],
            ["1.2DL", "1.6LL", "0.5SL"],
            ["1.2DL", "1.6SL", "1.0LL"],
            ["1.2DL", "1.0LL", "1.0WL", "0.5SL"],
            ["1.2DL", "1.0LL", "1.0EQ", "0.2SL"],
            ["0.9DL", "1.0WL"],
            ["0.9DL", "1.0EQ"]
        ]
        
        return combinations[obj.CombinationIndex % len(combinations)] if combinations else []
    
    def get_eurocode_combinations(self, obj):
        """Generate Eurocode standard combinations"""
        combinations = [
            ["1.35DL"],
            ["1.35DL", "1.5LL"],
            ["1.35DL", "1.5LL", "0.9WL"],
            ["1.0DL", "1.5WL"],
            ["1.0DL", "1.0EQ"]
        ]
        
        return combinations[obj.CombinationIndex % len(combinations)] if combinations else []
    
    def get_ibc_2018_combinations(self, obj):
        """Generate IBC 2018 standard combinations"""
        combinations = [
            ["1.4DL"],
            ["1.2DL", "1.6LL", "0.5SL"],
            ["1.2DL", "1.6SL", "1.0LL"],
            ["1.2DL", "1.0LL", "1.0WL"],
            ["1.2DL", "1.0LL", "1.0EQ"],
            ["0.9DL", "1.0WL"],
            ["0.9DL", "1.0EQ"]
        ]
        
        return combinations[obj.CombinationIndex % len(combinations)] if combinations else []
    
    def run_analysis(self, obj):
        """Run analysis for this load combination"""
        try:
            # Integration with calc.py using combination analysis manager
            from . import calc
            from .combination_analysis import combination_analysis_manager
            
            # Get all active load combinations in the document
            doc = FreeCAD.ActiveDocument
            if not doc:
                return False, "No active document"
            
            # Find calc object
            calc_objects = [o for o in doc.Objects if hasattr(o, 'Proxy') and 'Calc' in str(type(o.Proxy))]
            if not calc_objects:
                return False, "No calc object found. Please create a calculation first."
            
            calc_obj = calc_objects[0]
            
            # Use the analysis manager to run the combination analysis
            success, message = combination_analysis_manager.run_combination_analysis(obj, calc_obj)
            
            return success, message
                
        except Exception as e:
            return False, f"Analysis error: {str(e)}"
    
    def apply_combination_to_calc(self, obj, calc_obj):
        """Apply this combination's load factors to the calculation"""
        try:
            # Parse the combination formula and apply factors
            formula = obj.CombinationFormula
            
            # Reset all load factors first
            self.reset_load_factors(calc_obj)
            
            # Apply combination factors
            if "DL" in formula:
                factor = self.extract_factor(formula, "DL")
                self.apply_dead_load_factor(calc_obj, factor)
            
            if "LL" in formula:
                factor = self.extract_factor(formula, "LL")
                self.apply_live_load_factor(calc_obj, factor)
            
            if "WL" in formula:
                factor = self.extract_factor(formula, "WL")
                self.apply_wind_load_factor(calc_obj, factor)
            
            if "EQ" in formula:
                factor = self.extract_factor(formula, "EQ")
                self.apply_seismic_load_factor(calc_obj, factor)
            
            return True
            
        except Exception as e:
            print(f"Error applying combination: {str(e)}")
            return False
    
    def extract_factor(self, formula, load_type):
        """Extract load factor from formula"""
        import re
        pattern = rf'(\d*\.?\d+){load_type}'
        match = re.search(pattern, formula)
        return float(match.group(1)) if match else 1.0
    
    def reset_load_factors(self, calc_obj):
        """Reset all load factors to zero"""
        # This would integrate with the actual calc.py implementation
        pass
    
    def apply_dead_load_factor(self, calc_obj, factor):
        """Apply dead load factor"""
        # This would integrate with the actual calc.py implementation
        pass
    
    def apply_live_load_factor(self, calc_obj, factor):
        """Apply live load factor"""
        # This would integrate with the actual calc.py implementation
        pass
    
    def apply_wind_load_factor(self, calc_obj, factor):
        """Apply wind load factor"""
        # This would integrate with the actual calc.py implementation
        pass
    
    def apply_seismic_load_factor(self, calc_obj, factor):
        """Apply seismic load factor"""
        # This would integrate with the actual calc.py implementation
        pass
    
    def update_analysis_results(self, obj, calc_obj):
        """Update analysis results from calc object"""
        try:
            # This would extract results from the calc object
            # For now, we'll use placeholder values
            obj.MaxMoment = 1000.0  # Replace with actual calculation
            obj.MaxShear = 500.0    # Replace with actual calculation
            obj.MaxAxial = 2000.0   # Replace with actual calculation
            obj.MaxDeflection = 0.05 # Replace with actual calculation
            obj.CriticalMember = "B1" # Replace with actual critical member
            
        except Exception as e:
            print(f"Error updating results: {str(e)}")
    
    def export_combination(self, obj, filepath):
        """Export combination to file"""
        try:
            import json
            
            data = {
                'name': obj.CombinationName,
                'type': obj.CombinationType,
                'description': obj.Description,
                'formula': obj.CombinationFormula,
                'is_custom': obj.IsCustomFormula,
                'custom_formula': obj.CustomFormula,
                'include_in_analysis': obj.IncludeInAnalysis,
                'results': {
                    'max_moment': obj.MaxMoment,
                    'max_shear': obj.MaxShear,
                    'max_axial': obj.MaxAxial,
                    'max_deflection': obj.MaxDeflection,
                    'critical_member': obj.CriticalMember,
                    'is_critical': obj.IsCritical
                }
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True, f"Exported to {filepath}"
            
        except Exception as e:
            return False, f"Export failed: {str(e)}"
    
    def import_combination(self, filepath):
        """Import combination from file"""
        try:
            import json
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            return True, data
            
        except Exception as e:
            return False, f"Import failed: {str(e)}"
    
    def execute(self, obj):
        """Execute the load combination"""
        self.update_combination_formula(obj)
        
        # Create a simple visual representation
        # This could be enhanced to show load combination results
        box = Part.makeBox(100, 50, 20)
        box.translate(FreeCAD.Vector(-50, -25, 0))
        
        obj.Shape = box
        obj.ViewObject.DisplayMode = 'Shaded'
        obj.ViewObject.ShapeAppearance = (
            FreeCAD.Material(
                DiffuseColor=(0.2, 0.6, 1.0),
                AmbientColor=(0.1, 0.1, 0.1),
                SpecularColor=(0.3, 0.3, 0.3),
                EmissiveColor=(0.0, 0.0, 0.0),
                Shininess=(0.8),
                Transparency=(0.3)
            )
        )
        obj.Label = f'LoadCombo_{obj.CombinationName}'
    
    def onChanged(self, obj, prop):
        """Handle property changes"""
        if prop in ['CombinationType', 'DeadLoadFactor', 'LiveLoadFactor', 'WindLoadFactor', 
                   'SeismicLoadFactor', 'SnowLoadFactor', 'RoofLoadFactor',
                   'IncludeDeadLoad', 'IncludeLiveLoad', 'IncludeWindLoad', 
                   'IncludeSeismicLoad', 'IncludeSnowLoad', 'IncludeRoofLoad',
                   'CustomFormula', 'IsCustomFormula', 'CombinationIndex']:
            self.update_combination_formula(obj)


class ViewProviderLoadCombination:
    def __init__(self, obj):
        obj.Proxy = self
    
    def getIcon(self):
        return """
/* XPM */
static char * load_combination_xpm[] = {
"32 32 16 1",
" 	c None",
".	c #000080",
"+	c #0000FF",
"@	c #4040FF",
"#	c #8080FF",
"$	c #C0C0FF",
"%	c #FF8000",
"&	c #FFA040",
"*	c #FFC080",
"=	c #FFE0C0",
"-	c #00FF00",
";	c #40FF40",
">	c #80FF80",
",	c #C0FFC0",
"'	c #FFFFFF",
")	c #808080",
"                                ",
"  ......................        ",
"  .+++++++++++++++++++++.       ",
"  .+@@@@@@@@@@@@@@@@@@@@.       ",
"  .+@################@@@.       ",
"  .+@#$$$$$$$$$$$$$$#@@@.       ",
"  .+@#$''''''''''''$#@@@.       ",
"  .+@#$'%%%%%%%%%%'$#@@@.       ",
"  .+@#$'%&&&&&&&&%'$#@@@.       ",
"  .+@#$'%&********&%'$#@@@.     ",
"  .+@#$'%&*========*&%'$#@@@.   ",
"  .+@#$'%&*=------=*&%'$#@@@.   ",
"  .+@#$'%&*=-;;;;-=*&%'$#@@@.   ",
"  .+@#$'%&*=->>,>-=*&%'$#@@@.   ",
"  .+@#$'%&*=->,',>-=*&%'$#@@@.  ",
"  .+@#$'%&*=->','>-=*&%'$#@@@.  ",
"  .+@#$'%&*=->,',>-=*&%'$#@@@.  ",
"  .+@#$'%&*=->>,>-=*&%'$#@@@.   ",
"  .+@#$'%&*=-;;;;-=*&%'$#@@@.   ",
"  .+@#$'%&*=------=*&%'$#@@@.   ",
"  .+@#$'%&*========*&%'$#@@@.   ",
"  .+@#$'%&********&%'$#@@@.     ",
"  .+@#$'%&&&&&&&&%'$#@@@.       ",
"  .+@#$'%%%%%%%%%%'$#@@@.       ",
"  .+@#$''''''''''''$#@@@.       ",
"  .+@#$$$$$$$$$$$$$$#@@@.       ",
"  .+@################@@@.       ",
"  .+@@@@@@@@@@@@@@@@@@@@.       ",
"  .+++++++++++++++++++++.       ",
"  ......................        ",
"                                ",
"                                "};
        """


class LoadCombinationDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoadCombinationDialog, self).__init__(parent)
        self.setWindowTitle("Load Combination Generator")
        self.setMinimumSize(500, 600)
        self.setup_ui()
        self.combinations = []
    
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        # Header
        header_label = QtWidgets.QLabel("Load Combination Generator")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(header_label)
        
        # Standard selection
        standard_group = QtWidgets.QGroupBox("Standard")
        standard_layout = QtWidgets.QFormLayout(standard_group)
        
        self.standard_combo = QtWidgets.QComboBox()
        self.standard_combo.addItems(['Custom', 'ACI 318', 'AISC 360', 'Eurocode', 'IBC 2018'])
        self.standard_combo.currentTextChanged.connect(self.on_standard_changed)
        standard_layout.addRow("Code Standard:", self.standard_combo)
        
        layout.addWidget(standard_group)
        
        # Load types group
        loads_group = QtWidgets.QGroupBox("Available Load Types")
        loads_layout = QtWidgets.QGridLayout(loads_group)
        
        self.load_checkboxes = {}
        self.load_factors = {}
        
        load_types = [
            ('Dead Load (DL)', 'DL', 1.2),
            ('Live Load (LL)', 'LL', 1.6),
            ('Wind Load (WL)', 'WL', 1.6),
            ('Seismic Load (EQ)', 'EQ', 1.0),
            ('Snow Load (SL)', 'SL', 1.6),
            ('Roof Live Load (RL)', 'RL', 1.6)
        ]
        
        for i, (name, code, default_factor) in enumerate(load_types):
            checkbox = QtWidgets.QCheckBox(name)
            factor_spin = QtWidgets.QDoubleSpinBox()
            factor_spin.setRange(0.0, 10.0)
            factor_spin.setSingleStep(0.1)
            factor_spin.setValue(default_factor)
            factor_spin.setDecimals(1)
            
            loads_layout.addWidget(checkbox, i, 0)
            loads_layout.addWidget(QtWidgets.QLabel("Factor:"), i, 1)
            loads_layout.addWidget(factor_spin, i, 2)
            
            self.load_checkboxes[code] = checkbox
            self.load_factors[code] = factor_spin
        
        # Set default selections
        self.load_checkboxes['DL'].setChecked(True)
        self.load_checkboxes['LL'].setChecked(True)
        
        layout.addWidget(loads_group)
        
        # Combination preview
        preview_group = QtWidgets.QGroupBox("Combination Preview")
        preview_layout = QtWidgets.QVBoxLayout(preview_group)
        
        self.preview_text = QtWidgets.QTextEdit()
        self.preview_text.setMaximumHeight(100)
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        
        update_btn = QtWidgets.QPushButton("Update Preview")
        update_btn.clicked.connect(self.update_preview)
        preview_layout.addWidget(update_btn)
        
        layout.addWidget(preview_group)
        
        # Custom formula group
        custom_group = QtWidgets.QGroupBox("Custom Formula")
        custom_layout = QtWidgets.QVBoxLayout(custom_group)
        
        self.use_custom_checkbox = QtWidgets.QCheckBox("Use Custom Formula")
        self.use_custom_checkbox.toggled.connect(self.on_custom_toggle)
        custom_layout.addWidget(self.use_custom_checkbox)
        
        self.custom_formula_input = QtWidgets.QLineEdit()
        self.custom_formula_input.setPlaceholderText("e.g., 1.2DL + 1.6LL + 0.8WL")
        self.custom_formula_input.textChanged.connect(self.update_preview)
        self.custom_formula_input.setEnabled(False)
        custom_layout.addWidget(self.custom_formula_input)
        
        # Custom formula help
        help_label = QtWidgets.QLabel("Use: DL, LL, WL, EQ, SL, RL with factors (e.g., 1.2DL + 1.6LL)")
        help_label.setStyleSheet("color: gray; font-size: 10px;")
        custom_layout.addWidget(help_label)
        
        layout.addWidget(custom_group)
        
        # Generate buttons
        generate_group = QtWidgets.QGroupBox("Generate Combinations")
        generate_layout = QtWidgets.QVBoxLayout(generate_group)
        
        single_btn = QtWidgets.QPushButton("Generate Single Combination")
        single_btn.clicked.connect(self.generate_single_combination)
        generate_layout.addWidget(single_btn)
        
        all_btn = QtWidgets.QPushButton("Generate All Standard Combinations")
        all_btn.clicked.connect(self.generate_all_combinations)
        generate_layout.addWidget(all_btn)
        
        custom_btn = QtWidgets.QPushButton("Add Custom Combination to Standard")
        custom_btn.clicked.connect(self.add_custom_to_standard)
        generate_layout.addWidget(custom_btn)
        
        layout.addWidget(generate_group)
        
        # Analysis and Results group
        analysis_group = QtWidgets.QGroupBox("Analysis & Results")
        analysis_layout = QtWidgets.QVBoxLayout(analysis_group)
        
        # Analysis buttons
        analysis_btn_layout = QtWidgets.QHBoxLayout()
        
        run_analysis_btn = QtWidgets.QPushButton("Run Analysis for All")
        run_analysis_btn.clicked.connect(self.run_all_analysis)
        analysis_btn_layout.addWidget(run_analysis_btn)
        
        find_critical_btn = QtWidgets.QPushButton("Find Critical Combination")
        find_critical_btn.clicked.connect(self.find_critical_combination)
        analysis_btn_layout.addWidget(find_critical_btn)
        
        analysis_layout.addLayout(analysis_btn_layout)
        
        # Results display
        self.results_text = QtWidgets.QTextEdit()
        self.results_text.setMaximumHeight(150)
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Analysis results will appear here...")
        analysis_layout.addWidget(self.results_text)
        
        layout.addWidget(analysis_group)
        
        # Export/Import group
        export_group = QtWidgets.QGroupBox("Export/Import Combinations")
        export_layout = QtWidgets.QHBoxLayout(export_group)
        
        export_btn = QtWidgets.QPushButton("Export Combinations")
        export_btn.clicked.connect(self.export_combinations)
        export_layout.addWidget(export_btn)
        
        import_btn = QtWidgets.QPushButton("Import Combinations")
        import_btn.clicked.connect(self.import_combinations)
        export_layout.addWidget(import_btn)
        
        layout.addWidget(export_group)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        # Initial preview update
        self.update_preview()
    
    def on_custom_toggle(self, checked):
        """Handle custom formula checkbox toggle"""
        self.custom_formula_input.setEnabled(checked)
        
        # Disable/enable other controls
        for checkbox in self.load_checkboxes.values():
            checkbox.setEnabled(not checked)
        for factor in self.load_factors.values():
            factor.setEnabled(not checked)
        
        self.update_preview()
    
    def on_standard_changed(self, standard):
        """Update load factors based on selected standard"""
        if standard == 'ACI 318':
            self.load_factors['DL'].setValue(1.2)
            self.load_factors['LL'].setValue(1.6)
            self.load_factors['WL'].setValue(1.0)
            self.load_factors['EQ'].setValue(1.0)
        elif standard == 'AISC 360':
            self.load_factors['DL'].setValue(1.2)
            self.load_factors['LL'].setValue(1.6)
            self.load_factors['WL'].setValue(1.0)
            self.load_factors['EQ'].setValue(1.0)
        elif standard == 'Eurocode':
            self.load_factors['DL'].setValue(1.35)
            self.load_factors['LL'].setValue(1.5)
            self.load_factors['WL'].setValue(1.5)
            self.load_factors['EQ'].setValue(1.0)
        
        self.update_preview()
    
    def update_preview(self):
        """Update the combination preview"""
        if self.use_custom_checkbox.isChecked():
            # Show custom formula
            formula = self.custom_formula_input.text()
            self.preview_text.setText(formula if formula else "Enter custom formula")
        else:
            # Show standard formula
            formula_parts = []
            
            for code, checkbox in self.load_checkboxes.items():
                if checkbox.isChecked():
                    factor = self.load_factors[code].value()
                    formula_parts.append(f"{factor:.1f}{code}")
            
            if formula_parts:
                formula = " + ".join(formula_parts)
                self.preview_text.setText(formula)
            else:
                self.preview_text.setText("No loads selected")
    
    def generate_single_combination(self):
        """Generate a single combination based on current settings"""
        combination_data = {
            'name': f'COMB_{len(self.combinations) + 1}',
            'type': self.standard_combo.currentText().replace(' ', '_'),
            'description': f'{self.standard_combo.currentText()} Combination',
            'is_custom': self.use_custom_checkbox.isChecked(),
            'custom_formula': self.custom_formula_input.text() if self.use_custom_checkbox.isChecked() else ''
        }
        
        self.create_combination_object(combination_data)
    
    def add_custom_to_standard(self):
        """Add a custom combination to the selected standard"""
        if not self.custom_formula_input.text().strip():
            show_error_message("Please enter a custom formula first.")
            return
        
        combination_data = {
            'name': f'CUSTOM_{len(self.combinations) + 1}',
            'type': self.standard_combo.currentText().replace(' ', '_'),
            'description': f'Custom {self.standard_combo.currentText()} Combination',
            'is_custom': True,
            'custom_formula': self.custom_formula_input.text()
        }
        
        self.create_combination_object(combination_data)
        show_info_message(f"Added custom combination: {self.custom_formula_input.text()}")
    
    def generate_all_combinations(self):
        """Generate all standard combinations for selected code"""
        standard = self.standard_combo.currentText()
        
        if standard == 'ACI 318':
            combinations = self.get_aci_318_all_combinations()
        elif standard == 'AISC 360':
            combinations = self.get_aisc_360_all_combinations()
        elif standard == 'Eurocode':
            combinations = self.get_eurocode_all_combinations()
        elif standard == 'IBC 2018':
            combinations = self.get_ibc_2018_all_combinations()
        else:
            combinations = [{'name': 'CUSTOM', 'description': 'Custom Combination'}]
        
        for i, combo_data in enumerate(combinations):
            combo_data['type'] = standard.replace(' ', '_')
            combo_data['name'] = f'COMB_{len(self.combinations) + i + 1}'
            combo_data['index'] = i  # Set the combination index
            combo_data['is_custom'] = False  # Standard combinations
            combo_data['custom_formula'] = ''  # No custom formula for standard
            self.create_combination_object(combo_data)
    
    def get_aci_318_all_combinations(self):
        """Get all ACI 318 combinations"""
        return [
            {'description': '1.4DL'},
            {'description': '1.2DL + 1.6LL'},
            {'description': '1.2DL + 1.6LL + 0.5SL'},
            {'description': '1.2DL + 1.0LL + 1.6SL'},
            {'description': '1.2DL + 1.0LL + 1.0WL'},
            {'description': '1.2DL + 1.0LL + 1.0EQ'},
            {'description': '0.9DL + 1.0WL'},
            {'description': '0.9DL + 1.0EQ'}
        ]
    
    def get_aisc_360_all_combinations(self):
        """Get all AISC 360 combinations"""
        return [
            {'description': '1.4DL'},
            {'description': '1.2DL + 1.6LL + 0.5SL'},
            {'description': '1.2DL + 1.6SL + 1.0LL'},
            {'description': '1.2DL + 1.0LL + 1.0WL + 0.5SL'},
            {'description': '1.2DL + 1.0LL + 1.0EQ + 0.2SL'},
            {'description': '0.9DL + 1.0WL'},
            {'description': '0.9DL + 1.0EQ'}
        ]
    
    def get_eurocode_all_combinations(self):
        """Get all Eurocode combinations"""
        return [
            {'description': '1.35DL'},
            {'description': '1.35DL + 1.5LL'},
            {'description': '1.35DL + 1.5LL + 0.9WL'},
            {'description': '1.0DL + 1.5WL'},
            {'description': '1.0DL + 1.0EQ'}
        ]
    
    def get_ibc_2018_all_combinations(self):
        """Get all IBC 2018 combinations"""
        return [
            {'description': '1.4DL'},
            {'description': '1.2DL + 1.6LL + 0.5SL'},
            {'description': '1.2DL + 1.6SL + 1.0LL'},
            {'description': '1.2DL + 1.0LL + 1.0WL'},
            {'description': '1.2DL + 1.0LL + 1.0EQ'},
            {'description': '0.9DL + 1.0WL'},
            {'description': '0.9DL + 1.0EQ'}
        ]
    
    def create_combination_object(self, combination_data):
        """Create a load combination object in FreeCAD"""
        try:
            doc = FreeCAD.ActiveDocument
            if not doc:
                doc = FreeCAD.newDocument()
            
            obj = doc.addObject("Part::FeaturePython", f"LoadCombination_{combination_data['name']}")
            LoadCombination(obj, combination_data)
            ViewProviderLoadCombination(obj.ViewObject)
            
            self.combinations.append(obj)
            
            doc.recompute()
            show_info_message(f"Created load combination: {combination_data['name']}")
            
        except Exception as e:
            show_error_message(f"Error creating combination: {str(e)}")
    
    def run_all_analysis(self):
        """Run analysis for all combinations"""
        if not self.combinations:
            show_error_message("No combinations created yet.")
            return
        
        self.results_text.clear()
        self.results_text.append("Running analysis for all combinations...\n")
        
        for combo in self.combinations:
            if hasattr(combo, 'IncludeInAnalysis') and combo.IncludeInAnalysis:
                success, message = combo.Proxy.run_analysis(combo)
                status = "✓" if success else "✗"
                self.results_text.append(f"{status} {combo.CombinationName}: {message}")
        
        self.results_text.append("\nAnalysis completed.")
        show_info_message("Analysis completed for all combinations.")
    
    def find_critical_combination(self):
        """Find and highlight the critical combination"""
        if not self.combinations:
            show_error_message("No combinations created yet.")
            return
        
        critical_combo = None
        max_result = 0.0
        
        # Find combination with maximum moment (or other criteria)
        for combo in self.combinations:
            if hasattr(combo, 'MaxMoment') and combo.MaxMoment > max_result:
                max_result = combo.MaxMoment
                critical_combo = combo
        
        if critical_combo:
            # Mark as critical
            for combo in self.combinations:
                combo.IsCritical = False
            critical_combo.IsCritical = True
            
            self.results_text.clear()
            self.results_text.append("CRITICAL COMBINATION ANALYSIS\n")
            self.results_text.append("="*40)
            self.results_text.append(f"Critical Combination: {critical_combo.CombinationName}")
            self.results_text.append(f"Formula: {critical_combo.CombinationFormula}")
            self.results_text.append(f"Max Moment: {critical_combo.MaxMoment:.2f} kN⋅m")
            self.results_text.append(f"Max Shear: {critical_combo.MaxShear:.2f} kN")
            self.results_text.append(f"Max Axial: {critical_combo.MaxAxial:.2f} kN")
            self.results_text.append(f"Max Deflection: {critical_combo.MaxDeflection:.4f} m")
            self.results_text.append(f"Critical Member: {critical_combo.CriticalMember}")
            
            show_info_message(f"Critical combination: {critical_combo.CombinationName}")
        else:
            show_error_message("No analysis results found. Run analysis first.")
    
    def export_combinations(self):
        """Export all combinations to file"""
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Export Load Combinations", 
            "load_combinations.json", 
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                import json
                
                export_data = {
                    'standard': self.standard_combo.currentText(),
                    'export_date': str(QtCore.QDateTime.currentDateTime().toString()),
                    'combinations': []
                }
                
                for combo in self.combinations:
                    combo_data = {
                        'name': combo.CombinationName,
                        'type': combo.CombinationType,
                        'description': combo.Description,
                        'formula': combo.CombinationFormula,
                        'is_custom': combo.IsCustomFormula,
                        'custom_formula': combo.CustomFormula,
                        'include_in_analysis': combo.IncludeInAnalysis,
                        'results': {
                            'max_moment': combo.MaxMoment,
                            'max_shear': combo.MaxShear,
                            'max_axial': combo.MaxAxial,
                            'max_deflection': combo.MaxDeflection,
                            'critical_member': combo.CriticalMember,
                            'is_critical': combo.IsCritical
                        }
                    }
                    export_data['combinations'].append(combo_data)
                
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                show_info_message(f"Exported {len(self.combinations)} combinations to {filename}")
                
            except Exception as e:
                show_error_message(f"Export failed: {str(e)}")
    
    def import_combinations(self):
        """Import combinations from file"""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Import Load Combinations", 
            "", 
            "JSON Files (*.json);;All Files (*)"
        )
        
        if filename:
            try:
                import json
                
                with open(filename, 'r') as f:
                    import_data = json.load(f)
                
                # Set the standard from imported data
                if 'standard' in import_data:
                    index = self.standard_combo.findText(import_data['standard'])
                    if index >= 0:
                        self.standard_combo.setCurrentIndex(index)
                
                # Import combinations
                imported_count = 0
                for combo_data in import_data.get('combinations', []):
                    combination_data = {
                        'name': combo_data.get('name', f'IMPORTED_{imported_count + 1}'),
                        'type': combo_data.get('type', 'Custom'),
                        'description': combo_data.get('description', 'Imported combination'),
                        'is_custom': combo_data.get('is_custom', False),
                        'custom_formula': combo_data.get('custom_formula', '')
                    }
                    
                    self.create_combination_object(combination_data)
                    
                    # Import results if available
                    if 'results' in combo_data and self.combinations:
                        combo_obj = self.combinations[-1]
                        results = combo_data['results']
                        combo_obj.MaxMoment = results.get('max_moment', 0.0)
                        combo_obj.MaxShear = results.get('max_shear', 0.0)
                        combo_obj.MaxAxial = results.get('max_axial', 0.0)
                        combo_obj.MaxDeflection = results.get('max_deflection', 0.0)
                        combo_obj.CriticalMember = results.get('critical_member', '')
                        combo_obj.IsCritical = results.get('is_critical', False)
                    
                    imported_count += 1
                
                show_info_message(f"Imported {imported_count} combinations from {filename}")
                
            except Exception as e:
                show_error_message(f"Import failed: {str(e)}")


class CommandLoadCombination:
    """Load Combination Command"""
    
    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "icons/load_distributed.svg"),  # Using existing icon for now
            "Accel": "Shift+C",
            "MenuText": "Load Combination",
            "ToolTip": "Create and manage load combinations"
        }
    
    def Activated(self):
        try:
            dialog = LoadCombinationDialog()
            result = dialog.exec_()
            
            if result == QtWidgets.QDialog.Accepted:
                FreeCAD.ActiveDocument.recompute()
                
        except Exception as e:
            show_error_message(f"Error opening load combination dialog: {str(e)}")
    
    def IsActive(self):
        return True


# Register the command
FreeCADGui.addCommand("load_combination", CommandLoadCombination())
