from sqlalchemy import Column, TEXT, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SCHEDULED = 'Scheduled'
INPROGRESS = 'In Progress'
FINISHED = 'Finished'

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'

    name = Column(TEXT(), primary_key=True, nullable=False)
    status = Column(TEXT(), nullable=False, default='Scheduled')

    def __repr__(self):
        return f"Task('{self.name}', '{self.status}')"


# connection
engine = create_engine('sqlite:///data.db')

# create metadata
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)


def add_to_list(task):
    try:
        # session = Session()
        with Session.begin() as session:
            session.add(Task(**task))
        # session.commit()
    except Exception as e:
        print('Error: ', e)
        return None


def get_all_tasks():
    try:
        # session = Session()
        with Session.begin() as session:
            tasks = session.query(Task.name, Task.status).all()
        # tasks = session.query(*Task.__table__.columns).all()
        return [dict(task) for task in tasks]
    except Exception as e:
        print('Error: ', e)
        return None


def get_task_status(task_name):
    try:
        with Session.begin() as session:
            task_status, = session.query(Task.status).filter(Task.name == task_name).first()
        return task_status
    except Exception as e:
        print('Error: ', e)
        return None


def update_status(task_name, status):
    if status.lower().strip() == 'scheduled':
        status = SCHEDULED
    elif status.lower().strip() == 'in progress':
        status = INPROGRESS
    elif status.lower().strip() == 'finished':
        status = FINISHED
    else:
        print("Invalid Status: " + status)
        return None

    try:
        with Session.begin() as session:
            task = session.query(Task).filter(Task.name == task_name).first()
            task.status = status

        return {task_name: status}
    except Exception as e:
        print('Error: ', e)
        return None


def delete_task(task_name):
    try:
        with Session.begin() as session:
            session.query(Task).filter(Task.name == task_name).delete()

        return {'task': task_name}
    except Exception as e:
        print('Error: ', e)
        return None
