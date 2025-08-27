# Implementation Plan: Single Requirement Test with G-Eval

## Overview

This plan outlines the implementation approach for testing a single requirement using G-Eval validation with codebase comparison capabilities.

## Implementation Architecture

### **Recommended Approach: Modular Python Files**

```
validator-python/src/
├── requirement_extractor.py      # Extract single requirement from JSON
├── analyzable_object_creator.py  # Create analyzable objects
├── g_eval_validator.py          # G-Eval validation engine
├── codebase_analyzer.py         # Codebase analysis and comparison
├── report_generator.py          # Generate validation reports
└── main_validation_pipeline.py  # Orchestrate the entire process
```

## Step-by-Step Implementation

### **Step 1: Create Single Requirement JSON**

**File:** `requirement_extractor.py`

```python
def create_single_requirement_json(requirement_index: int = 0):
    """
    Extract one requirement from the original JSON and create a focused test file.
    """
    # Load original CD-Requirements.json
    # Extract specific requirement by index
    # Create focused JSON with just that requirement
    # Save as single_requirement_test.json
```

**Benefits:**

- **Focused Testing:** Work with one requirement at a time
- **Faster Processing:** Reduced complexity for initial testing
- **Easy Debugging:** Isolated issues and validation results
- **Incremental Development:** Build and test each component separately

### **Step 2: Create Analyzable Objects**

**File:** `analyzable_object_creator.py`

```python
def create_analyzable_objects(requirement_data):
    """
    Extract and categorize analyzable objects from the requirement.
    """
    analyzable_objects = {
        "business_rules": extract_business_rules(requirement_data),
        "technical_requirements": parse_technical_requirements(requirement_data),
        "architecture_components": extract_architecture_components(requirement_data),
        "integration_points": identify_integration_points(requirement_data),
        "data_entities": extract_data_entities(requirement_data),
        "validation_rules": extract_validation_rules(requirement_data)
    }
    return analyzable_objects
```

### **Step 3: G-Eval Validation Engine**

**File:** `g_eval_validator.py`

```python
class GEvalValidator:
    def __init__(self, llm_config):
        self.llm_config = llm_config
        self.evaluation_criteria = self._load_evaluation_criteria()

    def validate_analyzable_object(self, object_type, object_data):
        """
        Validate a single analyzable object using G-Eval framework.
        """
        criteria = self.evaluation_criteria[object_type]
        prompt = self._create_validation_prompt(object_data, criteria)
        result = self._call_llm_for_validation(prompt)
        return self._parse_validation_result(result)

    def _create_validation_prompt(self, object_data, criteria):
        """
        Create chain-of-thoughts prompt for validation.
        """
        return f"""
        Evaluate the following requirement against the specified criteria:

        REQUIREMENT: {object_data}

        EVALUATION CRITERIA: {criteria}

        Please provide your evaluation with reasoning:
        1. Analyze the requirement against each criterion
        2. Provide specific feedback for each criterion
        3. Give an overall assessment score (0-100)
        4. Suggest improvements if needed

        Use chain-of-thoughts reasoning to explain your evaluation.
        """
```

### **Step 4: Codebase Analysis and Comparison**

**File:** `codebase_analyzer.py`

```python
class CodebaseAnalyzer:
    def __init__(self, codebase_path):
        self.codebase_path = codebase_path
        self.codebase_context = self._analyze_codebase()

    def _analyze_codebase(self):
        """
        Analyze the CardDemo codebase to extract relevant context.
        """
        return {
            "database_schemas": self._extract_database_schemas(),
            "program_names": self._extract_program_names(),
            "integration_patterns": self._extract_integration_patterns(),
            "data_structures": self._extract_data_structures(),
            "business_logic": self._extract_business_logic()
        }

    def compare_requirement_to_codebase(self, requirement_data):
        """
        Compare requirement against codebase to identify gaps and matches.
        """
        comparison_results = {
            "implemented_features": self._find_implemented_features(requirement_data),
            "missing_implementations": self._find_missing_implementations(requirement_data),
            "codebase_evidence": self._find_codebase_evidence(requirement_data),
            "gap_analysis": self._perform_gap_analysis(requirement_data)
        }
        return comparison_results
```

### **Step 5: Report Generation**

**File:** `report_generator.py`

```python
def generate_validation_report(validation_results, codebase_comparison, requirement_data):
    """
    Generate comprehensive validation report.
    """
    report = {
        "requirement_summary": requirement_data,
        "g_eval_validation": validation_results,
        "codebase_comparison": codebase_comparison,
        "overall_assessment": calculate_overall_assessment(validation_results, codebase_comparison),
        "recommendations": generate_recommendations(validation_results, codebase_comparison)
    }
    return report
```

## Main Pipeline Orchestration

**File:** `main_validation_pipeline.py`

```python
def main():
    """
    Main validation pipeline for single requirement test.
    """
    # Step 1: Extract single requirement
    requirement_data = extract_single_requirement(requirement_index=0)

    # Step 2: Create analyzable objects
    analyzable_objects = create_analyzable_objects(requirement_data)

    # Step 3: Initialize G-Eval validator
    g_eval_validator = GEvalValidator(llm_config)

    # Step 4: Initialize codebase analyzer
    codebase_analyzer = CodebaseAnalyzer(codebase_path)

    # Step 5: Validate each analyzable object
    validation_results = {}
    for object_type, object_data in analyzable_objects.items():
        validation_results[object_type] = g_eval_validator.validate_analyzable_object(
            object_type, object_data
        )

    # Step 6: Compare against codebase
    codebase_comparison = codebase_analyzer.compare_requirement_to_codebase(requirement_data)

    # Step 7: Generate comprehensive report
    final_report = generate_validation_report(
        validation_results, codebase_comparison, requirement_data
    )

    # Step 8: Save results
    save_validation_results(final_report)

    return final_report
```

## Codebase Comparison Strategy

### **How to Compare Requirements Against Codebase:**

#### **1. Database Schema Analysis:**

```python
def _extract_database_schemas(self):
    """
    Extract database schemas from DDL files and IMS DBD files.
    """
    schemas = {
        "db2_tables": self._parse_ddl_files(),
        "ims_segments": self._parse_dbd_files(),
        "data_relationships": self._analyze_data_relationships()
    }
    return schemas
```

#### **2. Program Name Extraction:**

```python
def _extract_program_names(self):
    """
    Extract program names from COBOL files, JCL files, and CSD files.
    """
    return {
        "cobol_programs": self._find_cobol_programs(),
        "jcl_jobs": self._find_jcl_jobs(),
        "cics_transactions": self._find_cics_transactions()
    }
```

#### **3. Integration Pattern Analysis:**

```python
def _extract_integration_patterns(self):
    """
    Analyze integration patterns from MQ, CICS, and database interactions.
    """
    return {
        "mq_patterns": self._analyze_mq_usage(),
        "cics_patterns": self._analyze_cics_usage(),
        "database_patterns": self._analyze_database_usage()
    }
```

#### **4. Gap Analysis:**

```python
def _perform_gap_analysis(self, requirement_data):
    """
    Identify what's missing between requirement and codebase.
    """
    gaps = {
        "missing_database_objects": self._find_missing_database_objects(requirement_data),
        "missing_programs": self._find_missing_programs(requirement_data),
        "missing_integration_points": self._find_missing_integration_points(requirement_data),
        "missing_business_logic": self._find_missing_business_logic(requirement_data)
    }
    return gaps
```

## File Structure for Implementation

```
validator-python/src/
├── implementation_plan.md                    # This document
├── requirement_extractor.py                  # Step 1: Extract single requirement
├── analyzable_object_creator.py              # Step 2: Create analyzable objects
├── g_eval_validator.py                      # Step 3: G-Eval validation engine
├── codebase_analyzer.py                     # Step 4: Codebase analysis
├── report_generator.py                      # Step 5: Report generation
├── main_validation_pipeline.py              # Main orchestration
├── config/
│   ├── evaluation_criteria.json             # G-Eval criteria definitions
│   ├── llm_config.json                      # LLM configuration
│   └── codebase_paths.json                  # Codebase file paths
├── data/
│   ├── single_requirement_test.json         # Single requirement for testing
│   └── validation_results/                  # Validation output
└── reports/
    └── single_requirement_validation_report.md
```

## Implementation Order

### **Phase 1: Core Infrastructure (Week 1)**

1. Create `requirement_extractor.py` - Extract single requirement
2. Create `analyzable_object_creator.py` - Create analyzable objects
3. Create configuration files for evaluation criteria

### **Phase 2: G-Eval Integration (Week 2)**

1. Create `g_eval_validator.py` - G-Eval validation engine
2. Test with single analyzable object
3. Validate results and refine prompts

### **Phase 3: Codebase Analysis (Week 3)**

1. Create `codebase_analyzer.py` - Codebase analysis
2. Implement database schema extraction
3. Implement program name extraction
4. Test codebase comparison

### **Phase 4: Integration and Reporting (Week 4)**

1. Create `report_generator.py` - Report generation
2. Create `main_validation_pipeline.py` - Main orchestration
3. End-to-end testing with single requirement
4. Generate comprehensive validation report

## Success Criteria

### **Technical Success:**

- ✅ Single requirement successfully extracted and processed
- ✅ Analyzable objects created and categorized
- ✅ G-Eval validation working with chain-of-thoughts reasoning
- ✅ Codebase comparison identifying gaps and matches
- ✅ Comprehensive report generated

### **Validation Success:**

- ✅ G-Eval provides meaningful evaluation scores
- ✅ Codebase comparison identifies missing implementations
- ✅ Report provides actionable recommendations
- ✅ Process is repeatable and extensible

## Next Steps

1. **Start with Phase 1:** Create the requirement extractor and analyzable object creator
2. **Test incrementally:** Validate each component before moving to the next
3. **Document results:** Keep detailed notes on what works and what needs refinement
4. **Plan for scaling:** Once single requirement works, plan for multiple requirements

---

_Implementation Plan created: 2025-08-26_  
_Purpose: Detailed implementation approach for single requirement test with G-Eval validation_
