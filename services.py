from enum import Enum

from sqlalchemy import Column, TEXT, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Status(Enum):
    SCHEDULED = 'SCHEDULED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'


class InvalidStatusException(Exception):
    def __init__(self, status):
        super().__init__(f"Status '{status}' is invalid")


class TaskDoesNotExistException(Exception):
    def __init__(self, id):
        super().__init__(f"Task with id '{id}' does not exist")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(TEXT(), nullable=False)
    status = Column(TEXT(), nullable=False, default=Status.SCHEDULED.value)
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


def parse_status(s):
    if s is None:
        return None
    try:
        return Status(s)
    except ValueError:
        raise InvalidStatusException(s)


def add_task(data):
    parse_status(data.get('status'))
    with Session.begin() as session:
        task = Task(**data)
        session.add(task)
        session.flush()
        return task.to_dict()


def get_all_tasks():
    with Session.begin() as session:
        tasks = session.query(Task).all()
        return [task.to_dict() for task in tasks]


def get_task(id):
    with Session.begin() as session:
        task = must_get_task(session, id)
        return task.to_dict()


def update_task(id, data):
    status = parse_status(data.get('status'))
    name = data.get('name')
    description = data.get('description')

    with Session.begin() as session:
        task = must_get_task(session, id)

        if status is not None:
            task.status = status.value
        if name is not None:
            task.name = name
        if description is not None:
            task.description = description
        return task.to_dict()


def delete_task(id):
    with Session.begin() as session:
        task = must_get_task(session, id)
        session.delete(task)
