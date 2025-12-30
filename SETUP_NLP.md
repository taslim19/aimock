# NLP Setup Instructions

This project now uses **spaCy** for advanced Natural Language Processing.

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download spaCy English Model

After installing spaCy, you need to download the English language model. **We recommend the medium model** for better accuracy:

```bash
# Recommended: Medium model with word vectors (better similarity accuracy)
python -m spacy download en_core_web_md

# Alternative: Large model (best accuracy, but larger ~560MB)
# python -m spacy download en_core_web_lg

# Fallback: Small model (works but less accurate similarity)
# python -m spacy download en_core_web_sm
```

**Note**: The system will automatically try to use the best available model (md > lg > sm).

### 3. Verify Installation

Test that spaCy is working:

```bash
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('spaCy installed successfully!')"
```

## What NLP Features Are Used

### In Answer Evaluator (`evaluator.py`):

1. **Semantic Similarity**: Compares answer relevance to questions using word vectors
2. **Named Entity Recognition (NER)**: Identifies important entities in text
3. **Part-of-Speech Tagging**: Analyzes grammatical structure
4. **Lemmatization**: Normalizes words to their root forms for better keyword matching
5. **Advanced Sentence Analysis**: Evaluates sentence complexity and structure
6. **Stop Word Filtering**: Uses spaCy's built-in stop words

### In Question Generator (`question_generator.py`):

- Ready for NLP enhancements (currently uses template-based generation)
- Can be extended with NLP for dynamic question generation

## Fallback Behavior

If spaCy is not installed, the system will:
- Display a warning message
- Fall back to basic rule-based text processing
- Continue to function (with reduced accuracy)

## Troubleshooting

### Error: "Can't find model 'en_core_web_sm'"

**Solution:**
```bash
# Install the recommended model with word vectors
python -m spacy download en_core_web_md

# Or if you prefer the small model (less accurate)
python -m spacy download en_core_web_sm
```

### Error: "No module named 'spacy'"

**Solution:**
```bash
pip install spacy
python -m spacy download en_core_web_md
```

### Model Download Fails

If the download fails, try:
```bash
# Download directly
python -m spacy download en_core_web_sm --direct

# Or use alternative model
python -m spacy download en_core_web_lg  # Larger, more accurate model
```

Then update `evaluator.py` and `question_generator.py` to use `en_core_web_lg` instead of `en_core_web_sm`.

## Performance Notes

- **en_core_web_sm**: Small model (~12MB), faster, but **no word vectors** (less accurate similarity)
- **en_core_web_md**: Medium model (~40MB), **includes word vectors** (recommended for best balance)
- **en_core_web_lg**: Large model (~560MB), best accuracy but slower

**The system automatically uses the best available model** (tries md → lg → sm in order).

**For accurate semantic similarity scoring, use `en_core_web_md` or larger.**

## Next Steps

After installation, restart your Flask application:

```bash
python app.py
```

The NLP features will automatically activate when spaCy is available.

