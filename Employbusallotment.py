import mysql.connector as mys

#connection to bus database
print("hiiiii")
myconn=mys.connect(
    host='localhost',
    username='root',
    password='msmani@1980',
    database='empbus'
)

if(myconn.is_connected()):
    print("Successfully connected to database")
else:
    print("There is a problem is connection to database....")
#------------------------------------------------------------
cursor=myconn.cursor()
def checkbus(pp,en,ei):            #function for checking avalible bus for exitsing pickup point
    cursor.execute("SELECT busppid, busrno FROM buspp WHERE buspp = %s", (pp,))    #getting busno,bus pickup point id form buspp table
    data=cursor.fetchall()
    for row in data:
        cursor.execute("select busstrenght from bus where busno=%s",(row[1],))     #getting no of seats in bus for bus table
        no=cursor.fetchall()
        tablename=row[1]
        query=f"select count(*) from {tablename}"             #count no of seats occupied in bus
        cursor.execute(query)
        bn=cursor.fetchall()
        t=list(no[0])                                                                #converting tuple to list
        s=list(bn[0])
        if(s[0]>=t[0]):                                                              #checking which bus has seat using number seats available
            continue
        else:
            cursor.execute("INSERT INTO employ(empid, empname, emppup) VALUES (%s, %s, %s)", (ei, en, row[0]))  #inseting emp's setails into table(emly for bus)
            table_name=row[1]
            query = f"INSERT INTO `{table_name}` (empidb,emppp) VALUES (%s, %s)"
            cursor.execute(query, (ei, row[0]))

            print("added successfull bus no:",row[1])             #print alloted bus for employ

            myconn.commit()
            break


#getting  new employ's details for office bus
empname=input("Enter Employ's Name: ") 
empid=input("Enter Employ's ID: ")
cursor.execute("select DISTINCT buspp from buspp")
data=cursor.fetchall()
for row in data:
    print(row)

empPICKUPpoint=input("Enter Employ's Pickup Point from the list: ")       #getting pickup point prefered by employ form existsing pickuppoint
checkbus(empPICKUPpoint,empname,empid) #calling function