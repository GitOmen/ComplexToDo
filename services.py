from sqlalchemy import Column, TEXT, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SCHEDULED = 'Scheduled'
INPROGRESS = 'In Progress'
FINISHED = 'Finished'

Base = declarative_base()


class TaskDoesNotExistException(Exception):
    def __init__(self, id):
        super().__init__(f"Task with id '{id}' does not exist")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(TEXT(), nullable=False)
    status = Column(TEXT(), nullable=False, default=SCHEDULED)
    description = Column(TEXT(), nullable=True)

    def __repr__(self):
        return f"Task({self.to_dict()})"

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'status': self.status, 'description': self.description}


# connection
engine = create_engine('sqlite:///data.db')

# create metadata
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)


def must_get_task(session, id):
    task = session.query(Task).filter(Task.id == id).first()
    if task is None:
        raise TaskDoesNotExistException(id)
    return task


def add_to_list(data):
    try:
        with Session.begin() as session:
            task = Task(**data)
            session.add(task)
            session.flush()
            return task.to_dict()
    except Exception as e:
        print('Error: ', e)
        return None


def get_all_tasks():
    try:
        with Session.begin() as session:
            tasks = session.query(Task).all()
            return [task.to_dict() for task in tasks]
    except Exception as e:
        print('Error: ', e)
        return None


def get_task(id):
    with Session.begin() as session:
        task = must_get_task(session, id)
        return task.to_dict()


def update_task(id, data):
    status = data.get('status')
    name = data.get('name')
    description = data.get('description')
    if status is None:
        pass
    elif status.lower().strip() == 'scheduled':
        status = SCHEDULED
    elif status.lower().strip() == 'in progress':
        status = INPROGRESS
    elif status.lower().strip() == 'finished':
        status = FINISHED
    else:
        print("Invalid Status: " + status)
        return None

    with Session.begin() as session:
        task = must_get_task(session, id)

        if status is not None:
            task.status = status
        if name is not None:
            task.name = name
        if description is not None:
            task.description = description
        return task.to_dict()


def delete_task(id):
    with Session.begin() as session:
        task = must_get_task(session, id)
        session.delete(task)
