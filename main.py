import random
import mysql.connector
from getpass import getpass

mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="admin")
cursor = mydb.cursor()
try:
    cursor.execute("USE mydb")
except:
    cursor.execute("CREATE DATABASE mydb")
    cursor.execute("USE mydb")

gpuList = ['Nvidia GT 710', 'Nvidia GTX 1050', 'Nvidia GTX 1650', 'Nvidia GTX 2070', 'Nvidia RTX 3050', 'Nvidia RTX 3070', 'Nvidia RTX 3090', 'AMD Radeon RX 6600 XT']
processorList = ['Intel Core i3-2100', 'Intel Core i3-4130', 'Intel Core i3-7100', 'Intel Core i5-7400', 'Intel Core i5-8600K', 'Intel Core i7-8700', "AMD Ryzen 7 5700"]
ramList = ['2 GB', '4 GB', '8 GB', '16 GB', '32 GB']

def register():
    create1 = '''CREATE TABLE IF NOT EXISTS Customers (
    phoneNumber integer(10) NOT NULL PRIMARY KEY,
    firstName varchar(12) NOT NULL,
    lastName varchar(12) NOT NULL,
    gender varchar(1) NOT NULL,
    registrationDate date NOT NULL
);'''
    cursor.execute(create1)
    mydb.commit()
    print('--------------------------------\n')
    fname=input("Enter FIRST NAME: ")
    lname=input("Enter LAST NAME: ")
    phone = int(input("Enter PHONE NUMBER : "))
    gender=input("Enter GENDER (M/F): ")
    if gender.lower() not in ['m','f']:
        raise Exception("Wrong gender format!")
    user={
    "phoneNumber": phone,
    "firstName": fname,
    "lastName": lname,
    "gender": gender.upper()
    }
    print()
    print("User Details: ", user)

    register1 = '''INSERT INTO Customers (phoneNumber, firstName, lastName, gender, registrationDate)
    VALUES ("%s", "%s", "%s", "%s", NOW());''' % (int(user['phoneNumber']), user["firstName"], user["lastName"], user["gender"])
    cursor.execute(register1)
    mydb.commit()
    print("You have successfully registered!")
    print()
    return user['phoneNumber']

def order(uID):

    pc={}
    print("CHOOSE PARTS FOR YOUR COMPUTER")
    print('--------------------------------\n')
    print('PROCESSOR')
    print('--------------------------------\n')
    for i in processorList:
        print(processorList.index(i) + 1, "- ", i)
    processor=int(input("Select: "))-1
    print('--------------------------------\n')
    print('Graphics Card')
    print('--------------------------------\n')
    for i in gpuList:
        print(gpuList.index(i) + 1, "- ", i)
    gpu=int(input("Select: "))-1
    print('--------------------------------\n')
    print('RAM')
    print('--------------------------------\n')
    for i in ramList:
        print(ramList.index(i) + 1, "- ", i)
    ram=int(input("Select: "))-1
    p=processorList[processor]
    g=gpuList[gpu]
    r=ramList[ram]
    ad=input("Enter address: ")
    cursor.execute('INSERT INTO Orders (phoneNumber, processor, gpu, ram, address, orderDate) VALUES (%s, "%s", "%s", "%s", "%s", NOW())' % (uID, p, g, r, ad))
    mydb.commit()
    print()
    print("Processing your order...")
    print("------------------")
    print("Order placed!")
    print("------------------")
    main()

def admin_portal():
    password="pc123"
    p=getpass(prompt="Enter password: ")
    if p==password:
        print("======== Logged in to admin portal ========")
        optt=input("Select from the below menu:\n1. Delete order\n2. Print list of current orders\n3. Print list of users\nSelect: ")
        if optt=="1":
            ph=input("Enter phone number of order to delete: ")
            cursor.execute("""SELECT * FROM Customers WHERE phoneNumber=""" + ph)
            values=cursor.fetchall()
            if (len(values) > 0):
                print("Found phone number ", ph, " in db!")
            else:
                return print("Phone number not found!")
            cursor.execute("DELETE FROM Orders WHERE phoneNumber=" + ph)
            mydb.commit()
            print("Deleted order with the phone number '", ph, "' from db!")
            main()
        elif optt=="2":
            print()
            cursor.execute("""SELECT * FROM Orders""")
            a=cursor.fetchall()
            print("========================================================================")
            print("Phone No.  | Processor          | GPU             | Ram  | Address              | Transaction Date")
            for row in a:
                for element in row:
                    print(element, end = " | ")
                print('\n--------------------------------------------')
            print("========================================================================")
            main()
        elif optt=="3":
            cursor.execute("""SELECT * FROM Customers""")
            a=cursor.fetchall()
            print("========================================================================")
            print("Phone No. | First name  | Last name  | Ram  | Gender | Registration Date")
            for row in a:
                for element in row:
                    print(element, end = " | ")
                print('\n--------------------------------------------')
            print("========================================================================")
            main()
        else:
            return print("Invalid input")
    else:
        print("WRONG PASSWORD")

 # MAIN

uID = 0

def main():
    global uID

    print("""
  _____   _____      _____ _______ ____  _____  ______ 
 |  __ \ / ____|    / ____|__   __/ __ \|  __ \|  ____|
 | |__) | |        | (___    | | | |  | | |__) | |__   
 |  ___/| |         \___ \   | | | |  | |  _  /|  __|  
 | |    | |____     ____) |  | | | |__| | | \ \| |____ 
 |_|     \_____|   |_____/   |_|  \____/|_|  \_\______|
                                                       
""")

    print("WELCOME TO COMPUTER STORE\n\nOUR SERVICES:")
    print("""1 - Build a PC and order\n2 - View your order\n3 - Admin portal\n4 - Exit""")
    opt = input("\nChoose an option from the above menu: ")
    if opt in ['1', '2', '3', '4']:
        if uID==0 and opt=="1":
            print("----------------------------------------------")
            print("Not logged in, taking you to the login page...")
            q = input("Do you want to register a new account or login? (R/L): ")
            if q.lower() == "r":
                reg = register()
                if reg is not None:
                    uID=reg
                    main()
                else:
                    main()
            elif q.lower() == "l":
                loginID = input("Enter your phone number to login: ")
                login='SELECT phoneNumber FROM Customers WHERE phoneNumber='+loginID
                cursor.execute(login)
                numbers=cursor.fetchall()
                if (len(numbers)>0):
                    print("Logged in!")
                    uID = loginID
                    main()
                else:
                    print("Could not find that number!")
                    main()
        if opt == "1":
            print("You have selected 'Build a PC and order'")
            print()
            return order(uID)

        elif opt == "2":
            print("You have selected 'View your order'")
            print("")
            phone=input("Enter your phone number: ")
            cursor.execute("SELECT * FROM Orders WHERE phoneNumber=" + phone)
            a=cursor.fetchall()
            print()
            print("========================================================================")
            print("Phone No.  | Processor          | GPU             | Ram  | Address              | Transaction Date")
            for row in a:
                for element in row:
                    print(element, end = " | ")
                print()
            print("========================================================================")
            if (len(a) <= 0):
                return print("Not found")
            print()
            main()
        elif opt == "3":
            return admin_portal()
        elif opt == "4":
            print()
            print("Exiting menu, thank you!")
            print()
        else:
            print("Invalid input\n")
            main()

# TABLE CREATION (IF NOT EXISTS)

cursor.execute("""CREATE TABLE IF NOT EXISTS Customers (
    phoneNumber decimal(11) NOT NULL PRIMARY KEY,
    firstName varchar(12) NOT NULL,
    lastName varchar(12) NOT NULL,
    gender varchar(1) NOT NULL,
    registrationDate date NOT NULL
);
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Orders (
    phoneNumber decimal(11),
    processor varchar(25),
    gpu varchar(18),
    ram varchar(18),
    address varchar(40),
    orderDate date NOT NULL,
    FOREIGN KEY (`phoneNumber`) REFERENCES `Customers`(`phoneNumber`)
);
""")

main()
