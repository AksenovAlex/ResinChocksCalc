import sqlite3

bolt_info_create_table = """CREATE TABLE "bolt_info"(
    "id" INTEGER NOT NULL,
    "thread_id" INTEGER NOT NULL,
    "class_id" INTEGER NOT NULL, 
    "bolt_count" TEXT NOT NULL,
    "bolt_hold" TEXT NOT NULL,
    "bolt_type" INTEGER NOT NULL,
    FOREIGN KEY("bolt_type") REFERENCES "bolt_type"("id") ON DELETE SET NULL,
    FOREIGN KEY("bolt_count") REFERENCES "bolt_class"("id") ON DELETE SET NULL,
    FOREIGN KEY("class_id") REFERENCES "bolt_thread"("id") ON DELETE SET NULL,
    PRIMARY KEY("id" AUTOINCREMENT))"""

bolt_info_delete_table = """DELETE FROM 'bolt_info'"""
resin_chock_info_delete_table = """DELETE FROM 'resin_chock_info'"""
pin_info_delete_table = """DELETE FROM 'pin_info'"""
result_info_delete_table = """DELETE FROM 'result_info'"""

select_all_result_info_table = 'SELECT * FROM result_info'
