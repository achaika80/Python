from random import randint
import sqlite3
import sys
class CreditCard:
    
    def __init__(self):
        self.db_connection = sqlite3.connect('./card.s3db')
        self.cur = self.db_connection.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS card(ID INTEGER PRIMARY KEY, \
                        NUMBER TEXT, 
                        PIN text,
                        BALANCE INTEGER DEFAULT 0)''')
        self.id = 0
        self.number = ""
        self.pin = ""
        self.balance = 0

    def generate_acc_num(self):
        iin = "400000"
        acc_num = iin + str(randint(100000000, 999999999))
        return acc_num

    def checksum(self,acc_num):
        acc_num = list(map(int,acc_num))
        index = 0
        temp_acc_num = []
        for num in acc_num:
            if index % 2 == 0:
                temp_acc_num.append(num * 2)
                if temp_acc_num[index] - 9 > 0:
                    temp_acc_num[index] = temp_acc_num[index] - 9
            else:
                temp_acc_num.append(num)
            index += 1
        if sum(temp_acc_num) % 10 == 0:
            check_sum = 0
        else:
            check_sum = 10 - sum(temp_acc_num) % 10
        return str(check_sum)

    def generate_card_num(self,acc_num,check_sum):
        acc_num_str = ''.join([str(num) for num in acc_num])
        acc_num_str += check_sum
        return acc_num_str
    
    def generate_pin(self):
        return str(randint(1000, 9999))
    
    def add_new_card(self):
        account_number = self.generate_acc_num()
        checksum = self.checksum(account_number)
        self.number = self.generate_card_num(account_number, checksum)
        self.pin = self.generate_pin()
        self.cur.execute((f"INSERT INTO card (number, pin, balance) "
                          f"VALUES ('{self.number}', '{self.pin}', '{self.balance}')"))
        self.db_connection.commit()

    def test_card_number(self):
        account_number = self.number[0:15]
        checksum = self.number[-1]
        return (checksum == self.checksum(account_number))
    
    def get_balance(self):
        if self.pin and self.number:
            self.cur.execute((f"SELECT * FROM card WHERE number = '{self.number}'"
                              f"AND pin = '{self.pin}'"))
            result = self.cur.fetchone()
            if result:
                self.balance = result[3]
                return True
    
    def check_card(self):
        self.cur.execute((f"SELECT * FROM card WHERE number = '{self.number}'"))
        if self.cur.fetchone():
            return True

    def add_income(self,income):
        self.balance += income
        self.cur.execute((f"UPDATE card SET BALANCE = '{self.balance}'"
                          f"WHERE NUMBER = '{self.number}'"))
        self.db_connection.commit()
        return True

    def transfer(self,money,dest_card_number):
        self.balance -= money
        self.cur.execute((f"UPDATE card SET BALANCE = '{self.balance}'"
                          f"WHERE NUMBER = '{self.number}'"))
        self.cur.execute((f"UPDATE card SET BALANCE = BALANCE + '{money}'"
                          f"WHERE NUMBER = '{dest_card_number}'"))
        self.db_connection.commit()
        return True

    def close_account(self):
        self.cur.execute((f"DELETE FROM card WHERE number = '{self.number}'"
                          f"AND pin = '{self.pin}'"))
        self.db_connection.commit()
        return True


class OnlineBank:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = object.__new__(cls)
            return cls.instance

    def start_menu(self):
        self.card = CreditCard()
        choice = input("1. Create an account\n2. Log into account\n0. Exit\n")
        self.start(choice)

    def start(self,choice):
        if choice == "1":
            self.add_new_account()
            self.start_menu()
        elif choice == "2":
            self.login()
            self.start_menu()
        elif choice == "0":
            sys.exit("\nBye!")
    
    def add_new_account(self):
        self.card.add_new_card()
        print("\nYour card has been created")
        print("Your card number:")
        print(f"{self.card.number}")
        print("Your card PIN:")
        print(f"{self.card.pin}\n")

    def login(self):
        self.card.number = input("Enter your card number:")
        self.card.pin = input("Enter your PIN:")
        if self.card.get_balance():
            print("\nYou have successfully logged in!\n")
            self.card_menu()
        else:
            print("\nWrong card number or PIN!\n")
            self.start_menu()

    def card_menu(self):
        choice = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit \n")
        self.card_operations(choice)

    def card_operations(self,choice):
        if choice == "1":
            print(f"\nBalance: {self.card.balance}\n")
            self.card_menu()
        elif choice == "2":
            self.add_income()
            self.card_menu()
        elif choice == "3":
            self.do_transfer()
            self.card_menu()
        elif choice == "4":
            self.close_account()
            self.start_menu()
        elif choice == "5":
            print("\nYou have successfully logged out!\n")
            self.start_menu()
        elif choice == "0":
            self.start(choice)

    def add_income(self):
        income = int(input("\nEnter income:"))
        if self.card.add_income(income):
            print("Income was added!\n")
   
    def do_transfer(self):
        print("\nTransfer")
        dest_card = CreditCard()
        dest_card.number = input("Enter card number:")
        if self.card.number == dest_card.number:
            print("You can't transfer money to the same account!\n")
            self.card_menu()
        if not dest_card.test_card_number():
            print("Probably you made a mistake in the card number. Please try again!\n")
            self.card_menu()
        elif not dest_card.check_card():
            print("Such a card does not exist.")
            self.card_menu()
        else:
            money = int(input("Enter how much money you want to transfer:"))
            if self.card.balance < money:
                print("Not enough money!\n")
                self.card_menu()
            else:
                if self.card.transfer(money,dest_card.number):
                    print("Success!\n")
    
    def close_account(self):
        if self.card.close_account():
            print("\nThe account has been closed!\n")
    
bank = OnlineBank()
bank.start_menu()


        




