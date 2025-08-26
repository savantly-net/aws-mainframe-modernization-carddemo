# G-Eval Review Approach for CardDemo Requirements Validation

## Overview

This document outlines the G-Eval framework approach for validating user story and technical requirements against the CardDemo codebase using LLM-as-a-judge with chain-of-thoughts (CoT) evaluation.

## G-Eval Framework Benefits

### **Key Advantages:**

- **Custom Evaluation Criteria:** Define evaluation metrics specific to mainframe modernization
- **LLM-as-a-Judge:** Uses LLM to evaluate outputs based on custom criteria
- **Chain-of-Thoughts (CoT):** Provides reasoning for evaluation decisions
- **No Predefined Expected Output:** Evaluates based on criteria, not exact matches
- **Flexible Validation:** Can validate any type of requirement without predefined answers

### **Problem Solved:**

- **Traditional Approach:** Need exact expected output to compare against
- **G-Eval Approach:** Define evaluation criteria, let LLM judge based on those criteria
- **Result:** Flexible evaluation without requiring predefined expected outputs

## Evaluation Criteria Framework

### **Technical Feasibility Criteria:**

```python
technical_feasibility_criteria = {
    "mainframe_technology_alignment": "Does the requirement align with IMS/DB2/CICS capabilities?",
    "implementation_complexity": "Is the implementation complexity appropriate for the requirement?",
    "performance_considerations": "Are performance implications reasonable for the requirement?",
    "integration_feasibility": "Can this be integrated with existing mainframe systems?"
}
```

### **Business Logic Validation Criteria:**

```python
business_logic_criteria = {
    "credit_card_processing_alignment": "Does this align with credit card processing business rules?",
    "fraud_detection_consistency": "Is this consistent with fraud detection requirements?",
    "audit_compliance": "Does this meet audit and compliance requirements?",
    "real_time_processing": "Is real-time processing capability properly addressed?"
}
```

### **Architecture Compatibility Criteria:**

```python
architecture_criteria = {
    "system_integration": "Is this compatible with existing system architecture?",
    "data_consistency": "Does this maintain data consistency across IMS/DB2?",
    "scalability": "Is the solution scalable for production workloads?",
    "maintainability": "Is the solution maintainable and supportable?"
}
```

## Analyzable Objects for G-Eval Input

### **Business Rules (User Stories):**

```python
business_rules_inputs = [
    "The credit card number must be 16 digits and numeric.",
    "The transaction amount must be a positive decimal value.",
    "Authorization requests must include a valid card expiry date in MMYY format.",
    "Fraud detection rules must be applied to all authorization requests.",
    "Authorization requests must be processed in real-time using MQ.",
    "All approved transactions must be stored in the IMS database.",
    "All declined transactions must include a reason code.",
    "The system must ensure two-phase commit transactions across IMS DB and DB2.",
    "Authorization requests must be logged for audit purposes."
]
```

### **Technical Requirements (Parsed):**

```python
technical_requirements_inputs = [
    "AUTHFRDS table in DB2 to store authorization and fraud-related data.",
    "PA_AUTHORIZATION_DETAILS segment in IMS DB for hierarchical storage of authorization details.",
    "Validate credit card number format and length.",
    "Ensure transaction amount is within permissible limits.",
    "Check for expired cards and invalid authorization types.",
    "Detect potential fraud using predefined rules.",
    "MQ for asynchronous communication.",
    "IMS DB for hierarchical data storage.",
    "DB2 for relational data storage and fraud analytics.",
    "Return error messages for invalid credit card numbers.",
    "Provide reasons for declined transactions.",
    "Flag transactions for review in case of suspected fraud.",
    "Log all transactions in DB2 for audit purposes.",
    "Ensure two-phase commit transactions across IMS DB and DB2.",
    "Provide screens for submitting authorization requests and viewing authorization details."
]
```

### **Architecture Components:**

```python
architecture_components_inputs = [
    "IMS DB",
    "BMS",
    "MQ",
    "DB2",
    "CICS",
    "COBOL"
]
```

## Codebase Context for G-Eval

### **Database Schema Context:**

```python
database_context = {
    "existing_tables": ["AUTHFRDS", "CUSTOMER", "TRANSACTION", "FRAUD_DETECTION"],
    "existing_segments": ["PA_AUTHORIZATION_DETAILS", "CUSTOMER_INFO", "TRANSACTION_HISTORY"],
    "data_relationships": ["Customer -> Transactions", "Authorization -> Fraud Detection"],
    "storage_patterns": ["Hierarchical (IMS)", "Relational (DB2)", "VSAM Files"]
}
```

### **Program Context:**

```python
program_context = {
    "existing_programs": ["COPAUA0C", "COPAUS0C", "COPAUS1C", "COPAUS2C", "CBPAUP0C"],
    "cics_transactions": ["CP00", "CPVS", "CPVD"],
    "mq_queues": ["AWS.M2.CARDDEMO.PAUTH.REQUEST", "AWS.M2.CARDDEMO.PAUTH.REPLY"],
    "validation_logic": ["Credit card format validation", "Amount validation", "Expiry validation"]
}
```

### **Integration Context:**

```python
integration_context = {
    "existing_integrations": ["IMS-DB2 two-phase commit", "MQ message queuing", "CICS transaction processing"],
    "interface_patterns": ["BMS screen interfaces", "MQ asynchronous communication", "Database transactions"],
    "error_handling": ["Invalid card number errors", "Declined transaction reasons", "Fraud detection flags"]
}
```

## G-Eval Implementation Strategy

### **Phase 1: Requirements Validation**

```python
def validate_requirements_with_g_eval(requirements, criteria, context):
    """
    Validate requirements using G-Eval framework
    """
    validation_results = []

    for requirement in requirements:
        g_eval_result = g_eval_validate(
            requirement=requirement,
            criteria=criteria,
            context=context,
            chain_of_thoughts=True
        )
        validation_results.append({
            "requirement": requirement,
            "validation_result": g_eval_result,
            "confidence_score": g_eval_result.confidence,
            "reasoning": g_eval_result.reasoning
        })

    return validation_results
```

### **Phase 2: Gap Analysis**

```python
def identify_missing_requirements(user_story_requirements, codebase_requirements):
    """
    Identify requirements that exist in user stories but not in codebase
    """
    missing_requirements = []

    for requirement in user_story_requirements:
        if not requirement_exists_in_codebase(requirement, codebase_requirements):
            missing_requirements.append({
                "requirement": requirement,
                "gap_type": "missing_implementation",
                "priority": assess_requirement_priority(requirement)
            })

    return missing_requirements
```

### **Phase 3: Codebase Requirement Extraction**

```python
class CodebaseRequirementExtractor:
    def extract_database_requirements(self):
        """Extract database requirements from DDL/DBD files"""
        return {
            "tables": self.extract_db2_tables(),
            "segments": self.extract_ims_segments(),
            "relationships": self.extract_relationships(),
            "constraints": self.extract_constraints()
        }

    def extract_program_requirements(self):
        """Extract program requirements from COBOL source"""
        return {
            "programs": self.extract_cobol_programs(),
            "transactions": self.extract_cics_transactions(),
            "validations": self.extract_validation_logic(),
            "business_logic": self.extract_business_logic()
        }

    def extract_integration_requirements(self):
        """Extract integration requirements from MQ/JCL"""
        return {
            "queues": self.extract_mq_queues(),
            "workflows": self.extract_jcl_workflows(),
            "interfaces": self.extract_interface_definitions(),
            "error_handling": self.extract_error_handling()
        }
```

## Validation Workflow

### **Step 1: Extract Codebase Requirements**

```python
# Extract existing requirements from codebase
codebase_extractor = CodebaseRequirementExtractor()
existing_requirements = {
    "database": codebase_extractor.extract_database_requirements(),
    "programs": codebase_extractor.extract_program_requirements(),
    "integrations": codebase_extractor.extract_integration_requirements()
}
```

### **Step 2: Validate User Story Requirements**

```python
# Validate each analyzable object against codebase
for requirement in parsed_technical_requirements:
    validation_result = g_eval_validate(
        requirement=requirement,
        criteria=evaluation_criteria,
        context=existing_requirements,
        chain_of_thoughts=True
    )
    save_validation_result(validation_result)
```

### **Step 3: Identify Missing Requirements**

```python
# Compare user story requirements vs. codebase requirements
missing_requirements = identify_gaps(
    user_story_requirements=parsed_requirements,
    codebase_requirements=existing_requirements
)
```

### **Step 4: Generate Validation Report**

```python
# Generate comprehensive validation report
validation_report = generate_validation_report(
    validation_results=validation_results,
    missing_requirements=missing_requirements,
    codebase_context=existing_requirements
)
```

## Expected G-Eval Outputs

### **Validation Results:**

```json
{
  "requirement": "AUTHFRDS table in DB2 to store authorization and fraud-related data.",
  "validation_result": {
    "technical_feasibility": {
      "score": 0.95,
      "reasoning": "AUTHFRDS table already exists in DB2 schema and is appropriately designed for authorization data storage. The table structure supports fraud-related data fields."
    },
    "implementation_consistency": {
      "score": 0.9,
      "reasoning": "Consistent with existing DB2 table patterns and naming conventions used in the codebase."
    },
    "business_logic_alignment": {
      "score": 0.88,
      "reasoning": "Aligns with credit card authorization business requirements and supports fraud detection workflows."
    }
  },
  "overall_score": 0.91,
  "confidence": "high",
  "recommendations": [
    "Consider adding indexes for fraud detection queries",
    "Ensure proper audit logging for authorization data"
  ]
}
```

### **Gap Analysis Results:**

```json
{
  "missing_requirements": [
    {
      "requirement": "Real-time fraud detection using machine learning algorithms",
      "gap_type": "missing_implementation",
      "priority": "high",
      "impact": "Critical for fraud prevention",
      "recommendation": "Implement ML-based fraud detection module"
    }
  ],
  "incomplete_requirements": [
    {
      "requirement": "Two-phase commit transactions across IMS DB and DB2",
      "status": "partially_implemented",
      "missing_components": ["Transaction coordinator", "Rollback mechanisms"],
      "priority": "medium"
    }
  ]
}
```

## Implementation Benefits

### **1. No Expected Output Required:**

- G-Eval evaluates based on criteria, not exact matches
- Flexible validation for any requirement type
- Adaptable to changing requirements

### **2. Context-Aware Evaluation:**

- Uses actual codebase context for informed decisions
- Considers existing implementation patterns
- Provides realistic feasibility assessment

### **3. Comprehensive Gap Analysis:**

- Identifies missing requirements
- Highlights incomplete implementations
- Prioritizes gaps based on business impact

### **4. Chain-of-Thoughts Reasoning:**

- Provides clear reasoning for validation decisions
- Explains why requirements are feasible or not
- Offers actionable recommendations

### **5. Scalable Approach:**

- Can validate any number of requirements
- Consistent evaluation criteria across all requirements
- Automated validation pipeline

## Next Steps

### **Immediate Actions:**

1. **Set up G-Eval framework** with custom evaluation criteria
2. **Extract codebase requirements** using CodebaseRequirementExtractor
3. **Validate first 10 user stories** using G-Eval approach
4. **Generate initial validation report** with gap analysis

### **Validation Phases:**

- **Phase 1:** Technical feasibility validation
- **Phase 2:** Business logic alignment validation
- **Phase 3:** Architecture compatibility validation
- **Phase 4:** Gap analysis and missing requirements identification

### **Success Metrics:**

- **Validation Coverage:** 100% of analyzable objects validated
- **Gap Identification:** All missing requirements identified
- **Recommendation Quality:** Actionable recommendations provided
- **Processing Time:** Efficient validation pipeline

---

_Document created: 2025-08-26_  
_Purpose: G-Eval framework implementation for CardDemo requirements validation_
