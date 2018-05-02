import sqlite3

conn = sqlite3.connect('test.db')
print ("Opened database successfully")

# conn.execute('''CREATE TABLE WALLET
#          (id INT PRIMARY KEY     NOT NULL,
#          balance        INT    NOT NULL,
#          coin_symbol    TEXT     NOT NULL)''')
# print ("Table created successfully")

# conn.execute("INSERT INTO WALLET (id, balance, coin_symbol) VALUES (?,?,?)" , (1233445665353,5,"FOO_COIN") )

# conn.commit()
# print ("Records created successfully")


cursor = conn.execute("SELECT id, balance, coin_symbol from WALLET")
for row in cursor:
   print ("id = ", row[0])
   print ("balance = ", row[1])
   print ("coin_symbol = ", row[2], "\n")

print ("Operation done successfully")
conn.close()