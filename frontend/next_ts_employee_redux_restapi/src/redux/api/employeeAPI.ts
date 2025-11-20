import axios from "axios";
import {createAsyncThunk} from "@reduxjs/toolkit";
import {EmployeeInfo} from "@/redux/slice/employeeSlice";


const API_URL = "http://localhost:3001";

// Get 전체 infos
export const fetchGetEmployeeInfos = createAsyncThunk<EmployeeInfo[], void, {rejectValue: string}>(
    "employeeApi/fetchGetEmployeeInfos",
    async (_, thunkAPI) =>{
        try {
            const response = await axios.get(`${API_URL}/app/emp`);
            console.log("get", response.data);
            return response.data;
        }catch{
            return thunkAPI.rejectWithValue("데이터 로드 실패");
        }
    }
);

export const fetchPostEmployeeInfo = createAsyncThunk<
    EmployeeInfo, EmployeeInfo, {rejectValue: string}>(
        "employeeApi/fetchPostEmployeeInfo",
        async (obj, thunkAPI) =>{
                try{
                    const response = await axios.post<EmployeeInfo>(`${API_URL}/app/emp`, obj);
                    console.log("obj", obj)
                    console.log("response", response);
                    return response.data; //action.payload
                }catch{
                      return thunkAPI.rejectWithValue("데이터 전송 실패")
                }
        }
)

// Delete  selectedId 기반
export const fetchDeleteEmployeeInfoById = createAsyncThunk<
    number, number, {rejectValue: string}
>(
    "employeeApi/fetchDeleteEmployeeInfoById",
    async (id, thunkAPI) => {
        try{
            await axios.delete(`${API_URL}/app/emp/${id}`)
            return id;
        }catch {
            return thunkAPI.rejectWithValue("데이터 삭제 실패");
        }
    }
)

export const fetchPutEmployeeInfoById = createAsyncThunk<
    EmployeeInfo, EmployeeInfo, {rejectValue: string}
>(
    "employeeApi/fetchPutEmployeeInfoById",
    async (emp, thunkAPI) => {
        try{
            const response = await axios.put<EmployeeInfo>(`${API_URL}/app/emp/${emp.id}`, emp);
            return response.data;
        }catch{
            return thunkAPI.rejectWithValue("데이터 수정 실패")
        }
    }

)