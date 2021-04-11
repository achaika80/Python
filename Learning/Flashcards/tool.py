# write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
import sys

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')

Base = declarative_base()

class CardsTable(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String, default='Question # ' + str(id))
    answer = Column(String, default='Answer # ' + str(id))
    ranswern = Column(Integer, default=0)

    def __repr__(self):
        return self.task


class FlashCards:

    Session = sessionmaker(bind=engine)
    session = Session()

    card_session = 0

    def __init__(self):
        Base.metadata.create_all(engine)
        self.main_menu()


    def main_menu(self):
        print("1. Add flashcards")
        print("2. Practice flashcards")
        print("3. Exit")
        choice = input("")

        if choice == "1":
            self.add_cards_menu()
        elif choice == "2":
            self.practice_cards()
        elif choice == "3":
            print("\nBye!")
            sys.exit()
        else:
            print(f"{choice} is not an option")
            self.main_menu()

    def add_cards_menu(self):
        print("\n1. Add a new flashcard")
        print("2. Exit")
        choice = input("")

        if choice == "1":
            self.add_cards()
        elif choice == "2":
            self.main_menu()
        else:
            print(f"{choice} is not an option")
            self.add_cards_menu()

    def add_cards(self):
        q = ""
        while not q:
            q = input("Question:\n")
        a = ""
        while not a:
            a = input("Answer:\n")
        card = CardsTable(question=q, answer=a)
        self.session.add(card)
        self.session.commit()
        self.add_cards_menu()

    def practice_cards(self):
        prompt = ''
        if self.card_session == 0:
            cards = self.session.query(CardsTable).filter(CardsTable.ranswern == 0).all()
        elif self.card_session == 1:
            cards = self.session.query(CardsTable).filter(or_(CardsTable.ranswern == 0, CardsTable.ranswern == 1)).all()
        else:
            cards = self.session.query(CardsTable).all()
        if not cards:
            print("\nThere is no flashcard to practice!\n")
            self.main_menu()
        else:
            for card in cards:
                print(f"\nQuestion: {card.question}")
                prompt = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:')
                while prompt not in ['y', 'n', 'u']:
                    print(f"{prompt} is not an option")
                    prompt = input()
                if prompt == "y":
                    print(f"Answer: {card.answer}")
                    self.answer_menu(card)
                elif prompt == "n":
                    print('')
                    self.answer_menu(card)
                    continue
                elif prompt == "u":
                    self.update_cards(card)
        self.card_session += 1
        self.main_menu()

    def update_cards(self, card):
        prompt = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:')
        while prompt not in ['d', 'e']:
            print(f"{prompt} is not an option")
            prompt = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:')
        if prompt == 'd':
            self.session.delete(card)
            self.session.commit()
        elif prompt == 'e':
            print(f'\ncurrent question: {card.question}')
            q = ""
            while not q:
                q = input('please write a new question:')
            print(f'\ncurrent answer: {card.answer}')
            a = ""
            while not a:
                a = input('please write a new answer:')
            card.question = q
            card.answer = a
            self.session.commit()
        #self.practice_cards()

    def answer_menu(self, card):
        aprompt = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
        while aprompt not in ['y', 'n']:
            print(f"{aprompt} is not an option")
            aprompt = input()
        if aprompt == "y":
            card.ranswern += 1
            if card.ranswern >= 3:
                self.session.delete(card)
        else:
            card.ranswern = 0
        self.session.commit()


FlashCards()
