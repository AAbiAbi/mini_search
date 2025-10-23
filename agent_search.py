import os
from app import search_db
import itertools
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"
os.environ["CURL_HTTP_VERSION"] = "1.1"

# Initialize Gemini
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)



def expand_queries_with_gemini(user_query):
    """Use Gemini to generate multiple keyword-style search queries.

    Returns a list of short (3-6 word) keyword queries, one per list item.
    """
    print("🧠 Step 1: entering expand_queries_with_gemini()")
    prompt = f"""
    You are a search query expansion agent.
    Based on the user's natural language input, generate 5 concise keyword-style search queries.
    Each query should be short (3–6 words), focused on key concepts, and output one per line.

    User query: "{user_query}"
    """
    print("🧠 Step 2: preparing model...")
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    try:
        print("🧠 Step 3: sending request to Gemini API...")
        response = model.generate_content(prompt, request_options={"timeout": 10})
        print("🧠 Step 4: got response!")
        text = response.text.strip()
        queries = [q.strip("-• ") for q in text.split("\n") if q.strip()]
        print("🧠 Gemini expansions:", queries)
        return queries
    except Exception as e:
        print("⚠️ Gemini API failed:", e)
        return []


def agentic_search(natural_query):
    """Main agentic search logic.

    1. Try to expand the user query with Gemini.
    2. If Gemini fails, fall back to a simple local synonym expansion.
    3. Call `search_db` for each expansion and merge/deduplicate results.
    4. Return the top 3 results by score.
    """
    print(f"🤖 Running agentic search for: {natural_query}")
    try:
        expansions = expand_queries_with_gemini(natural_query)
    except Exception as e:
        print("⚠️ Gemini API failed, fallback to local expansion:", e)
        expansions = []
        words = natural_query.lower().split()
        synonyms = {
            "california": ["california", "ca"],
            "nonrenewal": ["nonrenewal", "non-renewal", "policy cancellation"],
            "insurance": ["insurance", "policy"]
        }
        for w in words:
            expansions.append(synonyms.get(w, [w]))
        all_queries = [" ".join(c) for c in itertools.product(*expansions)]
        expansions = all_queries

    # Call the existing `search_db()` multiple times and merge results
    seen, results = set(), []
    for q in expansions:
        for s, rid, path, snippet, clicks in search_db(q)[:5]:
            if rid not in seen:
                seen.add(rid)
                results.append((s, rid, path, snippet, clicks))
    # Aggregate ranking and return top 3
    top = sorted(results, reverse=True)[:3]
    return top


if __name__ == "__main__":
    docs = agentic_search("California insurance nonrenewal rules")
    for score, rid, path, snippet, clicks in docs:
        print(f"⭐️ {path} (score={score:.2f}, clicks={clicks})")
        print(snippet[:200])
        print("-" * 80)
