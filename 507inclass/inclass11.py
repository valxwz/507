
import sqlite3
import sys

conn = sqlite3.connect('Northwind_small.sqlite')
cur = conn.cursor()

statement='''SELECT o.Id,o.freight
from [Order] as o
Join Shipper as s
on o.ShipVia=s.id
where o.Freight>100 and s.CompanyName="Speedy Express"
'''


'''SELECT o.Id, o.ShippedDate,s.CompanyName,s.Phone
FROM [Order] AS o
  JOIN Shipper AS s
    ON o.ShipVia = s.Id
'''
cur.execute(statement)




for row in cur:
    print(row)

conn.close()