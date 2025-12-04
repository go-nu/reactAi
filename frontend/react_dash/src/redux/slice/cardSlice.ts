// cardSlice.ts

import { createSlice } from "@reduxjs/toolkit";
import { fetchSalesViewAll } from "@/redux/api/salesAPI"; // 기존 Thunk 파일
import { calculateCardData, CardData } from "@/redux/utils/cardUtils";

// 초기 상태
interface CardState {
    cardData: CardData | null;
    loading: boolean;
    error: string | null;
}

const initialState: CardState = {
    cardData: null,
    loading: false,
    error: null,
};

const cardSlice = createSlice({
    name: "card",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            // 💡 데이터 로딩 시작 (대시보드 업데이트 시작)
            .addCase(fetchSalesViewAll.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            // 💡 데이터 로딩 성공 (CardData 계산 및 저장)
            .addCase(fetchSalesViewAll.fulfilled, (state, action) => {
                state.loading = false;
                // 계산 유틸리티 함수를 사용하여 CardData 계산
                state.cardData = calculateCardData(action.payload);
            })
            // 💡 데이터 로딩 실패
            .addCase(fetchSalesViewAll.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload ?? "데이터 로드 실패";
                state.cardData = null;
            });
    },
});

export const cardReducer = cardSlice.reducer;