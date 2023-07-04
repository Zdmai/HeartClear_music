from sqlalchemy import create_engine
from sqlalchemy import text
# 数据库的配置变量

engine = create_engine(DB_URI)
#创建连接
with engine.connect() as con:
    rs = con.execute('SELECT 1')
    print(rs.fetchone())