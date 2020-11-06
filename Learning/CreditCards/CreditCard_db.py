from random import randint
import sqlite3
class CreditCard:
    iin = "400000"
    db_connection = sqlite3.connect('./card.s3db')

    def __init__(self):
        self.cur = CreditCard.create_db_and_table()
        self.card = dict()
        self.card['iin'] = CreditCard.iin
        self.card['account_number'] = self.generate_acc_num()
        self.card['check_sum'] = self.checksum(self.card['account_number'])
        self.card['pin'] = str(randint(1000, 9999))
        self.card['number'] = self.generate_card_num(self.card['account_number'],self.card['check_sum'])
        self.card['balance'] = 0
        self.cur.execute((f"INSERT INTO card (number, pin, balance) "
                     f"VALUES ('{self.card['number']}', '{self.card['pin']}', '{self.card['balance']}')"))
        CreditCard.db_connection.commit()

    @staticmethod
    def create_db_and_table():
        cur = CreditCard.db_connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS card(ID INTEGER PRIMARY KEY, \
                            NUMBER TEXT, 
                            PIN text,
                            BALANCE INTEGER DEFAULT 0)''')
        return cur

    def get_pin(self):
        return self.card['pin']
    
    def get_number(self):
        return self.card['number']
    
    def generate_acc_num(self):
        iin = "400000"
        acc_num = list(map(int, iin + str(randint(100000000, 999999999))))
        return acc_num

    def checksum(self,acc_num):
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
    
class OnlineBank:
    instance = None
    db_connection = sqlite3.connect('./card.s3db') 
    cur = CreditCard.create_db_and_table()

    def __new__(cls):
        if not cls.instance:
            cls.instance = object.__new__(cls)
            return cls.instance

    def start_menu(self):
        choice = input("1. Create an account\n2. Log into account\n0. Exit\n")
        self.start(choice)

    def start(self,choice):
        if choice == "1":
            self.add_new_account()
            self.start_menu
        elif choice == "2":
            self.login()
            self.start_menu
        elif choice == "0":
            print("\nBye!")
    
    def add_new_account(self):
        self.newcard = CreditCard()
        print("\nYour card has been created")
        print("Your card number:")
        print(f"{self.newcard.get_number()}")
        print("Your card PIN:")
        print(f"{self.newcard.get_pin()}\n")
        self.start_menu()

    def convert_row_to_dict(self,query):
        self.desc = OnlineBank.cur.description
        self.keys = [self.col[0] for self.col in self.desc]
        self.rows = []
        for self.row in query:
            self.rows.append(self.row)
        return dict(zip(self.keys,self.rows))

    def add_income(self, card):
        self.income = input("\nEnter income:")
        OnlineBank.cur.execute((f"UPDATE card SET balance = balance + '{self.income}'"
                                f"WHERE NUMBER = '{card['NUMBER']}'"))
        OnlineBank.db_connection.commit()
        OnlineBank.cur.execute((f"SELECT * FROM card WHERE NUMBER = '{card['NUMBER']}'"))
        print("Income was added")
        return self.convert_row_to_dict(OnlineBank.cur.fetchone())
        
    def login(self):
        self.card_number = input("Enter your card number:")
        self.pin = input("Enter your PIN:")
        self.card = self.find_card(self.card_number,self.pin)
        if self.card:
            print("\nYou have successfully logged in!\n")
            self.card_menu(self.card)
        else:
            print("\nWrong card number or PIN!\n")
            self.start_menu()


    def find_card(self,card_number,pin):
        OnlineBank.cur.execute((f"SELECT * FROM card WHERE number = '{card_number}'"
                                f"AND pin = '{pin}'"))
        return self.convert_row_to_dict(OnlineBank.cur.fetchone())

    def card_menu(self,card):
        choice = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit \n")
        self.card_operations(choice,card)
    
    def card_operations(self,choice,card):
        if choice == "1":
            print(f"\nBalance: {card['BALANCE']}\n")
            self.card_menu(card)
        elif choice == "2":
            self.card = self.add_income(card)
            self.card_menu(self.card)

        elif choice == "5":
            print("\nYou have successfully logged out!\n")
            self.start_menu()
        elif choice == "0":
            self.start(choice)


bank = OnlineBank()
bank.start_menu()




        


