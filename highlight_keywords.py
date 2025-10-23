import re

def highlight_keywords(text, tokens):
    """Return `text` with each token wrapped in an HTML <mark> tag (case-insensitive)."""
    highlighted = text
    for t in tokens:
        pattern = re.compile(re.escape(t), re.IGNORECASE)
        highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", highlighted)
    return highlighted


if __name__ == "__main__":
    sample_text = "California insurance policies often face nonrenewal issues."
    keywords = ["california", "nonrenewal", "insurance"]
    result = highlight_keywords(sample_text, keywords)
    print(result)