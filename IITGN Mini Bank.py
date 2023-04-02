from datetime import datetime
import time
import random
import mysql.connector as c

con = c.connect(host="localhost", user='root', passwd="1234", database="Bank_IITGN")
cursor = con.cursor()
con.autocommit = True

if con.is_connected():
    print("Succesfully Connected")
else:
    print("Error occured while connecting database")

list_of_account_holders = {"Mayur Patil": ["Your name:- Mayur Dnyaneshwar Patil", f"Your PAN Number:-GFR513TR65163",
                                           f"Your Account Number:-26565134515", f"Your PIN is 1567"]}
Bank_Balance = {26565134515: 3500}
Account_PIN = {26565134515: 1567}
Transaction_Details = {26565134515: []}


class CreateAccount():
    def __init__(self):
        self.name = input("What is your full name? ")
        self.pan = input("What is your PAN Number.? ")
        name = self.name
        pan = self.pan
        Account_No = int(random.random() * 1000000)
        __password1 = int(input("Please Set your Password:- "))
        __password2 = int(input("Please Re-enter your Password:- "))
        if __password2 == __password1:
            query1 = "insert into Account_Details values('{}',{},{},'{}',{});".format(name, pan, Account_No,
                                                                                      datetime.now(),
                                                                                      __password2)
            cursor.execute(query1)
            list_of_account_holders[
                self.name] = [f"Your name:-{self.name}", f"Your PAN Number:-{self.pan}",
                              f"Your Account Number:-{Account_No}", f"Your PIN is {__password2}",
                              f"Your Account created on {datetime.now()}"]
        else:
            print("Wrong Password")
            __password2 = int(input("Re-enter your password:- "))
            if __password2 == __password1:
                query1 = "insert into Account_Details values('{}',{},{},'{}',{});".format(name, pan, Account_No,
                                                                                          datetime.now(),
                                                                                          __password2)
                cursor.execute(query1)
                list_of_account_holders[
                    self.name] = [f"Your name:-{self.name}", f"Your PAN Number:-{self.pan}",
                                  f"Your Account Number:-{Account_No}", f"Your PIN is {__password2}"]
            else:
                print("Incorrect Password, Get Lost!!!!!")
                return None
        Bank_Balance[Account_No] = 0
        query2 = "insert into Bank_Balance values({},{});".format(Account_No, 0)
        cursor.execute(query2)
        Account_PIN[Account_No] = __password2
        Transaction_Details[Account_No] = []
        query3 = "insert into Transaction_Details values({},'{}');".format(Account_No, datetime.now())
        cursor.execute(query3)
        print("Creating your new Account.....")
        time.sleep(3)
        print(f"Your Bank Account has been successfully been created. Your Account Number is {Account_No}")


class CreditDebitAccount():
    def CreditInAccount(self):
        x = int(input("What is your Account Number? "))
        query4 = "select exists(select * from bank_balance where Account_No={});".format(x)
        cursor.execute(query4)
        y = cursor.fetchall()[0][0]
        if y == 1:
            query5 = "select Amount from bank_balance where Account_No={};".format(x)
            cursor.execute(query5)
            initial_amount = cursor.fetchall()[0][0]
            print("Your Initial Amount is ", initial_amount)
            Amount = int(input("Enter the Amount to be Credited:- "))
            new_amount = int(initial_amount) + Amount
            query6 = "update bank_balance set Amount={} where Account_No={};".format(new_amount, x)
            cursor.execute(query6)
            time.sleep(3)
            print(f"The amount has been successfully credited to your Account. Your current Balance is Rs.{new_amount}")
            query7 = "select Details from transaction_details where exists(select * from transaction_details where " \
                     "Account_No = {});".format(x)
            cursor.execute(query7)
            initial_details = []
            initial_details.append(cursor.fetchall()[0][0])
            initial_details.append([f"Amount credited:- {Amount} at {datetime.now()}"])
            print(initial_details)
        else:
            print("Your Account Doesn't Exist")

    def DebitFromAccount(self):
        s = int(input("What is your Account Number? "))
        query8 = "select exists(select * from bank_balance where Account_No={});".format(s)
        cursor.execute(query8)
        m = cursor.fetchall()[0][0]
        if m == 1:
            query9 = "select Amount from bank_balance where Account_No={};".format(s)
            cursor.execute(query9)
            initial_amount = cursor.fetchall()[0][0]
            print("Your Initial Amount is ", initial_amount)
            Amount = int(input("Enter the Amount to be Debited:- "))
            if Amount < int(initial_amount):
                u = int(input("Please enter your PIN:- "))
                query10 = f"select Pin from Account_Details where Account_No = {s};"
                cursor.execute(query10)
                n = cursor.fetchall()[0][0]
                print(n)
                if n == u:
                    final_amount = initial_amount - Amount
                    print("Please wait while your Transaction is Loading......")
                    time.sleep(3)
                    query11 = f"update Bank_Balance set Amount = {final_amount} where Account_No = {s};"
                    cursor.execute(query11)
                    ''' //////SOME ERROR EXISTS HERE\\\\\\'''
                    query12 = f"select Details from Transaction_Details where Account_No = {s};"
                    cursor.execute(query12)
                    temp_list = cursor.fetchall()[0][0]
                    print(temp_list)
                    temp_string = f"Amount debited:-{Amount} at {datetime.now()}"
                    new_string = temp_list+" "+temp_string
                    print(str(new_string))
                    query13 = f"update Transaction_Details set Details = '{new_string}' where Account_No={int(s)};"
                    cursor.execute(query13)
                    print(f"Amount Debited Successfully, Your current balance is {final_amount}")
                else:
                    print("!!!!!! Wrong PIN  !!!!!!!")
            else:
                print("You don't have sufficient balance!!!!")
        else:
            print("Your Account Doesn't exists.")


class GetDetails():
    def MyDetails(self):
        Account_No = int(input("Enter your Account number:- "))
        query14 = "select exists(select * from Account_Details where Account_No={});".format(Account_No)
        cursor.execute(query14)
        m = cursor.fetchall()[0][0]
        if m==1:
            print("Loading.......")
            time.sleep(3)
            query15 = "select * from Account_Details"
            cursor.execute(query15)
            temp_list = list(cursor.fetchall()[0])
            print(f"Name:- {temp_list[0]}, PAN_No:- {temp_list[1]},Account_No:- {temp_list[2]}, Account_Created_On:- {temp_list[3]}, PIN:- {temp_list[4]}")
        else:
            print("Your Account doesn't exist.....")

    def TransactionDetails(self):
        o = int(input("Enter your Account Number:- "))
        if o in Account_PIN.keys():
            w = int(input("Enter Your PIN:- "))
            if Account_PIN[o] == w:
                print("Loading.......")
                time.sleep(3)
                print(Transaction_Details[o])
            else:
                print("!!!!! Wrong PIN !!!!!!")
        else:
            print("Your Account doesn't exists....")


print("Welcome To the Bank of IIT Gandhinagar")
while True:
    i = int(input("Enter 1 to create an Account, Enter 2 to Credit or Debit an amount, Enter 3 to get your details "))
    if i == 1:
        CreateAccount()
    if i == 2:
        CreditDebitAccount()
        j = int(input("Enter 1 to credit and 2 to debit:- "))
        if j == 1:
            CreditDebitAccount.CreditInAccount(23)
        if j == 2:
            CreditDebitAccount.DebitFromAccount(23)
    if i == 3:
        GetDetails()
        e = int(input("Enter 1 to get your Personal Details or 2 to get your Transaction Details "))
        if e == 1:
            GetDetails.MyDetails(23)
        if e == 2:
            GetDetails.TransactionDetails(23)
    else:
        print("!!!!!! Please Enter valid Input !!!!!!")
