# app_graphql/mutations.py
import strawberry


@strawberry.type
class Mutation:
    # 동작 확인용 Mutation (실제 DB 변경 없음)
    @strawberry.mutation
    def ping(self) -> str:
        return "pong"