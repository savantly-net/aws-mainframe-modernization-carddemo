# DeepEval API Keys Explanation

## 🤔 **Common Confusion**

Many users are confused about why DeepEval requires API keys when it's supposed to run locally. This document clarifies the difference between DeepEval and DeepEval Cloud, and explains why API keys are still needed.

## 🔍 **DeepEval vs DeepEval Cloud**

### **DeepEval (Local)**

- ✅ Runs locally on your machine
- ✅ No DeepEval Cloud subscription required
- ❌ **Still needs LLM API keys** for semantic analysis
- ❌ Cannot perform semantic validation without an LLM provider

### **DeepEval Cloud**

- ❌ Runs on DeepEval's servers
- ❌ Requires DeepEval Cloud subscription
- ❌ Requires DeepEval API keys
- ✅ Managed service with built-in LLM providers

## 🧠 **Why DeepEval Needs LLM API Keys**

DeepEval performs **semantic analysis** of requirements, which requires:

1. **Understanding natural language** - What does the requirement mean?
2. **Semantic similarity** - How relevant is this requirement to the codebase?
3. **Hallucination detection** - Is the requirement making false claims?

These tasks require a **Large Language Model (LLM)** such as:

- OpenAI GPT-4/GPT-3.5
- Azure OpenAI
- Anthropic Claude
- Google Gemini

## 🔧 **API Key Requirements**

### **Required for Semantic Analysis:**

- **OpenAI API Key** (for GPT models)
- **Azure OpenAI API Key** (for Azure GPT models)
- **Anthropic API Key** (for Claude models)
- **Google API Key** (for Gemini models)

### **NOT Required:**

- DeepEval Cloud API keys (unless using DeepEval Cloud)
- DeepEval subscription

## 📊 **Validation Modes**

### **1. Basic Validation (No API Keys Required)**

```python
enable_deepeval=False
```

- ✅ **No API keys needed**
- ✅ **Runs completely locally**
- ✅ **Fast execution**
- ❌ **Limited to keyword matching**
- ❌ **No semantic understanding**

**What it does:**

- Extracts component names from requirements
- Checks if mentioned components exist in codebase
- Performs basic architectural consistency checks
- Uses simple pattern matching

### **2. DeepEval Validation (API Keys Required)**

```python
enable_deepeval=True
```

- ❌ **Requires LLM API keys**
- ✅ **Runs locally** (not on DeepEval Cloud)
- ✅ **Semantic understanding**
- ✅ **Advanced analysis**

**What it does:**

- Understands requirement meaning and context
- Detects hallucinations and false claims
- Performs semantic similarity analysis
- Provides detailed improvement suggestions

## 🚀 **How to Use**

### **Option 1: Basic Validation (Recommended for most users)**

```bash
cd validator-python/src
python run_basic_validation.py
```

- No API keys needed
- Fast and reliable
- Good for component validation

### **Option 2: DeepEval with API Keys**

```bash
# Set your API key
export OPENAI_API_KEY="your-api-key-here"

# Run with DeepEval enabled
cd validator-python/src
python run_basic_validation.py  # Edit to set enable_deepeval=True
```

## 💡 **Recommendations**

### **For Most Users:**

- Use **Basic Validation** - it's sufficient for most component validation needs
- No API keys required
- Fast and reliable

### **For Advanced Analysis:**

- Use **DeepEval Validation** if you need semantic understanding
- Requires LLM API key
- Provides more detailed analysis

## 🔍 **What Each Mode Validates**

| Feature                   | Basic Validation | DeepEval Validation |
| ------------------------- | ---------------- | ------------------- |
| Component existence       | ✅               | ✅                  |
| Architectural consistency | ✅               | ✅                  |
| Semantic understanding    | ❌               | ✅                  |
| Hallucination detection   | ❌               | ✅                  |
| Improvement suggestions   | Basic            | Detailed            |
| API keys required         | ❌               | ✅                  |
| Execution speed           | Fast             | Slower              |
| Accuracy                  | Good             | Excellent           |

## 🛠️ **Troubleshooting**

### **"DeepEval validation failed" Error**

This means:

1. DeepEval tried to use an LLM model
2. No API key was configured
3. It fell back to basic validation
4. This is **normal behavior** - basic validation still works

### **"API configuration" Error**

This means:

1. You're trying to use DeepEval semantic analysis
2. No LLM API key is configured
3. **Solution**: Either configure an API key or use basic validation

## 📝 **Summary**

- **DeepEval runs locally** but needs LLM API keys for semantic analysis
- **Basic validation** requires no API keys and runs completely locally
- **Both modes** provide useful validation, just at different levels of sophistication
- **Most users** should use basic validation unless they need semantic analysis
