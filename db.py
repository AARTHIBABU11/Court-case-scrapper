import sqlite3
import os

DB_NAME = "court_data.db"

def init_db():
    """Initialize the database and create the table if it doesn't exist."""
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                filing_year TEXT,
                parties TEXT,
                filing_date TEXT,
                hearing_date TEXT,
                pdf_url TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        print("✅ Database initialized.")
    else:
        print("⚠️ Database already exists.")

def save_query(case_type, case_number, filing_year, data):
    """Save the query and parsed data to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO queries (case_type, case_number, filing_year, parties, filing_date, hearing_date, pdf_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        case_type,
        case_number,
        filing_year,
        data.get("parties", ""),
        data.get("filing_date", ""),
        data.get("hearing_date", ""),
        data.get("pdf_url", "")
    ))

    conn.commit()
    conn.close()
    print("✅ Query saved to database.")
