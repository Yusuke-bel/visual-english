# CLAUDE.md - AI Assistant Guide for Visual English

## Project Overview

**Visual English** is a Streamlit web application that helps users understand English sentence structures through AI-powered analysis. The application takes English sentences as input and provides:

- Natural Japanese translations
- Grammar point explanations
- Color-coded structural blocks (Subject/Verb/Object/Complement/Modifier)
- Graphviz syntax tree visualizations

The AI backend uses Google's Gemini 2.5 Flash API for natural language processing.

## Codebase Structure

```
visual-english/
├── app.py              # Main application (single-file Streamlit app)
├── requirements.txt    # Python dependencies
├── CLAUDE.md           # This file - AI assistant guidance
└── .git/               # Git repository
```

This is a minimal, single-file application with no additional directories or modules.

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Programming language |
| Streamlit | Web UI framework |
| google-generativeai | Gemini API client (>=0.8.3) |
| Graphviz | Syntax tree visualization (runtime dependency) |

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The application requires:
1. A valid Gemini API key (entered via the UI)
2. Graphviz installed on the system for syntax tree rendering

## Key Architecture Patterns

### Single-File Structure
The entire application is contained in `app.py` (~135 lines):
- Lines 1-3: Imports
- Lines 5-11: Page configuration
- Lines 13-31: CSS styling (inline)
- Lines 33-59: UI layout and input components
- Lines 61-134: Analysis logic and results display

### Styling Approach
- All CSS is embedded inline using `st.markdown()` with `unsafe_allow_html=True`
- Design follows a "Wise-inspired" aesthetic with dark navy (#163354) header and green (#2ED06E) accents
- Responsive layout using Streamlit columns

### AI Integration Pattern
- Prompt engineering with strict JSON output schema (lines 76-96)
- Response cleaning to strip markdown code blocks
- JSON parsing of AI response for structured data extraction

### Color Scheme for Grammar Roles
| Role | Color | Hex |
|------|-------|-----|
| Subject (S) | Light blue | #E3F2FD |
| Verb (V) | Light orange | #FBE9E7 |
| Object/Complement (O/C) | Light green | #E8F5E9 |
| Modifier (M) | Light yellow | #FFF3E0 |

## Code Conventions

### Language
- **UI text**: Japanese (日本語)
- **Code comments**: Japanese
- **Variable names**: English with descriptive naming

### Naming Conventions
- Variables: `snake_case` (e.g., `api_key_input`, `input_text`, `analyze_btn`)
- CSS classes: `kebab-case` (e.g., `.block-item`, `.input-card`)

### Error Handling
- Single try-catch block wraps the entire analysis logic
- User-friendly error messages in Japanese
- Raw exception displayed via `st.code(e)` for debugging

## Important Files Reference

### app.py
The main application file containing:
- `st.set_page_config()` - App metadata and layout settings
- Custom CSS for Wise-inspired design
- Input interface with API key expander and text area
- Gemini API integration with prompt engineering
- Results rendering with translation, grammar blocks, and syntax tree

### requirements.txt
```
streamlit
google-generativeai>=0.8.3
```

## Development Guidelines

### When Modifying This Project

1. **Maintain single-file structure** - Keep all logic in `app.py` unless complexity demands splitting
2. **Preserve Japanese UI** - All user-facing text should remain in Japanese
3. **Keep CSS inline** - Follow the existing pattern of embedded styles
4. **Maintain color consistency** - Use the established palette for grammar roles
5. **JSON schema stability** - The AI prompt defines a specific JSON structure; changes require updating both prompt and rendering logic

### Common Tasks

**Adding a new grammar role color:**
1. Update the prompt in `app.py` (lines 93-94) with the new role and color
2. No other changes needed as colors come from AI response

**Modifying the UI layout:**
1. Edit the CSS in the `st.markdown()` block (lines 14-30)
2. Adjust column structure in the layout section (lines 33-59)

**Changing the AI model:**
1. Modify line 73: `model = genai.GenerativeModel('gemini-1.5-flash')`
2. Ensure the new model supports the same response format

### Testing Considerations
- No automated tests exist in this project
- Manual testing: Enter various English sentences and verify structural analysis
- Edge cases to test: complex sentences, passive voice, questions, imperatives

## Known Limitations

1. **No caching** - Every analysis hits the Gemini API
2. **No rate limiting** - Potential for API quota exhaustion
3. **API key in UI** - Not suitable for shared deployments
4. **No input validation** - Very long sentences may cause issues
5. **Graphviz dependency** - Must be installed separately on the system

## Git Workflow

- **Main development**: Direct commits to feature branches
- **Commit style**: Simple "Update app.py" messages historically used
- **Branch naming**: `claude/` prefix for AI-assisted work

## Quick Reference

### File Locations
| What | Where |
|------|-------|
| Main app | `app.py` |
| Dependencies | `requirements.txt` |
| Styling | `app.py` lines 14-30 |
| AI prompt | `app.py` lines 76-96 |
| Results rendering | `app.py` lines 102-130 |

### Key Functions/Sections
- Page config: `st.set_page_config()` at line 6
- API configuration: `genai.configure()` at line 72
- Model initialization: `genai.GenerativeModel()` at line 73
- Content generation: `model.generate_content()` at line 98
- Block rendering: Lines 115-126
- Syntax tree: `st.graphviz_chart()` at line 130
