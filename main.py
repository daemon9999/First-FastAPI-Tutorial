from fastapi import FastAPI, Depends
import schemas 


from models import Item

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



app = FastAPI()

fakeDatabase = {
    1: {'task': 'Clean car'},
    2: {'task': 'Write Blog'},
    3: {'task': 'Start stream'}
}

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(Item).all()
    return items


@app.get("/{id}")
def getItem(id: int, session: Session = Depends(get_session)):
    item = session.query(Item).get(id)
    return item


#Option 1
# @app.post("/")
# def addItem(task: str):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {"task": task}
#     return fakeDatabase


#Option 2
@app.post("/")
def addItem(item: schemas.Item, session: Session = Depends(get_session)):
    item = Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)

    return item

@app.put("/{id}")
def updateItem(id: int, item: schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(Item).get(id)
    itemObject.task = item.task
    session.commit()
    
    return itemObject
    
@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    itemObject = session.query(Item).get(id)
    session.delete(itemObject)
    session.commit()
    
    return "Item was deleted"