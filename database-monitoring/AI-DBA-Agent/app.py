import os
import re
import logging
from typing import TypedDict

from dotenv import load_dotenv
import mysql.connector

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()

MASTER_IP = os.getenv("MASTER_IP")
SLAVE_IP = os.getenv("SLAVE_IP")

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# LLM
# =========================================================

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0
)

# =========================================================
# MYSQL CONNECTION
# =========================================================

def mysql_conn(host):

    return mysql.connector.connect(
        host=host,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        connection_timeout=5
    )

# =========================================================
# AUTO LOAD TABLES
# =========================================================

def load_tables():

    try:

        conn = mysql_conn(MASTER_IP)

        cursor = conn.cursor()

        cursor.execute("SHOW TABLES")

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [x[0] for x in rows]

    except Exception as e:

        logger.error(f"Gagal load tables: {e}")

        return []

COLLECTION_TABLES = load_tables()

# =========================================================
# FORMATTER
# =========================================================

def format_rows(rows):

    if not rows:
        return "Tidak ada data."

    output = []

    for idx, row in enumerate(rows, 1):

        output.append(f"{idx}. {row}")

    return "\n".join(output)

# =========================================================
# STATE
# =========================================================

class AgentState(TypedDict, total=False):

    input: str
    intent: str
    table: str
    target_node: str
    response: str

# =========================================================
# EXTRACT TABLE
# =========================================================

def extract_table(user_input):

    text = user_input.lower()

    for table in COLLECTION_TABLES:

        if table.lower() in text:
            return table

    return None

# =========================================================
# DETECT INTENT
# =========================================================

def detect_intent(user_input):

    text = user_input.lower()

    intents = {

        "latest_data": [
            "data terakhir",
            "latest",
            "terakhir"
        ],

        "show_data": [
            "tampilkan data",
            "show data",
            "lihat data",
            "select"
        ],

        "table": [
            "tampilkan tabel",
            "show tables",
            "list table",
            "daftar tabel"
        ],

        "users": [
            "daftar user",
            "list user",
            "show user",
            "tampilkan user"
        ],

        "permission": [
            "grant",
            "permission",
            "privilege"
        ],

        "online_user": [
            "online",
            "processlist",
            "user online"
        ],

        "replication": [
            "replikasi",
            "replication",
            "slave",
            "replica status"
        ],

        "slow_query": [
            "slow query",
            "query lama",
            "load",
            "performa",
            "performance",
            "optimasi"
        ]
    }

    for intent, keywords in intents.items():

        if any(k in text for k in keywords):
            return intent

    return "unknown"

# =========================================================
# ROUTER
# =========================================================

def router_node(state: AgentState):

    user_input = state["input"]

    intent = detect_intent(user_input)

    table = extract_table(user_input)

    # =====================================================
    # TARGET HOST
    # =====================================================

    target_node = "master"

    if "slave" in user_input.lower():
        target_node = "slave"

    logger.info({
        "intent": intent,
        "table": table,
        "target_node": target_node
    })

    # =====================================================
    # CATEGORY
    # =====================================================

    if intent in [
        "replication",
        "slow_query",
        "online_user"
    ]:

        category = "dba"

    elif intent in [
        "latest_data",
        "show_data"
    ] and table:

        category = "da"

    elif intent in [
        "table",
        "users",
        "permission"
    ]:

        category = "de"

    else:

        category = "de"

    return {
        "category": category,
        "intent": intent,
        "table": table,
        "target_node": target_node
    }

# =========================================================
# DB ENGINEER NODE
# =========================================================

def db_engineer_node(state: AgentState):

    logger.info("[DB ENGINEER NODE]")

    try:

        conn = mysql_conn(MASTER_IP)

        cursor = conn.cursor()

        # =================================================
        # SHOW TABLES
        # =================================================

        if state["intent"] == "table":

            cursor.execute("SHOW TABLES")

            rows = cursor.fetchall()

            tables = [x[0] for x in rows]

            cursor.close()
            conn.close()

            return {
                "response": (
                    f"\n[DB ENGINEER]\n\n"
                    f"Database : {DB_NAME}\n"
                    f"Total Table : {len(tables)}\n\n"
                    + format_rows(tables)
                )
            }

        # =================================================
        # USERS
        # =================================================

        if state["intent"] == "users":

            cursor.execute("""
            SELECT User, Host
            FROM mysql.user
            """)

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            return {
                "response": (
                    "\n[DB ENGINEER]\n\n"
                    "Daftar User Database:\n\n"
                    + format_rows(rows)
                )
            }

        # =================================================
        # PERMISSION
        # =================================================

        if state["intent"] == "permission":

            cursor.execute("""
            SELECT User, Host
            FROM mysql.user
            """)

            users = cursor.fetchall()

            output = []

            for user, host in users:

                try:

                    cursor.execute(
                        f"SHOW GRANTS FOR '{user}'@'{host}'"
                    )

                    grants = cursor.fetchall()

                    output.append(
                        f"\nUSER : {user}@{host}"
                    )

                    for g in grants:

                        output.append(f"  - {g[0]}")

                except Exception as e:

                    output.append(
                        f"\nUSER : {user}@{host}"
                    )

                    output.append(
                        f"  - ERROR : {str(e)}"
                    )

            cursor.close()
            conn.close()

            return {
                "response": (
                    "\n[DB ENGINEER]\n"
                    + "\n".join(output)
                )
            }

        cursor.close()
        conn.close()

        return {
            "response": (
                "\n[DB ENGINEER]\n\n"
                "Command tidak dikenali."
            )
        }

    except Exception as e:

        logger.error(e)

        return {
            "response": (
                f"\n[DB ENGINEER ERROR]\n\n{str(e)}"
            )
        }

# =========================================================
# DATA ANALYST NODE
# =========================================================

def data_analyst_node(state: AgentState):

    logger.info("[DATA ANALYST NODE]")

    table = state.get("table")
    intent = state.get("intent")

    if not table:

        return {
            "response": (
                "\n[DATA ANALYST]\n\n"
                "Table tidak ditemukan."
            )
        }

    # =====================================================
    # TARGET HOST
    # =====================================================

    host = MASTER_IP

    if state.get("target_node") == "slave":
        host = SLAVE_IP

    try:

        conn = mysql_conn(host)

        cursor = conn.cursor(dictionary=True)

        # =================================================
        # DATA TERAKHIR
        # =================================================

        if intent == "latest_data":

            query = f"""
            SELECT *
            FROM {table}
            ORDER BY 1 DESC
            LIMIT 5
            """

        # =================================================
        # SHOW DATA
        # =================================================

        elif intent == "show_data":

            query = f"""
            SELECT *
            FROM {table}
            LIMIT 10
            """

        else:

            return {
                "response": (
                    "\n[DATA ANALYST]\n\n"
                    "Intent data tidak dikenali."
                )
            }

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if not rows:

            return {
                "response": (
                    f"\n[DATA ANALYST]\n\n"
                    f"Tabel '{table}' kosong."
                )
            }

        # =================================================
        # AI SUMMARY
        # =================================================

        summary_prompt = f"""
        Analisa data database berikut.

        HOST : {host}
        TABLE : {table}

        Fokus:
        - jumlah data
        - pola penting
        - anomaly jika ada

        Maksimal 5 kalimat.

        DATA:
        {rows[:5]}
        """

        summary = llm.invoke(summary_prompt).content

        # =================================================
        # RAW DATA
        # =================================================

        raw_output = []

        for idx, row in enumerate(rows, 1):

            raw_output.append(f"{idx}. {row}")

        return {
            "response": (
                f"\n[DATA ANALYST]\n\n"
                f"HOST  : {host}\n"
                f"TABLE : {table}\n"
                f"ROWS  : {len(rows)}\n\n"
                f"SUMMARY:\n{summary}\n\n"
                f"RAW DATA:\n\n"
                + "\n".join(raw_output)
            )
        }

    except Exception as e:

        logger.error(e)

        return {
            "response": (
                f"\n[DATA ANALYST ERROR]\n\n{str(e)}"
            )
        }

# =========================================================
# DBA NODE
# =========================================================

def dba_technical_node(state: AgentState):

    logger.info("[DBA NODE]")

    try:

        # =================================================
        # REPLICATION
        # =================================================

        if state["intent"] == "replication":

            conn = mysql_conn(SLAVE_IP)

            cursor = conn.cursor(dictionary=True)

            try:

                cursor.execute("SHOW SLAVE STATUS")

            except:

                cursor.execute("SHOW REPLICA STATUS")

            row = cursor.fetchone()

            cursor.close()
            conn.close()

            if not row:

                return {
                    "response": (
                        "\n[DBA]\n\n"
                        "Replica tidak ditemukan."
                    )
                }

            io_running = row.get("Slave_IO_Running")
            sql_running = row.get("Slave_SQL_Running")
            delay = row.get("Seconds_Behind_Master")

            status = (
                "SEHAT"
                if io_running == "Yes"
                and sql_running == "Yes"
                else "BERMASALAH"
            )

            return {
                "response": (
                    "\n[DBA REPLICATION]\n\n"
                    f"Status          : {status}\n"
                    f"IO Running      : {io_running}\n"
                    f"SQL Running     : {sql_running}\n"
                    f"Delay           : {delay} second\n"
                    f"Master Host     : {row.get('Master_Host')}"
                )
            }

        # =================================================
        # PROCESSLIST
        # =================================================

        if state["intent"] == "online_user":

            conn = mysql_conn(MASTER_IP)

            cursor = conn.cursor()

            cursor.execute("""
            SELECT
                ID,
                USER,
                HOST,
                DB,
                COMMAND,
                TIME,
                STATE
            FROM information_schema.processlist
            WHERE COMMAND != 'Sleep'
            ORDER BY TIME DESC
            LIMIT 10
            """)

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            return {
                "response": (
                    "\n[DBA PROCESSLIST]\n\n"
                    + format_rows(rows)
                )
            }

        # =================================================
        # PERFORMANCE
        # =================================================

        if state["intent"] == "slow_query":

            conn = mysql_conn(MASTER_IP)

            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
            SELECT
                ID,
                USER,
                HOST,
                DB,
                TIME,
                STATE,
                INFO
            FROM information_schema.processlist
            WHERE COMMAND='Query'
            AND TIME > 3
            ORDER BY TIME DESC
            LIMIT 10
            """)

            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            if not rows:

                return {
                    "response": (
                        "\n[DBA PERFORMANCE]\n\n"
                        "Tidak ditemukan slow query.\n"
                        "Database dalam kondisi sehat."
                    )
                }

            analysis_prompt = f"""
            Analisa slow query berikut.

            Berikan:
            - apakah perlu optimasi
            - kemungkinan bottleneck
            - rekomendasi index/query

            Maksimal 7 kalimat.

            DATA:
            {rows}
            """

            analysis = llm.invoke(analysis_prompt).content

            return {
                "response": (
                    "\n[DBA PERFORMANCE]\n\n"
                    f"{analysis}\n\n"
                    "SLOW QUERY:\n\n"
                    + format_rows(rows)
                )
            }

        # =================================================
        # DEFAULT HEALTH
        # =================================================

        conn = mysql_conn(MASTER_IP)

        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.processlist
        WHERE TIME > 10
        AND COMMAND='Query'
        """)

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        health = (
            "SEHAT"
            if total == 0
            else f"TERDAPAT {total} LONG QUERY"
        )

        return {
            "response": (
                "\n[DBA HEALTH]\n\n"
                f"Status Database : {health}"
            )
        }

    except Exception as e:

        logger.error(e)

        return {
            "response": (
                f"\n[DBA ERROR]\n\n{str(e)}"
            )
        }

# =========================================================
# GRAPH
# =========================================================

workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("de", db_engineer_node)
workflow.add_node("da", data_analyst_node)
workflow.add_node("dba", dba_technical_node)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    lambda x: x["category"],
    {
        "de": "de",
        "da": "da",
        "dba": "dba"
    }
)

workflow.add_edge("de", END)
workflow.add_edge("da", END)
workflow.add_edge("dba", END)

app = workflow.compile()

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AI DATABASE ENGINEER ASSISTANT")
    print("=" * 60)

    while True:

        try:

            user_input = input("\n[USER]: ")

            if user_input.lower() in [
                "exit",
                "quit"
            ]:
                break

            result = app.invoke({
                "input": user_input
            })

            print(result["response"])

        except KeyboardInterrupt:
            break

        except Exception as e:

            print(f"\n[SYSTEM ERROR]\n{str(e)}")
