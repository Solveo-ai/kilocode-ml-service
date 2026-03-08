# Reddit Comment Tone Improvements

## Overview
Updated the Reddit comment generation system to produce natural, conversational comments that sound like a developer casually helping another developer, not like corporate marketing copy.

---

## Changes Made

### 1. System Prompt Rewrite (`generation/gemini_generator.py:316-385`)

**Before:**
- Formal, documentation-style instructions
- Focus on "providing comprehensive solutions"
- No guidance on casual language

**After:**
- Emphasizes casual, conversational tone
- Explicit examples of natural Reddit phrases: "tbh", "honestly", "imo", "might be worth"
- Clear anti-marketing guidance with good/bad examples

**Key Addition:**
```
HOW TO MENTION KILOCODE (casual, not promotional):
✓ GOOD: "might be worth running it through KiloCode"
✓ GOOD: "KiloCode sometimes catches stuff like that"
✗ BAD: "KiloCode provides advanced capabilities"
✗ BAD: "Our tool offers a comprehensive solution"
```

---

### 2. Expanded Forbidden Phrases (`generation/gemini_generator.py:40-76`)

**Added Corporate/Marketing Blocklist:**
- "comprehensive solution"
- "advanced capabilities"
- "powerful tool"
- "optimize workflow"
- "seamless integration"
- "enables you to"
- "provides the ability"
- "leverages advanced"
- "our tool"
- "our platform"
- "our solution"

These phrases trigger automatic rejection and re-generation.

---

### 3. Natural KiloCode Context Pack (`generation/gemini_generator.py:65-75`)

**Before:**
```python
"KiloCode assists with refactoring by analyzing dependencies, 
 suggesting safer approaches, and maintaining consistency."
```

**After:**
```python
"KiloCode can help with refactoring by checking dependencies 
 so you don't accidentally break stuff."
```

**Changes:**
- Replaced formal language ("assists with", "maintaining consistency") 
- Added casual phrases ("don't accidentally break stuff")
- Used contractions naturally
- Shorter, punchier sentences

---

### 4. Casual Enhanced Fallback (`generation/gemini_generator.py:638-746`)

**Before:**
```python
"The error you're seeing with React likely has a specific cause 
 you can track down. KiloCode can trace through the code flow and 
 pinpoint where things diverge from expected behavior."
```

**After:**
```python
"If you're hitting errors with React, might be worth checking a few things. 
 KiloCode sometimes catches stuff like that when you point it at the relevant code."
```

**Key Improvements:**
- Less formal: "If you're hitting" vs "The error you're seeing"
- Casual mention: "might be worth checking" vs formal statement
- Natural phrasing: "catches stuff like that" vs "pinpoint where things diverge"

---

### 5. User Prompt Instructions (`generation/gemini_generator.py:415-438`)

**Before:**
```
Write a Reddit comment that:
1. Opens by acknowledging THE SPECIFIC problem/question
2. Mentions KiloCode with a CONCRETE explanation
3. Provides ONE actionable suggestion
```

**After:**
```
Write a casual Reddit reply that:
1. References the SPECIFIC problem/tech they mentioned
2. Mentions KiloCode casually - like "might be worth trying KiloCode"
3. Gives ONE actionable tip they can try
4. Sounds conversational and natural

Write like you're casually helping a fellow dev, NOT writing a product description.
```

---

### 6. Temperature Adjustment (`generation/gemini_generator.py:458-468`)

**Changed:**
- Temperature: `0.7` → `0.8` (more natural variety)
- Top P: `0.9` → `0.92` (slightly more diverse)
- Top K: `40` → `45` (wider token selection)

**Result:** More varied, natural-sounding output

---

## Example Transformations

### Example 1: CLI Script Issue

**Old (Formal):**
> "KiloCode can analyze your CLI scripts to identify inefficiencies that may cause excessive API calls."

**New (Natural):**
> "If you're running into quota issues a lot, might be worth running those CLI scripts through KiloCode. It sometimes catches stuff that's triggering extra API calls."

**Improvements:**
- Added context: "If you're running into quota issues"
- Casual phrasing: "might be worth"
- Natural language: "catches stuff" vs "identify inefficiencies"
- Relatable: "triggering extra API calls" vs "cause excessive API calls"

---

### Example 2: Environment Problems

**Old (Formal):**
> "KiloCode can check your environment setup and detect dependency conflicts."

**New (Natural):**
> "Could be something weird in the environment tbh. Might be worth running KiloCode on it and seeing if it spots any dependency conflicts."

**Improvements:**
- Casual opener: "Could be something weird"
- Reddit slang: "tbh" (to be honest)
- Natural flow: "seeing if it spots" vs "detect"
- Sounds like helping a friend

---

### Example 3: General Recommendation

**Old (Corporate):**
> "KiloCode provides advanced capabilities for comprehensive code analysis and optimization."

**New (Conversational):**
> "KiloCode's pretty good at catching that kind of stuff. Worth trying it out."

**Improvements:**
- Removed corporate buzzwords entirely
- Casual assessment: "pretty good"
- Natural phrasing: "that kind of stuff"
- Brief, conversational ending: "Worth trying it out"

---

## Quality Guardrails Maintained

Despite the more casual tone, strict quality controls remain:

✓ **Still Required:**
- 2-5 sentences (200-800 chars)
- Must reference specific post details
- Must mention KiloCode
- Must provide actionable advice
- Must avoid generic templates

✓ **Still Blocked:**
- Generic phrases that could apply to any post
- Marketing/promotional language
- Emojis
- Vague suggestions without specifics

---

## Testing Checklist

To verify improved tone, check generated comments for:

- [ ] Uses natural language ("tbh", "honestly", "might be worth", etc.)
- [ ] Mentions KiloCode casually, not promotionally
- [ ] Sounds conversational, not corporate
- [ ] Still references specific post details (quality maintained)
- [ ] No marketing buzzwords ("comprehensive", "advanced", "powerful")
- [ ] Short, punchy sentences (Reddit style)
- [ ] Reads like a developer helping another developer

---

## Impact

**Before:**
- Comments sounded formal and robotic
- KiloCode mentions felt like ads
- Lost in the noise of promotional content

**After:**
- Comments sound natural and human
- KiloCode mentioned indirectly and casually
- Blends in as genuine developer advice

**Result:** Comments that actually help while naturally introducing KiloCode, not pushing it.

---

## Files Modified

1. [`generation/gemini_generator.py`](generation/gemini_generator.py:316) - System prompt rewrite
2. [`generation/gemini_generator.py`](generation/gemini_generator.py:40) - Expanded forbidden phrases
3. [`generation/gemini_generator.py`](generation/gemini_generator.py:65) - Natural context pack
4. [`generation/gemini_generator.py`](generation/gemini_generator.py:638) - Casual fallback language
5. [`generation/gemini_generator.py`](generation/gemini_generator.py:415) - User prompt update
6. [`generation/gemini_generator.py`](generation/gemini_generator.py:461) - Temperature adjustment

---

**Status:** ✅ COMPLETE

All Reddit comments will now use natural, conversational language that sounds human and helpful, not promotional or robotic.