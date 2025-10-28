import pyodbc

def connect():
    try:
        ketnoi = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=172.18.180.173;"
            "DATABASE=QUANLYCUAHANGXEMAY;"
            "UID=sa;"
            "PWD=sql2022;"
        )
        print("✅ Kết nối SQL Server thành công!")
        return ketnoi
    except Exception as e:
        print("❌ Lỗi khi kết nối:", e)
        return None


# --- Thử chạy ---
conn = connect()

if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")  # Lấy danh sách database trên SQL Server
    print("\n📋 Danh sách database trên SQL Server:")
    for row in cursor:
        print(" -", row[0])
    conn.close()
