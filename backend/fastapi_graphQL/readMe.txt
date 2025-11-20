pip install -r requirements.txt

실행 방법
uvicorn main:app --reload --port 3001

Query 쿼리
query {
    employees {
        id
        name
        age
        job
        language
        pay
    }
}

Mutation 쿼리
POST 방식
mutation {
    createEmployee(
        input: {
            name: "Taylor"
            age: 29
            job: "backend"
            language: "python"
            pay: 410
        }
    ) {
        id
        name
        age
        job
        language
        pay
    }
}

PUT 방식
mutation {
    updateEmployee(
        id: "2"
        input: {
            name: "Peter"
            age: 30
            job: "backend"
            language: "java"
            pay: 350
        }
    ) {
        id
        name
        age
        job
        language
        pay
    }
}

DELETE 방식
mutation {
    deleteEmployee(id: "3")
}