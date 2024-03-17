# import sqlite3
#
# db = sqlite3.connect('bolt.db')
# cur = db.cursor()
# query = "SELECT COUNT(*) FROM (SELECT 0 FROM pin_info LIMIT 1)"
# query_1 = "SELECT * FROM pin_info"
# query_2 = "SELECT * FROM bolt_info WHERE thread_id==10"
# query_bolt_parameters = """SELECT thread, type, stud_square, sigma_t, bolt_count
#            FROM bolt_info
#            INNER JOIN bolt_thread ON bolt_info.thread_id=bolt_thread.id
#            INNER JOIN bolt_class ON bolt_info.class_id=bolt_class.id
#            INNER JOIN bolt_type ON bolt_info.bolt_type=bolt_type.id
#            """
# query_resin_chock_parameters = """SELECT resin_name, weight_load, total_load, friction_ratio, density
#             FROM resin_type WHERE resin_name='EPY'"""
# query_pin = "SELECT * FROM pin_info"
# query_resin_chocks_static_load = """SELECT value
#            FROM result_info WHERE description='Нагрузка на полимер от веса оборудования'"""
# cur.execute(query_bolt_parameters)
# res = cur.fetchall()
# print(res)
#
# res = list(map(list, res))
# while sum(blt[2] for blt in res) > 200:
#     for i in res:
#         i[2] *= 0.95
# print(res)

# import pprint
# import openpyxl as op

# filename = 'Ответы.xlsx'
# wb = op.load_workbook(filename, data_only=True)
# sheet = wb.active
#
# max_rows = sheet.max_row
#
# d = {}
# for i in range(2, max_rows + 1):
#     question = sheet.cell(row=i, column=2).value
#     answer = sheet.cell(row=i, column=3).value
#     if question not in d:
#         d[question] = [answer]
#     else:
#         if answer not in d.values():
#             d[question].append(answer)
#         else:
#             continue
#
# n = 0
# for i in d.items():
#     print(i)
