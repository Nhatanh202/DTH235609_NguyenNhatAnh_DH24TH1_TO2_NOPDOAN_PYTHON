import mysql.connector

def connect():
    try:
        ketnoi = mysql.connector.connect(
            host = " ",
            user = " ",
            password = " ",
            database=" "
        )
        return ketnoi
            print ("Lỗi kết nối đến database: {err}")
        return None
