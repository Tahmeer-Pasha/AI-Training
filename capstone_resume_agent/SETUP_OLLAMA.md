# Agentic Resume Shortlisting System Setup

## Prerequisites

### 1. Install Ollama
Download and install Ollama from: https://ollama.ai/

**Windows:**
```bash
# Download the installer from https://ollama.ai/download/windows
# Run the installer and follow the setup wizard
```

**macOS:**
```bash
# Download from https://ollama.ai/download/mac
# Or use Homebrew:
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Install Llama 3
After installing Ollama, pull the Llama 3 model:

```bash
# Start Ollama service (if not auto-started)
ollama serve

# In a new terminal, pull Llama 3
ollama pull llama3

# Verify installation
ollama list
```

### 3. Test Ollama Connection
```bash
# Test that Llama 3 is working
ollama run llama3 "Hello, how are you?"
```

## Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Agentic System

### With Sample Data (Recommended for first test)
```bash
python agentic_main.py --use-sample
```

### With Your Own Data
```bash
python agentic_main.py --job job_description.txt --resumes-folder ./resumes
```

### Traditional Mode (No LLM)
```bash
python agentic_main.py --job job_description.txt --resumes-folder ./resumes --llm-off
```

## Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve
```

### Llama 3 Not Available
```bash
# Check available models
ollama list

# If llama3 is not listed, pull it:
ollama pull llama3
```

### System Information
```bash
python agentic_main.py --system-info
```

## Expected Output

The agentic system will generate enhanced CSV reports with:
- Traditional NLP scores
- LLM-powered analysis scores
- Extracted skills and experience
- Strengths and gaps analysis
- Interview question suggestions
- Intelligent recommendations

## Performance Notes

- First run may be slower as models initialize
- Llama 3 analysis adds ~10-30 seconds per resume
- Traditional mode processes ~50 resumes/minute
- Agentic mode processes ~5-10 resumes/minute