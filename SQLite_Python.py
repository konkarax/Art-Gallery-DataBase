import sqlite3

def print_action():
    print("\nSelect your action:")
    print("0:CRUD Operations")
    print("1:See which artwork is under maintenance at a specific date")
    print("2:See the exhibitions in a specific date")
    print("3:See which artworks are borrowed to an external institution")

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
            print("\nEnter your data")
            while(True):
                try:
                    data=input()
                    conn.execute("INSERT INTO "+table+" VALUES("+data+");")
                    conn.commit()
                except:
                    print("Invalide data")
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
                print("What do you want to update")
                print("e.g. ID=12345, Name='test'")
                update=input()
                print("Select were you want to update")
                condition=input()
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
                print("e.g. ID=12345, Name='test'")
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
                cursor.execute("SELECT A.ID,A.Title FROM ARTWORK AS A, MAINTENANCE AS M WHERE M.ID_Artwork=A.ID AND\
                                date('"+date+"')>Date_import AND date('"+date+"')<Date_export)")
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
                cursor.execute("SELECT ID,Title FROM EXHIBITION WHERE (Periodical==0 AND date('"+date+"')>Date_Import) OR\
                                (Periodical==1 AND date('"+date+"')>Date_Import AND date('"+date+"')<Date_Export)")
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
                cursor.execute("SELECT A.ID,A.Title,EX.Date_borrowing,EX.Date_return FROM EXTERNAL_INSTITUTION as EX, ARTWORK as A,\
                                BORROWS_TO as B WHERE EX.ID=B.ID_Borrowing AND B.ID_Artwork=A.ID AND date('"+date+"')<EX.Date_return")
                for row in cursor:
                    print(row)
                break
            else:
                print("Invalid date")
            break
    else:
        print("Selection was invalid")
    print_action()
    select=input()
print("Exiting data base...")

conn.close()



