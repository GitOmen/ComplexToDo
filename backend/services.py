from enum import Enum
from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import Column, TEXT, create_engine, Integer, ForeignKey
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Status(Enum):
    SCHEDULED = 'SCHEDULED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'

    @classmethod
    def parse(cls, s):
        if s is None:
            return None
        try:
            return Status(s)
        except ValueError:
            raise InvalidStatusException(s)


class InvalidStatusException(Exception):
    def __init__(self, status):
        super().__init__(f"Status '{status}' is invalid")


class TaskDoesNotExistException(Exception):
    def __init__(self, id):
        super().__init__(f"Task with id '{id}' does not exist")


class TaskListDoesNotExistException(Exception):
    def __init__(self, id):
        super().__init__(f"Task List with id '{id}' does not exist")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(TEXT(), nullable=False)
    status = Column(TEXT(), nullable=False, default=Status.SCHEDULED.value)
    description = Column(TEXT(), nullable=True)
    list_id = Column(Integer, ForeignKey('task_lists.id', ondelete='CASCADE'), nullable=False)
    list = relationship("TaskList", back_populates="tasks")

    def __repr__(self):
        return f"Task({self.to_dict()})"

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'status': self.status, 'description': self.description,
                'list': self.list.to_dict()}


class TaskList(Base):
    __tablename__ = 'task_lists'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(TEXT(), nullable=False)
    tasks = relationship("Task", back_populates="list", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f"TaskList({self.to_dict()})"

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


engine = create_engine('sqlite:///data.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
# https://stackoverflow.com/questions/57726047/sqlalchemy-expression-language-and-sqlites-on-delete-cascade
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def _fetch_task(session, id):
    task = session.query(Task).filter(Task.id == id).first()
    if task is None:
        raise TaskDoesNotExistException(id)
    return task


def _fetch_task_list(session, id):
    task_list = session.query(TaskList).filter(TaskList.id == id).first()
    if task_list is None:
        raise TaskListDoesNotExistException(id)
    return task_list


def add_task(data):
    Status.parse(data.get('status'))
    with Session.begin() as session:
        _fetch_task_list(session, data.get('list_id'))
        task = Task(**data)
        session.add(task)
        session.flush()
        return task.to_dict()


def get_all_tasks(list_id=None):
    with Session.begin() as session:
        query = session.query(Task)
        if list_id is not None:
            query = query.filter(Task.list_id == list_id)
        tasks = query.all()
        return [task.to_dict() for task in tasks]


def get_task(id):
    with Session.begin() as session:
        task = _fetch_task(session, id)
        return task.to_dict()


def update_task(id, data):
    with Session.begin() as session:
        task = _fetch_task(session, id)

        if status := Status.parse(data.get('status')):
            task.status = status.value
        if name := data.get('name'):
            task.name = name
        if description := data.get('description'):
            task.description = description
        if list_id := data.get('list_id'):
            _fetch_task_list(session, list_id)
            task.list_id = list_id
        return task.to_dict()


def delete_task(id):
    with Session.begin() as session:
        task = _fetch_task(session, id)
        session.delete(task)


def add_task_list(data):
    with Session.begin() as session:
        task_list = TaskList(**data)
        session.add(task_list)
        session.flush()
        return task_list.to_dict()


def get_all_task_lists():
    with Session.begin() as session:
        task_lists = session.query(TaskList).all()
        return [_list.to_dict() for _list in task_lists]


def get_task_list(id):
    with Session.begin() as session:
        task_list = _fetch_task_list(session, id)
        return task_list.to_dict()


def update_task_list(id, data):
    with Session.begin() as session:
        task_list = _fetch_task_list(session, id)

        if name := data.get('name'):
            task_list.name = name
        return task_list.to_dict()


def delete_task_list(id):
    with Session.begin() as session:
        task_list = _fetch_task_list(session, id)
        session.delete(task_list)
