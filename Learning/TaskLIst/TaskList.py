from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
import sys

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class TasksTable(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key = True)
    task = Column(String, default = 'Task # ' + str(id))
    deadline = Column(Date, default = datetime.today().date())

    def __repr__(self):
        return self.task
    
class ManageTasks:
    
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self):
        Base.metadata.create_all(engine)
        self.task_menu()
        

    def task_menu(self):
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Add task")
        print("0) Exit")
        choice = input("")
        
        if choice == "1":
            self.get_today_tasks()
        elif choice == "2":
            self.weeks_tasks()
        elif choice == "3":
            self.get_all_tasks()
        elif choice == "4":
            self.add_task()
        elif choice == "0":
            sys.exit("\nBye!")

    def get_task_by_date(self, tasks_date):
        tasks = self.session.query(TasksTable).filter(TasksTable.deadline == tasks_date).all()
        return tasks

    def get_today_tasks(self):
        tasks = self.get_task_by_date(datetime.today().date())
        #tasks = self.session.query(TasksTable).all()
        print(f"\nToday {datetime.today().date().day} {datetime.today().date().strftime('%b')}:")
        if not tasks:
            print("Nothing to do!\n")
        else:
            n = 1
            for task in tasks:
                print(f"{n}. {task.task}")
                n += 1
            print("")
        self.task_menu()

    def weeks_tasks(self):
        today = datetime.today().date()
        for delta in range(7):
            tasks_date = (today + timedelta(days=delta))
            tasks = self.get_task_by_date(tasks_date)
            n = 1
            print(f"\n{tasks_date.strftime('%A')} {tasks_date.day} {tasks_date.strftime('%b')}:")
            if not tasks:
                print("Nothing to do!")
            else:
                for task in tasks:
                    print(f"{n}. {task.task}")
                    n += 1
        print("")
        self.task_menu()
        

    def get_all_tasks(self):
        tasks = self.session.query(TasksTable).all()
        print("\nAll tasks:")
        for task in tasks:
            print(f"{task.id}. {task.task} {task.deadline.day} {task.deadline.strftime('%b')}")
        print("")
        self.task_menu()

    def add_task(self):
        task_text = input("\nEnter task\n")
        task_deadline = datetime.strptime(input("Enter deadline\n"),'%Y-%m-%d')
        new_task = TasksTable(task = task_text, deadline = task_deadline)
        self.session.add(new_task)
        self.session.commit()
        print("The task has been added!\n")
        self.task_menu()

tasks = ManageTasks()

