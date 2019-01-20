import alchemy as db
import xlrd

dataset = []
workbook = xlrd.open_workbook("C:\\Users\\aimer\\Desktop\\news_keyword.xlsx")
table = workbook.sheets()[0]

set = dict()
m = 0
for row in range(1,table.nrows):
    row = table.row_values(row)
    row[0] = int(row[0])
    row[1] = int(row[1])
    if row[0] in set.keys():
        set[row[0]].append(row[1])
    else:
        set[row[0]] = [row[1]]
xx = len(set.keys())
for key,value in set.items():
    m = m + 1
    print(str(m) + "/" + str(xx))
    try:
        x = db.db_session.query(db.News).filter(db.News.id == key).first()
        y = []
        for i in value:
            y.append(db.db_session.query(db.Keyword).filter(db.Keyword.id == i).first())
        x.keywords = y
        db.db_session.commit()
    except:
        continue




