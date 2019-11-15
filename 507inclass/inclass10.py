
import sqlite3

conn = sqlite3.connect('Northwind_small.sqlite')
cur = conn.cursor()


# statement5 = 'SELECT CompanyName '
# statement5 += 'FROM Customer '
# statement5 += 'WHERE Region!="North America"'
# cur.execute(statement5)

# not_NA_company=[]

# for row in cur:
#     not_NA_company.append(row[0])

# print (not_NA_company)


statement6 = 'SELECT FirstName '
statement6 += 'FROM Employee '
statement6 += 'WHERE BirthDate LIKE "198%"'
cur.execute(statement6)

emp198=[]

for row in cur:
    emp198.append(row[0])

print (emp198)

# statement1 = 'SELECT CompanyName '
# statement1 += 'FROM Customer '
# statement1 += 'WHERE Region="Western Europe"'
# cur.execute(statement1)

# we_company=[]

# for row in cur:
#     we_company.append(row[0])

# # print ("Comanies in Western Europe: ", we_company)

# statement2 = 'SELECT ProductName '
# statement2 += 'FROM Product '
# statement2 += 'WHERE UnitsInStock=0'

# cur.execute(statement2)

# discontinued_units=[]
# for row in cur:
#     discontinued_units.append(row)

# # print ("discontinued_units:", discontinued_units)

# statement3 = 'SELECT LastName, FirstName '
# statement3 += 'FROM Employee '
# statement3 += 'WHERE ReportsTo=2'

# cur.execute(statement3)

# employee=[]
# for row in cur:
#     employee.append(row)
# # print (employee)




# statement4 = 'SELECT OrderDate, ShippedDate '
# statement4 += 'FROM [Order] '
# statement4 += 'WHERE ShipCountry="USA"'

# cur.execute(statement4)

# order=[]
# for row in cur:
#     order.append(row)
#     # print ("order date:",row[0],"ship date",row[1])

# cur.execute('SELECT CompanyName, Id from Customer where Id="ALFKI"')
# com=cur.fetchall()
# cur.execute('SELECT Id from Customer where id="ALFKI"')
# for em in com:
# 	print (em)

conn.close()