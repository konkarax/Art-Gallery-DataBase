import sqlite3
import datetime
import SQLite_CreateTables
import SQLite_InsertData

def print_action():
    print("\nSelect your action:")
    print("0:CRUD Operations")
    print("1:See which artwork is under maintenance at a specific date")
    print("2:See the exhibitions in a specific date")
    print("3:See which artworks are borrowed to an external institution")
    print("4:Issue a ticket") 
    print("5:Send an artwork to an external institution")
    print("6:Request an artwork from an external institution")
    print("7:Send an artwork to a maintenance lab")
    

def print_selection():
    print("\nSelect the table you want to search:")

def print_tables():
    print("\nARTWORK, ARTIST, BORROWS_FROM, BORROWS_TO, CONDUCTS, EMPLOYEE")
    print("EMPLOYEE_MAINTENANCE, EXHIBITION, EXTERNAL_INSTITUTION")
    print("HALL, MAINTENANCE, TICKET, TICKET_CONTAINS")

def print_attribute():
    print("\nSelect attribute of table:")
    print("To see the attributes of the table press '0'")

def select_correct_table():
    while(True):
        table=input()
        try:
            cursor.execute("SELECT * FROM "+table)
        except:
            print("Table is invalid")
            continue
        break
    return table

def select_correct_attribute():
    while(True):
        attribute=input()
        try:
            cursor.execute("SELECT "+attribute+" FROM "+table)
        except:
            print("Attribute name was invalid")
            continue   
        break
    return attribute
    

def show_attribute(table):
    if (table=='EXHIBITION'):
        print('ID,Title,Cost,Date_Import,Date_Export,Periodical')
    elif (table=='HALL'):
        print('ID,Area,Floor,Wing,Capacity,ID_Exhibition')
    elif (table=='ARTIST'):
        print('ID,Biography,Gender,Year_of_death,Year_of_birth,Place_of_birth,First_Name,Middle_Name,Last_Name,Nickname')
    elif (table=='ARTWORK'):
        print('ID,Title,Material,Dimensions,Type,Year_of_creation,Description,Current_of_influence,ID_Exhibition,ID_Hall,ID_Artist')
    elif (table=='TICKET'):
        print('ID,Date_issuing,Date_expiring,Price,Buyer,Multiplicity,Discount,Time_of_arrival')
    elif (table=='TICHET_CONTAINS'):
        print('ID_Ticket,ID_Exhibition')
    elif (table=='EXTERNAL_INSTITUTION'):
        print('ID,Name,Date_arrangment,Date_borrowing,Date_return,Contract')
    elif (table=='BORROWS_FROM' or table=='BORROWS_TO'):
        print('ID_Artwork,ID_Borrowing')
    elif (table=="EMPLOYEE"):
        print("VAT,Email,Gender,Job_position,Salary,Name,Middle_Name,Last_Name,Contact_number,VAT_Supervisor")
    elif (table=='EMPLOYEE_MAINTENANCE'):
        print('VAT, Specialty')
    elif (table=='MAINTENANCE'):
        print('ID_Artwork,Lab,Date_import,Expected_date_export,Date_export,VAT_Supervisor')
    elif (table=='CONDUCTS'):
        print('ID_Artwork,VAT')

        
def check_date(date):
    date_format ='%Y-%m-%d'
    try:
        dateObject = datetime.datetime.strptime(date, date_format)
        return True
    except:
        return False

def check_time(time):
    time_format ='%H:%M:%S'
    try:
        dateObject = datetime.datetime.strptime(time, time_format)
        return True
    except:
        return False

def check_available(date,art):
    not_available=[]
    cursor.execute("SELECT ID_Artwork FROM MAINTENANCE WHERE Date_import<date('"+date+"') AND\
                    (Date_export IS NULL OR Date_export>date('"+date+"'))")
    for row in cursor:
        not_available.append(row[0])
    cursor.execute("SELECT B.ID_Artwork FROM BORROWS_TO AS B, EXTERNAL_INSTITUTION AS E \
                    WHERE E.ID=B.ID_Borrowing AND E.Date_borrowing<date('"+date+"') AND (Date_return IS NULL OR Date_return>date('"+date+"'))")
    for row in cursor:
        not_available.append(row[0])
    if int(art) in not_available:
        return False
    return True
    
    

conn =sqlite3.connect("DBGallery.db")
conn.execute("PRAGMA foreign_keys = ON;") #Δημιουργούνται περιορισμοί με τα ξένα κλειδιά
cursor= conn.cursor()
print("----------Gallery Data Base----------")

print_action()
select=input()
while(select!='exit'):
    if (select=='0'):
        print("Select Operation:")
        print("1:Create")
        print("2:Read")
        print("3:Upate")
        print("4:Delete")
        operation=input()
        if (operation=='1'):
            print_tables()
            print("\nSelect the table you want to create a new row:")
            table=select_correct_table()
            cursor.execute("PRAGMA table_info("+table+")")
            for row in cursor:
                print(row)
            print("\nEnter your data (eg 356178210,'konstantinos.karax@gmail.com','Αρσενικό','Ξεναγός',6000,'Κωνσταντίνος',NULL,'Καραχάλιος',6986694778,NULL)")
            while(True):
                try:
                    data=input()
                    conn.execute("INSERT INTO "+table+" VALUES("+data+");")
                    conn.commit()
                except:
                    print("Invalid data")
                    continue
                break
            print("Data has been added to the database")   
        elif (operation=='2'):
            print_tables()
            print("Select the table you want to read")
            table=select_correct_table()
            show_attribute(table)
            attribute=select_correct_attribute()
            cursor.execute("SELECT "+attribute+" FROM "+table)
            for row in cursor:
                print(row)
        elif (operation=='3'):
            print_tables()
            print("Select the table you want to update")
            table=select_correct_table()
            show_attribute(table)
            while(True):
                print("\nSelect the row you want to update")
                print("e.g. VAT=356178210")
                condition=input()
                print("\nWhat do you want to update (eg VAT_Supervisor=723466902)")
                update=input()
                try:
                    conn.execute("UPDATE "+table+" SET "+update+" WHERE "+condition+";")
                    conn.commit()
                except:
                    print("Invalid update")
                    continue
                break
            print("Value has been updated")
        elif (operation=='4'):
            print_tables()
            print("Select the table from where you want to delete")
            table=select_correct_table()
            show_attribute(table)
            while(True):
                print("Which rows do you want to delete?")
                print("e.g. VAT=356178210")
                delete=input()
                try:
                    conn.execute("DELETE FROM "+table+" WHERE "+delete+";")
                    conn.commit()
                except:
                    print("Invalid delete")
                    continue
                break
            print("Row has been deleted")
                
            
            
    elif(select=='1'):
        while(True):
            print("Select your date")
            print("Select 'now' for today's date or write your date in the form of YYYY-MM-DD")
            date=input()
            flag=check_date(date)
            if (flag==True or date=='now'):
                cursor.execute("SELECT A.ID,A.Title,M.Date_import,M.Expected_date_export,M.Date_export\
                                FROM ARTWORK AS A, MAINTENANCE AS M\
                                WHERE M.ID_Artwork=A.ID AND date('"+date+"')>M.Date_import AND \
                                     (M.Date_export IS NULL OR M.Date_export>date('"+date+"'))")
                for row in cursor:
                    print(row)
            else:
                print("Invalid date")
                continue
            break
    elif(select=='2'):
        while(True):
            print("Select your date")
            print("Select 'now' for today's date or write your date in the form of YYYY-MM-DD")
            date=input()
            flag=check_date(date)
            if (flag==True or date=='now'):
                cursor.execute("SELECT ID,Title\
                               FROM EXHIBITION\
                               WHERE date('"+date+"')>Date_Import AND(Periodical=0 OR (Periodical=1 AND date('"+date+"')<Date_Export)")
                for row in cursor:
                    print(row)
            else:
                print("Invalid date")
                continue
            break
    elif (select=='3'):
         while(True):
            print("Select your date")
            print("Select 'now' for today's date or write your date in the form of YYYY-MM-DD")
            date=input()
            flag=check_date(date)
            if (flag==True or date=='now'):
                cursor.execute("SELECT A.ID,A.Title,EX.Date_borrowing,EX.Date_return\
                                FROM EXTERNAL_INSTITUTION as EX, ARTWORK as A,BORROWS_TO as B\
                                WHERE EX.ID=B.ID_Borrowing AND B.ID_Artwork=A.ID AND date('"+date+"')<EX.Date_return")
                for row in cursor:
                    print(row)
                break
            else:
                print("Invalid date")
            break
    
    elif (select=='4'):
        while(True):
            print("Select your date (eg 2022-01-04)")
            print("Select 'now' for today's date or write your date in the form of YYYY-MM-DD")
            date=input()
            flag=check_date(date)#Έλεγχος format ημερομηνίας
            print("Select time (eg 11:30:00)")
            print("08:00:00, 08:30:00, 09:00:00, 09:30:00, 10:00:00, 10:30:00, 11:00:00, 11:30:00")
            print("12:00:00, 12:30:00, 13:00:00, 13:30:00, 14:00:00, 14:30:00, 15:00:00, 15:30:00")
            time=input()
            flag2=check_time(time) #Έλεγχος format χρόνου
            if (flag==True or date=='now') and flag2==True :
                #Άθροισμα όλων των εισητηρίων ανά αίθουσα για συγκεκριμένη στιγμή
                cursor.execute("SELECT SUM(T.Multiplicity),H.ID_Exhibition,H.ID,H.Capacity\
                                FROM TICKET as T, TICKET_CONTAINS as TC, HALL as H\
                                WHERE T.Date_issuing='"+date+" "+time+"' AND T.ID=TC.ID_Ticket AND TC.ID_Exhibition=H.ID_Exhibition\
                                GROUP BY H.ID")
                for row in cursor:
                    print(row)

                while(True):
                    print("How many tickets do you want to issue")
                    num=int(input())
                    if num=='':
                        break
                    print("Select the exhibitions you want to visit: (eg 120,300,400,500,6783)")
                    exhibition=input()
                    #Βάση των εκθέσεων που έχω επιλέξει αναγνωρίζω τις αίθουσες που θα κλείσω
                    ex_split=exhibition.split(",")
                    halls=[]
                    for ex in ex_split:
                        cursor.execute("SELECT H.ID FROM HALL AS H WHERE H.ID_Exhibition="+ex+"")
                        for hall in cursor:
                            halls.append(int(hall[0]))
                    cursor.execute("SELECT SUM(T.Multiplicity),H.ID,H.Capacity\
                                    FROM TICKET as T, TICKET_CONTAINS as TC, HALL as H\
                                    WHERE T.Date_issuing='"+date+" "+time+"' AND T.ID=TC.ID_Ticket AND TC.ID_Exhibition=H.ID_Exhibition\
                                    GROUP BY H.ID")
                    flag_ticket=True
                    for row in cursor:
                        if row[1] in halls:
                            if (row[0]+num>row[2]):
                                print("Not enough available tickets")
                                flag_ticket=False
                                break
                    if flag_ticket==False:
                        continue
                    cursor.execute("SELECT ID FROM TICKET")
                    for row in cursor:
                        continue
                    ID=row[0]+1
                    print("Insert name")
                    name=input()
                    if name=='':
                        name='NULL'
                    print("Insert discount: 0, 0.25, 0.5, 1")
                    discount=float(input())
                    value=0
                    for ex in ex_split:
                        value+=2
                        if ex=='6783':
                            value+=2
                    if len(ex_split)==5:
                        value-=2
                    value*=num
                    if discount!=0:
                        value*=(1-discount)
                    now=datetime.datetime.now()
                    now_time=now.strftime("%H:%M:%S")
                    print(ID,date,time,date,'20:00:00',value,name,num,discount,now_time)
                    conn.execute("INSERT INTO TICKET VALUES("+str(ID)+",'"+date+" "+time+"',\
                                    '"+date+" 20:00:00',"+str(value)+",'"+name+"',"+str(num)+","+str(discount)+",'"+now_time+"');")
                    for ex in ex_split:
                        print(ex)
                        conn.execute("INSERT INTO TICKET_CONTAINS VALUES("+str(ID)+","+ex+");")
                    conn.commit()
                    print("Ticket has been inserted succesfully to the database")
                    break
                    
                       
                break
            else:
                print("Invalid date")
            break
    elif(select=='5'):
        print(5)
    elif(select=='6'):
        print(6)
    elif(select=='7'):
        print("Select the artwork you want to send to maintenance: (eg 12031)")
        art=input()
        print("Select the date you want to send it (eg 2023-01-05)")
        date_send=input()
        if date_send=='now':
            date_send=now.strftime("%Y-%m-%d")
        flag=check_date(date_send)
        
        print("Select the approximate date you want to return (eg 2023-03-05)")
        date_r=input()
        if date_r=='now':
            date_r=now.strftime("%Y-%m-%d")
        flag2=check_date(date_r)
        while (flag and flag2 and check_available(date_send,art)==True):
            print("Select lab (Α1 Α2 Β1 Β2)")
            lab=input()
            cursor.execute("SELECT ID_Artwork FROM MAINTENANCE WHERE Lab='"+lab+"' AND (Date_export>'"+date_send+"' OR Date_export IS NULL)")
            temp=0
            for row in cursor:
                temp=row
            if temp==0:
                print("Select Supervisor: 411297822, 021132021, 099807807,151629092,131206401")
                supervisor=input()
                print("Select the employee that is going to conduct the maintenance")
                employee=input()
                conn.execute("INSERT INTO MAINTENANCE VALUES("+art+",'"+lab+"','"+date_send+"','"+date_r+"',NULL,"+supervisor+")")
                conn.execute("INSERT INTO CONDUCTS_MAINTENANCE VALUES("+art+","+employee+",'"+date_send+"')")
                conn.commit()
                print("Artwork has been send to maintenance")
                break
            else:
                print("This lab is occupied with another artwork this day")
        
    else:
        print("Selection was invalid")
    print_action()
    select=input()
            
print("Exiting data base...")
conn.close()



