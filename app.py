from flask import Flask, request, render_template
import sqlite3, re
from search_db import search_db

app = Flask(__name__)


@app.route("/")
def home():
    q = request.args.get("q")
    res = []
    if q: res = search_db(q)
    return render_template("index.html", query=q, results=res)

@app.route("/click/<int:doc_id>")
def click(doc_id):
    with sqlite3.connect("index.db") as conn:
        c = conn.cursor()
        c.execute("UPDATE docs SET clicks = clicks + 1 WHERE id = ?", (doc_id,))
        path = c.execute("SELECT path FROM docs WHERE id = ?", (doc_id,)).fetchone()[0]
        conn.commit()
    return f"<script>window.open('/static/{path}','_blank');history.back();</script>"

@app.route("/ai_search")
def ai_search():
    from agent_search import agentic_search
    q = request.args.get("q")
    res = []
    if q: res = agentic_search(q)
    return render_template("index.html", query=q, results=res)

if __name__ == "__main__":
    app.run(debug=True)
