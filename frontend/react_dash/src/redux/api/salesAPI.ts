// src/redux/api/salesAPI.ts (수정)

import { createAsyncThunk } from "@reduxjs/toolkit";
// 💡 dbConn import 제거 (클라이언트에서 DB 코드 사용 중단)
import { SalesData } from "../types"; // (가정) SalesData 타입 import

export const fetchSalesViewAll = createAsyncThunk<
    SalesData[],
    { limit: number },
    { rejectValue: string }
>(
    "salesApi/fetchSalesViewAll",
    async ({ limit }, thunkAPI) => {
        try {
            // 💡 쿼리 대신 API Route 호출로 변경
            const response = await fetch(`/api/sales?limit=${limit}`);

            if (!response.ok) {
                // 서버에서 발생한 오류 메시지를 읽어와 반환
                const errorText = await response.text();
                return thunkAPI.rejectWithValue(`API 오류 발생: ${errorText}`);
            }

            const salesData: SalesData[] = await response.json();

            return salesData;

        } catch (error) {
            console.error("Network Fetch Error:", error);
            // 클라이언트와 서버 간의 네트워크 오류 처리
            return thunkAPI.rejectWithValue("네트워크 연결 실패 (API 서버 접근 불가)");
        }
    }
);