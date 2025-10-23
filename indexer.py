import os, re, sqlite3, pdfplumber, pytesseract
from PIL import Image

DB = "index.db"

def create_tables():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS docs(
            id INTEGER PRIMARY KEY,
            path TEXT,
            text TEXT,
            clicks INT DEFAULT 0,
            folder1 TEXT,
            folder2 TEXT,
            folder3 TEXT
        )
        """)
        conn.commit()

def ensure_columns():
    """Add folder1/folder2/folder3 columns if they don't exist (safe to run)."""
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("PRAGMA table_info(docs)")
        cols = [row[1] for row in c.fetchall()]
        for col in ("folder1","folder2","folder3"):
            if col not in cols:
                try:
                    c.execute(f"ALTER TABLE docs ADD COLUMN {col} TEXT")
                except Exception:
                    pass
        conn.commit()

def extract_text(file_path):
    text = ""
    if file_path.lower().endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.lower().endswith((".jpg", ".png")):
        text = pytesseract.image_to_string(Image.open(file_path))
    else:
        try:
            text = open(file_path, encoding="utf-8").read()
        except:
            text = open(file_path, errors="ignore").read()
    return re.sub(r'\s+', ' ', text)

def index_folder(folder):
    import time
    create_tables()
    ensure_columns()
    print(f"Indexing folder: {folder}")
    started = time.time()
    total = 0
    processed = 0
    errors = 0
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        if not os.path.exists(folder):
            print(f"Warning: folder '{folder}' does not exist. Skipping.")
            return
        # Walk recursively and process files
        for root, dirs, files in os.walk(folder):
            # sort to make order deterministic
            dirs.sort()
            files.sort()
            if files:
                print(f"Entering directory: {root} (contains {len(files)} files)")
            for fname in files:
                total += 1
                p = os.path.join(root, fname)
                try:
                    print(f"Processing: {p}")
                    # skip if already indexed
                    c.execute("SELECT 1 FROM docs WHERE path=? LIMIT 1", (p,))
                    if c.fetchone():
                        print(f"Already indexed, skipping: {p}")
                        continue
                    txt = extract_text(p)
                    # compute up to 3 folder levels relative to base folder
                    rel = os.path.relpath(p, start=folder)
                    parts = rel.split(os.sep)
                    folder1 = parts[0] if len(parts) > 1 else (parts[0] if len(parts) == 1 else None)
                    folder2 = parts[1] if len(parts) > 2 else None
                    folder3 = parts[2] if len(parts) > 3 else None
                    c.execute(
                        "INSERT INTO docs(path,text,folder1,folder2,folder3) VALUES(?,?,?,?,?)",
                        (p, txt, folder1, folder2, folder3)
                    )
                    processed += 1
                except Exception as e:
                    errors += 1
                    print(f"Error processing {p}: {e}")
        conn.commit()
    took = time.time() - started
    print(f"Done. total={total} processed={processed} errors={errors} time={took:.2f}s")

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else "Input_Filings"
    index_folder(folder)
    print("✅ Indexing complete.")
