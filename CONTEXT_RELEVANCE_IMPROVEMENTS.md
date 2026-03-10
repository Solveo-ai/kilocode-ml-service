# Reddit Comment Context Relevance Improvements

## Overview

This document describes improvements made to the Reddit comment generation system to ensure comments stay highly relevant to the specific content of Reddit posts while maintaining a natural conversational tone.

## Problem Statement

Previously, generated comments could be too generic and didn't always reference specific entities mentioned in the original post. Comments like "Interesting discussion" or "Thanks for sharing" don't add value to the conversation.

## Solution

### 1. Entity Extraction System

Added a comprehensive entity extraction system in [`generation/gemini_generator.py`](generation/gemini_generator.py:255) that identifies:

#### AI Models
- Opus, Sonnet, Haiku, Claude
- GPT-4, GPT-4o, GPT-3.5, GPT
- Kimi, MiniMax, Gemini
- Llama, Mistral, Codestral, DeepSeek
- O1, O1-preview, O1-mini
- Cursor, Aider, Copilot, Codex

#### Developer Tools
- Editors: VSCode, Vim, Neovim, Emacs, JetBrains
- Infrastructure: Docker, Kubernetes, Terraform, Ansible
- Languages: Python, JavaScript, TypeScript, Rust, Go, Java
- Frameworks: React, Vue, Angular, Svelte, Next.js
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Cloud: AWS, Azure, GCP, Vercel, Netlify, Heroku

#### Workflows/Approaches
- TDD, BDD, CI/CD, DevOps
- Microservices, Serverless, MVC
- Refactoring, Testing, Debugging, Profiling

### 2. Enhanced System Prompt

Updated [`_build_system_prompt()`](generation/gemini_generator.py:438) with:

- **Context Relevance Rules**: Explicit instructions to reference specific entities
- **Entity-Specific Examples**: Good examples showing how to reference Opus, Sonnet, Docker, etc.
- **Forbidden Generic Phrases**: Added "Great question" and "Good point" without specific context

### 3. Enhanced User Prompt

Updated [`_build_user_prompt()`](generation/gemini_generator.py:509) with:

- **Entities Section**: New section that lists all detected entities
- **Explicit Reference Instructions**: Warning that comments MUST mention 1-2 entities by name
- **Dynamic Task Instructions**: Task instructions now include specific entity names

### 4. Enhanced Fallback Generator

Updated [`_generate_enhanced_fallback()`](generation/gemini_generator.py:834) to:

- Use extracted entities (models, tools, workflows) as primary entity references
- Format entity names correctly (uppercase for OPUS, SONNET, etc.)
- Include entity type detection for more contextual responses

## Code Changes

### New Functions

```python
def _extract_specific_entities(post_title: str, post_content: str) -> Dict[str, List[str]]:
    """
    Extract specific entities mentioned in the post for context relevance.
    
    Returns:
        Dict with keys: 'models', 'tools', 'workflows', 'technologies', 'problems'
    """
```

### Modified Functions

1. **`_extract_key_points()`** - Now includes extracted entities as the first key points
2. **`_build_system_prompt()`** - Added context relevance rules and entity-specific examples
3. **`_build_user_prompt()`** - Added entities section with explicit reference instructions
4. **`_generate_enhanced_fallback()`** - Uses extracted entities for contextual responses

## Quality Guardrails

### Forbidden Phrases (Never Allowed)
- "Interesting discussion"
- "Thanks for sharing"
- "Great post"
- "Nice thread"
- "Good topic"
- "Great question" (without specific context)
- "Good point" (without specific context)

### Generic Phrases (Rejected by Quality Check)
- "many developers encounter"
- "comprehensive solution"
- "advanced capabilities"
- "powerful tool"
- "optimize workflow"
- "seamless integration"

## Example Outputs

### Before (Generic)
> "This is something many developers encounter. KiloCode can help analyze the problem systematically."

### After (Context-Aware)
> "Honestly both Opus and Sonnet are pretty solid for coding tasks, but Opus tends to handle more complex refactoring better. Might be worth running your codebase through KiloCode to see which model catches more issues in your specific setup."

### Before (Generic)
> "Thanks for sharing this interesting discussion about Docker."

### After (Context-Aware)
> "Docker networking can be a pain to debug tbh. Might be worth running KiloCode on your compose file and seeing if it spots any config issues with the container setup."

## Testing

A test file [`test_context_relevance.py`](test_context_relevance.py) was created to verify:

1. Entity extraction works correctly for models, tools, workflows
2. Key points include extracted entities
3. Fallback comments reference specific entities
4. No generic or forbidden phrases are generated

## Files Modified

1. [`generation/gemini_generator.py`](generation/gemini_generator.py) - Main changes to entity extraction and prompt building

## Files Created

1. [`test_context_relevance.py`](test_context_relevance.py) - Test suite for context relevance improvements

## Benefits

1. **Higher Relevance**: Comments now directly reference the specific technologies, models, and tools mentioned in posts
2. **Better Engagement**: Natural, developer-to-developer tone that fits Reddit culture
3. **No Generic Content**: Quality guardrails prevent generic, low-value comments
4. **Entity Awareness**: System recognizes and references AI models, tools, and workflows commonly discussed in developer communities