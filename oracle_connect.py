import oracledb

user, password, host, port, service_name = "test", "test", "10.0.7.5", 1521, "kgcapp"
dsn = f"{host}:{port}/{service_name}"

try:
    conn = oracledb.connect(user=user, password=password, dsn=dsn)
    cursor = conn.cursor()

    cursor.execute("SELECT table_name FROM user_tables")
    print("테이블 목록:")
    for t in cursor.fetchall():
        print(t[0])

    cursor.execute("SELECT * FROM your_table_name WHERE ROWNUM <= 5")
    print("\n샘플 데이터:")
    for row in cursor.fetchall():
        print(row)

except oracledb.Error as e:
    print("오류 발생:", e)

finally:
    if 'conn' in locals():
        conn.close()
