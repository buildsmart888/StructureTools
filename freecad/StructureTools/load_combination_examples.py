# Load Combination System Usage Examples
# This file demonstrates how to use the Load Combination System in StructureTools

import FreeCAD
import os

def create_sample_structure():
    """Create a sample structure for testing load combinations"""
    
    # Create new document
    doc = FreeCAD.newDocument("LoadCombinationExample")
    
    print("=== Creating Sample Structure ===")
    
    # 1. Create materials
    from . import material
    steel = material.makeMaterial()
    steel.MaterialName = "Steel Grade 50"
    steel.YieldStrength = 345.0  # MPa
    steel.UltimateStrength = 450.0  # MPa
    steel.ElasticModulus = 200000.0  # MPa
    steel.Density = 7850.0  # kg/m³
    
    # 2. Create sections
    from . import section
    beam_section = section.makeSection()
    beam_section.SectionName = "W18x50"
    beam_section.SectionType = "Wide Flange"
    beam_section.Depth = 457.0  # mm
    beam_section.Width = 190.0  # mm
    beam_section.WebThickness = 9.0  # mm
    beam_section.FlangeThickness = 14.2  # mm
    
    # 3. Create members
    from . import member
    beam1 = member.makeMember()
    beam1.MemberName = "B1"
    beam1.StartPoint = FreeCAD.Vector(0, 0, 0)
    beam1.EndPoint = FreeCAD.Vector(6000, 0, 0)  # 6m beam
    beam1.Material = steel
    beam1.Section = beam_section
    
    beam2 = member.makeMember()
    beam2.MemberName = "B2"
    beam2.StartPoint = FreeCAD.Vector(6000, 0, 0)
    beam2.EndPoint = FreeCAD.Vector(12000, 0, 0)  # Another 6m beam
    beam2.Material = steel
    beam2.Section = beam_section
    
    # 4. Create supports
    from . import suport
    support1 = suport.makeSuport()
    support1.SupportName = "S1"
    support1.Position = FreeCAD.Vector(0, 0, 0)
    support1.FixityX = True
    support1.FixityY = True
    support1.FixityZ = True
    support1.FixityRotX = True
    support1.FixityRotY = False  # Allow rotation about Y-axis
    support1.FixityRotZ = True
    
    support2 = suport.makeSuport()
    support2.SupportName = "S2"
    support2.Position = FreeCAD.Vector(12000, 0, 0)
    support2.FixityX = False  # Allow horizontal movement
    support2.FixityY = True
    support2.FixityZ = True
    support2.FixityRotX = True
    support2.FixityRotY = False
    support2.FixityRotZ = True
    
    # 5. Create loads
    from . import load_nodal
    dead_load = load_nodal.makeNodalLoad()
    dead_load.LoadName = "DL1 - Dead Load"
    dead_load.Position = FreeCAD.Vector(6000, 0, 0)  # Mid-span
    dead_load.ForceZ = -50000.0  # 50 kN downward
    
    live_load = load_nodal.makeNodalLoad()
    live_load.LoadName = "LL1 - Live Load"
    live_load.Position = FreeCAD.Vector(6000, 0, 0)
    live_load.ForceZ = -75000.0  # 75 kN downward
    
    from . import load_distributed
    wind_load = load_distributed.makeDistributedLoad()
    wind_load.LoadName = "WL1 - Wind Load"
    wind_load.StartPoint = FreeCAD.Vector(0, 0, 0)
    wind_load.EndPoint = FreeCAD.Vector(12000, 0, 0)
    wind_load.LoadIntensity = 5000.0  # 5 kN/m horizontal
    wind_load.Direction = FreeCAD.Vector(1, 0, 0)  # X-direction
    
    print("Sample structure created successfully!")
    print("- Materials: 1 steel grade")
    print("- Sections: 1 wide flange")
    print("- Members: 2 beams (12m total)")
    print("- Supports: 2 supports")
    print("- Loads: 2 nodal loads + 1 distributed load")
    
    return doc

def demonstrate_standard_combinations():
    """Demonstrate creating standard load combinations"""
    
    print("\n=== Creating Standard Load Combinations ===")
    
    from .load_combination import makeLoadCombination
    
    # Create ACI 318 combinations
    print("Creating ACI 318 combinations...")
    
    # Service Load Combination
    service_combo = makeLoadCombination()
    service_combo.CombinationName = "ACI Service"
    service_combo.CombinationType = "ACI 318"
    service_combo.Description = "Service load combination per ACI 318"
    service_combo.CombinationFormula = "1.0DL + 1.0LL"
    service_combo.IncludeInAnalysis = True
    
    # Ultimate Load Combination 1
    ultimate_combo1 = makeLoadCombination()
    ultimate_combo1.CombinationName = "ACI Ultimate 1"
    ultimate_combo1.CombinationType = "ACI 318"
    ultimate_combo1.Description = "Ultimate strength design combination 1"
    ultimate_combo1.CombinationFormula = "1.2DL + 1.6LL"
    ultimate_combo1.IncludeInAnalysis = True
    
    # Ultimate Load Combination 2 (with wind)
    ultimate_combo2 = makeLoadCombination()
    ultimate_combo2.CombinationName = "ACI Ultimate 2"
    ultimate_combo2.CombinationType = "ACI 318"
    ultimate_combo2.Description = "Ultimate strength design with wind"
    ultimate_combo2.CombinationFormula = "1.2DL + 1.0LL + 1.0WL"
    ultimate_combo2.IncludeInAnalysis = True
    
    print(f"Created {service_combo.CombinationName}: {service_combo.CombinationFormula}")
    print(f"Created {ultimate_combo1.CombinationName}: {ultimate_combo1.CombinationFormula}")
    print(f"Created {ultimate_combo2.CombinationName}: {ultimate_combo2.CombinationFormula}")
    
    return [service_combo, ultimate_combo1, ultimate_combo2]

def demonstrate_custom_combinations():
    """Demonstrate creating custom load combinations"""
    
    print("\n=== Creating Custom Load Combinations ===")
    
    from .load_combination import makeLoadCombination
    
    # Custom seismic combination
    seismic_combo = makeLoadCombination()
    seismic_combo.CombinationName = "Custom Seismic"
    seismic_combo.CombinationType = "Custom"
    seismic_combo.Description = "Custom seismic load combination"
    seismic_combo.IsCustomFormula = True
    seismic_combo.CustomFormula = "1.0DL + 0.5LL + 1.0EQ"
    seismic_combo.IncludeInAnalysis = True
    
    # Custom construction load
    construction_combo = makeLoadCombination()
    construction_combo.CombinationName = "Construction Load"
    construction_combo.CombinationType = "Custom"
    construction_combo.Description = "Special construction stage loading"
    construction_combo.IsCustomFormula = True
    construction_combo.CustomFormula = "1.0DL + 0.25LL + 1.2CL"  # CL = Construction Load
    construction_combo.IncludeInAnalysis = False  # Not included in regular analysis
    
    print(f"Created {seismic_combo.CombinationName}: {seismic_combo.CustomFormula}")
    print(f"Created {construction_combo.CombinationName}: {construction_combo.CustomFormula}")
    
    return [seismic_combo, construction_combo]

def demonstrate_analysis_integration():
    """Demonstrate analysis integration with load combinations"""
    
    print("\n=== Running Analysis with Load Combinations ===")
    
    try:
        # Get all load combinations in the document
        doc = FreeCAD.ActiveDocument
        combinations = [obj for obj in doc.Objects if hasattr(obj, 'Proxy') and 'LoadCombination' in str(type(obj.Proxy))]
        
        if not combinations:
            print("No load combinations found. Please create some first.")
            return
        
        # Import the analysis manager
        from .combination_analysis import combination_analysis_manager
        
        # Create calc object
        from . import calc
        calc_obj = calc.makeCalc()
        
        # Run analysis for each combination
        results = []
        for combo in combinations:
            print(f"\nAnalyzing combination: {combo.CombinationName}")
            print(f"Formula: {combo.CombinationFormula if not combo.IsCustomFormula else combo.CustomFormula}")
            
            success, message = combination_analysis_manager.run_combination_analysis(combo, calc_obj)
            
            if success:
                print(f"✓ Analysis completed: {message}")
                print(f"  Max Moment: {combo.MaxMoment:.2f} kN⋅m")
                print(f"  Max Shear: {combo.MaxShear:.2f} kN")
                print(f"  Max Deflection: {combo.MaxDeflection:.4f} m")
                print(f"  Critical Member: {combo.CriticalMember}")
                results.append(combo)
            else:
                print(f"✗ Analysis failed: {message}")
        
        # Find critical combinations
        print("\n=== Critical Combination Analysis ===")
        
        if results:
            critical_moment, msg = combination_analysis_manager.find_critical_combination(results, 'moment')
            if critical_moment:
                print(f"Critical for Moment: {critical_moment.CombinationName} ({critical_moment.MaxMoment:.2f} kN⋅m)")
            
            critical_shear, msg = combination_analysis_manager.find_critical_combination(results, 'shear')
            if critical_shear:
                print(f"Critical for Shear: {critical_shear.CombinationName} ({critical_shear.MaxShear:.2f} kN)")
            
            critical_deflection, msg = combination_analysis_manager.find_critical_combination(results, 'deflection')
            if critical_deflection:
                print(f"Critical for Deflection: {critical_deflection.CombinationName} ({critical_deflection.MaxDeflection:.4f} m)")
        
        return results
        
    except Exception as e:
        print(f"Analysis integration failed: {str(e)}")
        return []

def demonstrate_export_import():
    """Demonstrate export/import functionality"""
    
    print("\n=== Export/Import Demonstration ===")
    
    try:
        # Get all load combinations
        doc = FreeCAD.ActiveDocument
        combinations = [obj for obj in doc.Objects if hasattr(obj, 'Proxy') and 'LoadCombination' in str(type(obj.Proxy))]
        
        if not combinations:
            print("No combinations to export")
            return
        
        # Export combinations
        export_path = os.path.join(FreeCAD.getUserAppDataDir(), "load_combinations_export.json")
        
        from .combination_analysis import combination_analysis_manager
        success, message = combination_analysis_manager.export_analysis_report(combinations, export_path)
        
        if success:
            print(f"✓ Export successful: {message}")
            print(f"File location: {export_path}")
            
            # Show file contents (first few lines)
            with open(export_path, 'r') as f:
                lines = f.readlines()[:10]
                print("\nExported data preview:")
                for line in lines:
                    print(f"  {line.strip()}")
                if len(lines) == 10:
                    print("  ...")
        else:
            print(f"✗ Export failed: {message}")
            
    except Exception as e:
        print(f"Export/Import demonstration failed: {str(e)}")

def run_complete_example():
    """Run complete load combination system example"""
    
    print("=" * 60)
    print("LOAD COMBINATION SYSTEM - COMPLETE EXAMPLE")
    print("=" * 60)
    
    try:
        # Step 1: Create sample structure
        doc = create_sample_structure()
        
        # Step 2: Create standard combinations
        standard_combos = demonstrate_standard_combinations()
        
        # Step 3: Create custom combinations
        custom_combos = demonstrate_custom_combinations()
        
        # Step 4: Run analysis integration
        analyzed_combos = demonstrate_analysis_integration()
        
        # Step 5: Export results
        demonstrate_export_import()
        
        print("\n" + "=" * 60)
        print("EXAMPLE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Document: {doc.Name}")
        print(f"Standard Combinations: {len(standard_combos)}")
        print(f"Custom Combinations: {len(custom_combos)}")
        print(f"Analyzed Combinations: {len(analyzed_combos)}")
        print("\nNext steps:")
        print("1. Open the Load Combination dialog to view/edit combinations")
        print("2. Run individual analyses using the Analysis buttons")
        print("3. Export combinations for use in other projects")
        print("4. Create additional custom combinations as needed")
        
    except Exception as e:
        print(f"\nExample failed: {str(e)}")
        import traceback
        traceback.print_exc()

# Usage instructions
def show_usage_instructions():
    """Show instructions for using the Load Combination System"""
    
    instructions = """
    LOAD COMBINATION SYSTEM - USAGE INSTRUCTIONS
    ============================================
    
    1. CREATING LOAD COMBINATIONS:
       - Use the Load Combination dialog from the StructureTools toolbar
       - Select from standard combinations (ACI 318, AISC 360, Eurocode, IBC)
       - Create custom combinations with your own formulas
    
    2. STANDARD COMBINATIONS:
       - Automatically generated based on selected design code
       - Include service and ultimate load combinations
       - Cover dead load, live load, wind load, seismic load combinations
    
    3. CUSTOM COMBINATIONS:
       - Define your own load combination formulas
       - Use format: "1.2DL + 1.6LL + 0.5WL"
       - Include special load cases like construction loads
    
    4. ANALYSIS INTEGRATION:
       - Run analysis for individual combinations
       - Compare results across different combinations
       - Identify critical combinations for design
    
    5. RESULTS ANALYSIS:
       - View maximum moments, shears, and deflections
       - Identify critical members for each combination
       - Find governing combinations for different criteria
    
    6. EXPORT/IMPORT:
       - Save combination sets to JSON files
       - Import combinations from other projects
       - Generate comprehensive analysis reports
    
    7. WORKFLOW EXAMPLE:
       a) Create your structural model (members, loads, supports)
       b) Open Load Combination dialog
       c) Generate standard combinations for your design code
       d) Add any custom combinations needed
       e) Run analysis for critical combinations
       f) Review results and identify governing cases
       g) Export combination set for documentation
    
    For more information, see the README-NEWFEATURES.md file.
    """
    
    print(instructions)

if __name__ == "__main__":
    # Show usage instructions
    show_usage_instructions()
    
    # Ask user if they want to run the complete example
    print("\nWould you like to run the complete example? (This will create a new document)")
    print("Type 'yes' to continue or 'no' to exit.")
    
    # Note: In FreeCAD, you would typically run this interactively
    # For now, we'll show how to use it:
    print("\nTo run the example in FreeCAD:")
    print("1. Open FreeCAD")
    print("2. Load the StructureTools workbench")
    print("3. In the Python console, type:")
    print("   from freecad.StructureTools.load_combination_examples import run_complete_example")
    print("   run_complete_example()")
