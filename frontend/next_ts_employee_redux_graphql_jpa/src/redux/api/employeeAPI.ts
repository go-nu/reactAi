import axios from "axios";
import { createAsyncThunk } from "@reduxjs/toolkit";
import { EmployeeInfo } from "@/redux/slice/employeeSlice";

// FastAPI GraphQL 서버 주소 (uvicorn 기본 포트는 8000)
// 필요하면 본인 환경에 맞게 수정
const GRAPH_URL = "http://localhost:3001/graphql";

// 공통 GraphQL 응답 타입
type GraphQLResponse<T> = {
    data?: T;
    errors?: { message: string }[];
};

// =======================
// 1) GET: 전체 조회
// =======================
export const fetchGetEmployeeInfos = createAsyncThunk<
    EmployeeInfo[],
    void,
    { rejectValue: string }
>(
    "employeeApi/fetchGetEmployeeInfos",
    async (_, thunkAPI) => {
        const query = `
      query GetEmployees {
        employees {
          id
          name
          age
          job
          language
          pay
        }
      }
    `;

        try {
            const { data } = await axios.post<
                GraphQLResponse<{ employees: EmployeeInfo[] }>
            >(
                GRAPH_URL,
                { query },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            if (data.errors?.length) {
                console.error("GraphQL errors:", data.errors);
                return thunkAPI.rejectWithValue("GraphQL error");
            }

            if (!data.data) {
                return thunkAPI.rejectWithValue("응답 데이터가 없습니다.");
            }

            console.log(data.data);

            return data.data.employees;
        } catch (e) {
            console.error("Network error:", e);
            return thunkAPI.rejectWithValue("데이터 로드 실패");
        }
    }
);

// =======================
// 2) POST: 등록
// =======================
export const fetchPostEmployeeInfo = createAsyncThunk<
    EmployeeInfo,   // 성공 시 반환 타입
    EmployeeInfo,   // 호출 시 payload 타입
    { rejectValue: string }
>(
    "employeeApi/fetchPostEmployeeInfo",
    async (obj, thunkAPI) => {
        const mutation = `
      mutation CreateEmployee($input: EmployeeInput!) {
        createEmployee(input: $input) {
          id
          name
          age
          job
          language
          pay
        }
      }
    `;

        try {
            const { data } = await axios.post<
                GraphQLResponse<{ createEmployee: EmployeeInfo }>
            >(
                GRAPH_URL,
                {
                    query: mutation,
                    variables: {
                        input: {
                            name: obj.name,
                            age: Number(obj.age),
                            job: obj.job,
                            language: obj.language,
                            pay: Number(obj.pay),
                        },
                    },
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            if (data.errors?.length) {
                console.error("GraphQL errors:", data.errors);
                return thunkAPI.rejectWithValue("GraphQL error");
            }

            if (!data.data) {
                return thunkAPI.rejectWithValue("응답 데이터가 없습니다.");
            }

            const created = data.data.createEmployee;
            console.log("created employee:", created);
            return created;
        } catch (e) {
            console.error("Network error:", e);
            return thunkAPI.rejectWithValue("데이터 전송 실패");
        }
    }
);

// =======================
// 3) PUT: 수정
// =======================
export const fetchPutEmployeeInfoById = createAsyncThunk<
    EmployeeInfo,
    EmployeeInfo,
    { rejectValue: string }
>(
    "employeeApi/fetchPutEmployeeInfo",
    async (obj, thunkAPI) => {
        const mutation = `
      mutation UpdateEmployee($id: ID!, $input: EmployeeInput!) {
        updateEmployee(id: $id, input: $input) {
          id
          name
          age
          job
          language
          pay
        }
      }
    `;

        try {
            const { data } = await axios.post<
                GraphQLResponse<{ updateEmployee: EmployeeInfo }>
            >(
                GRAPH_URL,
                {
                    query: mutation,
                    variables: {
                        id: String(obj.id),
                        input: {
                            name: obj.name,
                            age: Number(obj.age),
                            job: obj.job,
                            language: obj.language,
                            pay: Number(obj.pay),
                        },
                    },
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            if (data.errors?.length) {
                console.error("GraphQL errors:", data.errors);
                return thunkAPI.rejectWithValue("GraphQL error");
            }

            if (!data.data) {
                return thunkAPI.rejectWithValue("응답 데이터가 없습니다.");
            }

            const updated = data.data.updateEmployee;
            console.log("updated employee:", updated);
            return updated;
        } catch (e) {
            console.error("Network error:", e);
            return thunkAPI.rejectWithValue("데이터 전송 실패");
        }
    }
);

// =======================
// 4) DELETE: 삭제
// =======================
export const fetchDeleteEmployeeInfoById = createAsyncThunk<
    number,   // 성공 시: 삭제한 id (number)
    number,   // 호출 시: id (number)
    { rejectValue: string }
>(
    "employeeApi/fetchDeleteEmployeeInfo",
    async (id, thunkAPI) => {
        const mutation = `
      mutation DeleteEmployee($id: ID!) {
        deleteEmployee(id: $id)
      }
    `;

        try {
            const { data } = await axios.post<
                GraphQLResponse<{ deleteEmployee: string }>
            >(
                GRAPH_URL,
                {
                    query: mutation,
                    variables: { id: String(id) },
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            if (data.errors?.length) {
                console.error("GraphQL errors:", data.errors);
                return thunkAPI.rejectWithValue("GraphQL error");
            }

            if (!data.data) {
                return thunkAPI.rejectWithValue("응답 데이터가 없습니다.");
            }

            // 서버는 ID(string)를 반환하지만, 우리는 호출한 number id를 그대로 돌려줌
            // slice에서 state.infos = infos.filter(e => e.id !== action.payload) 할 수 있게
            console.log("deleted employee id:", data.data.deleteEmployee);
            return id;
        } catch (e) {
            console.error("Network error:", e);
            return thunkAPI.rejectWithValue("데이터 전송 실패");
        }
    }
);
