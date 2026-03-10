"""
Test script for Reddit comment context relevance improvements.

Tests that comments properly reference:
- AI models (Opus, Sonnet, GPT, Kimi, MiniMax, etc.)
- Tools (VSCode, Docker, React, Python, etc.)
- Workflows (TDD, CI/CD, debugging, etc.)
- Specific problems mentioned in posts
"""
import sys
sys.path.insert(0, '.')

from generation.gemini_generator import (
    _extract_specific_entities,
    _extract_key_points,
    _generate_enhanced_fallback,
    _check_generic_phrases,
    FORBIDDEN_PHRASES,
    GENERIC_PHRASES,
)


def test_entity_extraction():
    """Test that entities are correctly extracted from posts."""
    print("\n=== Testing Entity Extraction ===\n")
    
    # Test 1: AI Models extraction
    post_title = "Opus vs Sonnet for coding tasks"
    post_content = "I've been comparing Opus and Sonnet for my daily coding workflow. Also tried GPT-4 and Kimi for comparison."
    
    entities = _extract_specific_entities(post_title, post_content)
    print(f"Post: {post_title}")
    print(f"Extracted models: {entities['models']}")
    assert "opus" in entities['models'], "Should extract Opus"
    assert "sonnet" in entities['models'], "Should extract Sonnet"
    assert "gpt-4" in entities['models'], "Should extract GPT-4"
    assert "kimi" in entities['models'], "Should extract Kimi"
    print("✓ AI Models extraction working\n")
    
    # Test 2: Tools extraction
    post_title = "Setting up VSCode with Docker"
    post_content = "I'm trying to configure VSCode to work with Docker and Kubernetes for my React project."
    
    entities = _extract_specific_entities(post_title, post_content)
    print(f"Post: {post_title}")
    print(f"Extracted tools: {entities['tools']}")
    assert "vscode" in entities['tools'], "Should extract VSCode"
    assert "docker" in entities['tools'], "Should extract Docker"
    assert "kubernetes" in entities['tools'], "Should extract Kubernetes"
    assert "react" in entities['tools'], "Should extract React"
    print("✓ Tools extraction working\n")
    
    # Test 3: Workflows extraction
    post_title = "Best practices for TDD in Python"
    post_content = "Looking for advice on TDD workflow and CI/CD integration with GitHub Actions."
    
    entities = _extract_specific_entities(post_title, post_content)
    print(f"Post: {post_title}")
    print(f"Extracted workflows: {entities['workflows']}")
    assert "tdd" in entities['workflows'], "Should extract TDD"
    assert "ci/cd" in entities['workflows'] or "cicd" in entities['workflows'], "Should extract CI/CD"
    print("✓ Workflows extraction working\n")
    
    # Test 4: Problem extraction
    post_title = "Having trouble with React useEffect"
    post_content = "I'm having trouble with React useEffect dependency array warnings in my component."
    
    entities = _extract_specific_entities(post_title, post_content)
    print(f"Post: {post_title}")
    print(f"Extracted problems: {entities['problems']}")
    print(f"Extracted tools: {entities['tools']}")
    assert "react" in entities['tools'], "Should extract React"
    print("✓ Problem extraction working\n")


def test_key_points_extraction():
    """Test that key points include entities."""
    print("\n=== Testing Key Points Extraction ===\n")
    
    post_title = "Comparing Claude Opus vs GPT-4 for code review"
    post_content = "I've been using both Opus and GPT-4 for code reviews in my GitHub workflow. Looking for opinions on which handles complex refactoring better."
    
    key_points = _extract_key_points(post_title, post_content)
    print(f"Post: {post_title}")
    print(f"Key points: {key_points}")
    
    # Check that models are in key points
    models_found = any("opus" in kp.lower() or "gpt" in kp.lower() for kp in key_points)
    assert models_found, "Key points should include AI models"
    
    # Check that tools are in key points
    tools_found = any("github" in kp.lower() for kp in key_points)
    assert tools_found, "Key points should include tools"
    print("✓ Key points extraction working\n")


def test_enhanced_fallback():
    """Test that fallback comments reference specific entities."""
    print("\n=== Testing Enhanced Fallback ===\n")
    
    # Test 1: Fallback with AI models
    post_title = "Opus vs Sonnet comparison"
    post_content = "Which model is better for coding tasks - Opus or Sonnet?"
    key_points = _extract_key_points(post_title, post_content)
    
    comment = _generate_enhanced_fallback(post_title, post_content, key_points, ["core"])
    print(f"Post: {post_title}")
    print(f"Generated comment: {comment}")
    
    # Check that comment references the models
    assert "opus" in comment.lower() or "sonnet" in comment.lower(), "Comment should reference Opus or Sonnet"
    assert "kilocode" in comment.lower(), "Comment should mention KiloCode"
    
    # Check for forbidden phrases
    for phrase in FORBIDDEN_PHRASES:
        assert phrase not in comment.lower(), f"Comment should not contain forbidden phrase: {phrase}"
    
    print("✓ Fallback with AI models working\n")
    
    # Test 2: Fallback with tools
    post_title = "Docker container networking issues"
    post_content = "I'm having issues with Docker container networking in my Kubernetes cluster."
    key_points = _extract_key_points(post_title, post_content)
    
    comment = _generate_enhanced_fallback(post_title, post_content, key_points, ["debugging"])
    print(f"Post: {post_title}")
    print(f"Generated comment: {comment}")
    
    # Check that comment references the tools
    assert "docker" in comment.lower() or "kubernetes" in comment.lower(), "Comment should reference Docker or Kubernetes"
    assert "kilocode" in comment.lower(), "Comment should mention KiloCode"
    print("✓ Fallback with tools working\n")
    
    # Test 3: Fallback with workflows
    post_title = "TDD best practices"
    post_content = "What are your best practices for TDD in a CI/CD pipeline?"
    key_points = _extract_key_points(post_title, post_content)
    
    comment = _generate_enhanced_fallback(post_title, post_content, key_points, ["testing"])
    print(f"Post: {post_title}")
    print(f"Generated comment: {comment}")
    
    # Check that comment references the workflow
    assert "tdd" in comment.lower() or "ci/cd" in comment.lower() or "cicd" in comment.lower(), "Comment should reference TDD or CI/CD"
    assert "kilocode" in comment.lower(), "Comment should mention KiloCode"
    print("✓ Fallback with workflows working\n")


def test_no_generic_phrases():
    """Test that generated comments don't contain generic phrases."""
    print("\n=== Testing No Generic Phrases ===\n")
    
    test_posts = [
        ("Opus vs Sonnet for coding", "Which model handles complex codebases better?"),
        ("Docker networking problems", "My Docker containers can't communicate with each other."),
        ("React performance issues", "My React app is slow and I need help optimizing."),
        ("TDD workflow questions", "How do you integrate TDD with GitHub Actions?"),
    ]
    
    for title, content in test_posts:
        key_points = _extract_key_points(title, content)
        comment = _generate_enhanced_fallback(title, content, key_points, ["core"])
        
        # Check for generic phrases
        is_specific, detected = _check_generic_phrases(comment)
        
        print(f"Post: {title}")
        print(f"Comment: {comment}")
        print(f"Generic phrases detected: {detected}")
        assert is_specific, f"Comment should not contain generic phrases: {detected}"
        print("✓ No generic phrases\n")


def test_forbidden_phrases():
    """Test that forbidden phrases are never in generated comments."""
    print("\n=== Testing Forbidden Phrases ===\n")
    
    test_posts = [
        ("Interesting discussion about AI", "What do you think about AI coding assistants?"),
        ("Great post about Docker", "Docker is amazing for development."),
        ("Thanks for sharing this", "I learned a lot from this post."),
    ]
    
    for title, content in test_posts:
        key_points = _extract_key_points(title, content)
        comment = _generate_enhanced_fallback(title, content, key_points, ["core"])
        
        print(f"Post: {title}")
        print(f"Comment: {comment}")
        
        for phrase in FORBIDDEN_PHRASES:
            assert phrase not in comment.lower(), f"Comment should not contain forbidden phrase: '{phrase}'"
        
        print("✓ No forbidden phrases\n")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("REDDIT COMMENT CONTEXT RELEVANCE TESTS")
    print("=" * 60)
    
    try:
        test_entity_extraction()
        test_key_points_extraction()
        test_enhanced_fallback()
        test_no_generic_phrases()
        test_forbidden_phrases()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60 + "\n")
        return True
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)