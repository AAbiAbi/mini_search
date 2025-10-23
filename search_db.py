import sqlite3, re
from highlight_keywords import highlight_keywords
def search_db(query):
    tokens = query.lower().split()
    where = " OR ".join(["text LIKE ?"] * len(tokens))
    params = [f"%{t}%" for t in tokens]
    q = f"SELECT id, path, text, clicks FROM docs WHERE {where}"

    with sqlite3.connect("index.db") as conn:
        c = conn.cursor()
        results = c.execute(q, params).fetchall()

    scored = []
    for rid, path, text, clicks in results:
        score = sum(text.lower().count(t) for t in tokens) + clicks * 0.5
        m = re.search(tokens[0], text, re.I)
        snippet = text[max(0, m.start()-50):m.end()+100] if m else text[:150]
        snippet = highlight_keywords(snippet, tokens)
        scored.append((score, rid, path, snippet, clicks))
    return sorted(scored, reverse=True)
