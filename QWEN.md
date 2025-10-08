# LinkedIn Autopost Project

## Project Overview

The `linkedin-autopost` project is a Python application that automates the process of creating and posting LinkedIn content from YouTube video transcripts. It uses AI (via Pydantic AI and OpenAI models) to convert YouTube video transcripts into engaging LinkedIn posts, and then posts them directly to a user's LinkedIn profile using the LinkedIn API.

### Key Features:
- Extracts YouTube video transcripts using the YouTube Transcript API
- Uses AI to convert transcripts into LinkedIn post format with engaging content
- Summarizes long content to stay within LinkedIn's character limits
- Posts content directly to LinkedIn using the LinkedIn API
- Follows best practices for LinkedIn personal branding content

## Architecture

The project consists of a main Python script (`main.py`) that handles:
1. YouTube URL processing and transcript extraction
2. AI-powered content generation and summarization
3. LinkedIn API integration for posting
4. Content formatting following LinkedIn best practices

## Dependencies

The project requires the following key dependencies (from pyproject.toml):
- `pydantic-ai` - AI agent framework
- `openai` - OpenAI integration
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `youtube-transcript-api` - YouTube transcript extraction
- `python-dotenv` - Environment variable management

## Environment Variables

The project requires the following environment variables (see `.env.example`):
- `OPENAI_API` - OpenAI API key
- `USER_SECRET` - LinkedIn user access token

## Building and Running

### Prerequisites
- Python 3.11+
- Valid OpenAI API key
- LinkedIn API access token

### Setup Process
1. Install dependencies with uv or pip:
   ```bash
   uv sync  # if using uv
   # or
   pip install -r requirements.txt  # if you generate requirements from pyproject.toml
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the Application
The application has an interactive menu system:

1. To generate personal branding content from a YouTube URL:
   ```bash
   python main.py
   # Choose option 1, then paste the YouTube URL
   ```

2. To post existing generated content to LinkedIn:
   ```bash
   python main.py
   # Choose option 2, then select from the available .txt files
   ```

## Development Conventions

### Code Style
- The code follows Python best practices
- Uses type hints extensively
- Functions have clear docstrings
- Follows a modular approach with helper functions

### Content Generation Rules
The AI agents follow specific guidelines for generating LinkedIn content:
1. Short, punchy opening paragraphs
2. Short paragraphs (2-5 sentences each)
3. Meaningful substance and value
4. Storytelling elements
5. Show then tell approach

### Testing
- Basic test functionality is available in `test.py`
- The project processes sample markdown files to test content conversion

## File Structure
- `main.py` - Main application logic
- `README.md` - Project description
- `.env.example` - Environment variable template
- `input.md` - Sample input data
- `sample.md` - Sample markdown content
- `output.txt` - Generated output (example)
- `output-summarized.txt` - Summarized output (example)
- `pyproject.toml` - Project dependencies and configuration
- `test.py` - Additional test functionality

## Key Functions
- `_get_youtube_id()` - Extracts YouTube video ID from URL
- `_get_youtube_full_text()` - Combines YouTube transcript into full text
- `get_youtube_text()` - Retrieves complete transcript from YouTube URL
- `get_ai_do_it()` - Main function that generates LinkedIn post from YouTube URL
- `post_content_no_image()` - Posts text content to LinkedIn API
- `post_personal_branding_with_image()` - Posts content with image to LinkedIn