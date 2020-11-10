from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
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
        print("2) Add task")
        print("0) Exit")
        choice = input("")
        
        if choice == "1":
            self.get_tasks_by_date(datetime.today().date())
        elif choice == "2":
            self.add_task()
        elif choice == "0":
            print("\nBye!")


    def get_tasks_by_date(self,tasks_date):
        tasks = self.session.query(TasksTable).filter(TasksTable.deadline == tasks_date).all()
        #tasks = self.session.query(TasksTable).all()
        cur_date = tasks_date
        if(tasks_date == datetime.today().date()):
            cur_date = "Today"
        print(f'{cur_date}: ')
        if not tasks:
            print("Nothing to do!\n")
        else:
            for task in tasks:
                print(f"{task.id}. {task.task}")
            print("")
        self.task_menu()

    def add_task(self):
        task_text = input("Enter task\n")
        new_task = TasksTable(task = task_text)
        self.session.add(new_task)
        self.session.commit()
        print("The task has been added!\n")
        self.task_menu()


tasks = ManageTasks()

