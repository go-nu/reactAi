import strawberry
from typing import Optional, List
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from bson import ObjectId
from pymongo import MongoClient


# -----------------------------
# MongoDB 연결
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["employee_db"]
employee_collection = db["employees"]


# -----------------------------
# GraphQL 타입 선언
# -----------------------------
@strawberry.type
class Employee:
    id: strawberry.ID
    name: str
    age: int
    job: str
    language: str
    pay: int


@strawberry.input
class EmployeeInput:
    name: str
    age: int
    job: str
    language: str
    pay: int


# -----------------------------
# MongoDB → GraphQL 변환 도우미
# -----------------------------
def mongo_to_graphql(doc) -> Employee:
    return Employee(
        id=str(doc["_id"]),
        name=doc["name"],
        age=doc["age"],
        job=doc["job"],
        language=doc["language"],
        pay=doc["pay"]
    )


# -----------------------------
# Query
# -----------------------------
@strawberry.type
class Query:
    @strawberry.field
    def employees(self) -> List[Employee]:
        docs = employee_collection.find()
        return [mongo_to_graphql(doc) for doc in docs]


# -----------------------------
# Mutation
# -----------------------------
@strawberry.type
class Mutation:
    @strawberry.mutation
    def createEmployee(self, input: EmployeeInput) -> Employee:

        new_doc = {
            "name": input.name,
            "age": input.age,
            "job": input.job,
            "language": input.language,
            "pay": input.pay,
        }

        result = employee_collection.insert_one(new_doc)
        new_doc["_id"] = result.inserted_id

        return mongo_to_graphql(new_doc)

    @strawberry.mutation
    def updateEmployee(self, id: strawberry.ID, input: EmployeeInput) -> Employee:
        obj_id = ObjectId(str(id))

        doc = employee_collection.find_one({"_id": obj_id})
        if not doc:
            raise ValueError("Employee not found")

        updated_data = {
            "name": input.name,
            "age": input.age,
            "job": input.job,
            "language": input.language,
            "pay": input.pay,
        }

        employee_collection.update_one({"_id": obj_id}, {"$set": updated_data})

        updated_doc = employee_collection.find_one({"_id": obj_id})
        return mongo_to_graphql(updated_doc)

    @strawberry.mutation
    def deleteEmployee(self, id: strawberry.ID) -> strawberry.ID:
        obj_id = ObjectId(str(id))

        doc = employee_collection.find_one({"_id": obj_id})
        if not doc:
            raise ValueError("Employee not found")

        employee_collection.delete_one({"_id": obj_id})
        return strawberry.ID(str(obj_id))


# -----------------------------
# Schema & FastAPI 설정
# -----------------------------
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app = FastAPI()


# 샘플 데이터 초기화
def init_sample_data():

    if employee_collection.count_documents({}) > 0:
        return

    samples = [
        {"name": "John",  "age": 35, "job": "frontend",  "language": "react",      "pay": 400},
        {"name": "Peter", "age": 28, "job": "backend",   "language": "java",       "pay": 300},
        {"name": "Sue",   "age": 38, "job": "publisher", "language": "javascript", "pay": 400},
        {"name": "Susan", "age": 45, "job": "pm",        "language": "python",     "pay": 500},
    ]

    employee_collection.insert_many(samples)


@app.on_event("startup")
def startup_event():
    init_sample_data()


# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "FastAPI GraphQL + MongoDB Employee server running..."}

