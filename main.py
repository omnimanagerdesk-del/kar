from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI()

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
email TEXT,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY,
title TEXT,
assigned_to TEXT,
status TEXT
)
""")

conn.commit()


class User(BaseModel):
    email:str
    password:str


class Task(BaseModel):
    title:str
    assigned_to:str


@app.post("/register")
def register(user:User):

    cursor.execute(
        "INSERT INTO users(email,password) VALUES(?,?)",
        (user.email,user.password)
    )

    conn.commit()

    return {"message":"user created"}



@app.post("/login")
def login(user:User):

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (user.email,user.password)
    )

    data = cursor.fetchone()

    if data:
        return {"status":"success"}

    return {"status":"fail"}



@app.post("/add_task")
def add_task(task:Task):

    cursor.execute(
        "INSERT INTO tasks(title,assigned_to,status) VALUES(?,?,?)",
        (task.title,task.assigned_to,"pending")
    )

    conn.commit()

    return {"message":"task added"}



@app.get("/tasks")
def get_tasks():

    cursor.execute("SELECT * FROM tasks")

    data = cursor.fetchall()

    return data



@app.post("/complete/{task_id}")
def complete(task_id:int):

    cursor.execute(
        "UPDATE tasks SET status='done' WHERE id=?",
        (task_id,)
    )

    conn.commit()

    return {"message":"task completed"}
