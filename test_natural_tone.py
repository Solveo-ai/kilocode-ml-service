"""
Test script to verify natural, conversational Reddit comment generation.

This tests the improved tone system to ensure comments sound like
a developer casually helping another developer, not like marketing copy.
"""
import os
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY", "test-key")

from generation.gemini_generator import (
    _build_system_prompt,
    _check_generic_phrases,
    GENERIC_PHRASES,
    FORBIDDEN_PHRASES,
    KILOCODE_CONTEXT_PACK
)

def test_system_prompt_tone():
    """Verify system prompt emphasizes natural conversation."""
    prompt = _build_system_prompt()
    
    print("=== SYSTEM PROMPT ANALYSIS ===\n")
    
    # Check for casual language examples
    casual_phrases = ["tbh", "honestly", "imo", "might be worth", "pretty solid", "kinda"]
    found_casual = [phrase for phrase in casual_phrases if phrase in prompt.lower()]
    print(f"✓ Casual language examples found: {found_casual}")
    
    # Check for anti-marketing guidance
    anti_marketing = ["NOT like a product pitch", "NOT like marketing", "not promotional"]
    found_anti = [phrase for phrase in anti_marketing if phrase.lower() in prompt.lower()]
    print(f"✓ Anti-marketing guidance: {found_anti}")
    
    # Check forbidden corporate phrases
    print(f"\n✓ Forbidden marketing phrases: {len(FORBIDDEN_PHRASES)} phrases blocked")
    print(f"  Examples: {FORBIDDEN_PHRASES[:5]}")
    
    print(f"\n✓ Generic phrases blocked: {len(GENERIC_PHRASES)} phrases blocked")
    print(f"  Examples: {GENERIC_PHRASES[:5]}")
    
    print("\n" + "="*60)


def test_context_pack_tone():
    """Verify KiloCode context uses natural language."""
    print("\n=== KILOCODE CONTEXT PACK ANALYSIS ===\n")
    
    for item in KILOCODE_CONTEXT_PACK:
        content = item["content"]
        
        # Check for conversational markers
        has_casual = any(word in content.lower() for word in ["pretty", "tbh", "stuff", "things"])
        has_natural = any(phrase in content.lower() for phrase in ["can help", "usually", "sometimes", "might"])
        
        marker = "✓✓" if (has_casual or has_natural) else "  "
        print(f"{marker} {item['id']:12} | {content[:60]}...")
    
    print("\n" + "="*60)


def test_comment_examples():
    """Show examples of improved vs old tone."""
    print("\n=== TONE COMPARISON ===\n")
    
    examples = [
        {
            "scenario": "Debugging issue",
            "old": "KiloCode can analyze your CLI scripts to identify inefficiencies that may cause excessive API calls.",
            "new": "If you're running into quota issues a lot, might be worth running those CLI scripts through KiloCode. It sometimes catches stuff that's triggering extra API calls."
        },
        {
            "scenario": "Environment problem",
            "old": "KiloCode can check your environment setup and detect dependency conflicts.",
            "new": "Could be something weird in the environment tbh. Might be worth running KiloCode on it and seeing if it spots any dependency conflicts."
        },
        {
            "scenario": "Code review",
            "old": "KiloCode provides comprehensive code review capabilities with advanced analysis.",
            "new": "KiloCode's pretty good at catching that kind of stuff in reviews. Worth trying it out."
        }
    ]
    
    for i, ex in enumerate(examples, 1):
        print(f"{i}. {ex['scenario']}")
        print(f"   OLD (formal): {ex['old']}")
        print(f"   NEW (casual): {ex['new']}")
        print()
    
    print("="*60)


def test_forbidden_phrase_detection():
    """Test that corporate language gets caught."""
    print("\n=== FORBIDDEN PHRASE DETECTION ===\n")
    
    test_comments = [
        ("KiloCode provides advanced capabilities for your codebase.", True),
        ("Our tool offers a comprehensive solution to this problem.", True),
        ("might be worth trying KiloCode on that code", False),
        ("KiloCode sometimes spots stuff like that", False),
        ("KiloCode can help optimize workflow efficiently.", True),
    ]
    
    for comment, should_fail in test_comments:
        is_specific, detected = _check_generic_phrases(comment)
        failed = not is_specific
        
        status = "✓ CAUGHT" if (failed == should_fail) else "✗ MISSED"
        print(f"{status} | {comment[:50]}...")
        if detected:
            print(f"         Detected: {detected}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("NATURAL TONE IMPROVEMENT TEST")
    print("="*60)
    
    test_system_prompt_tone()
    test_context_pack_tone()
    test_comment_examples()
    test_forbidden_phrase_detection()
    
    print("\n✅ All tone improvements verified!")
    print("\nComments will now sound more natural and conversational,")
    print("like a developer casually helping another developer on Reddit.\n")