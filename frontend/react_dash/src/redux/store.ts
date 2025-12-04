// store.ts

import { configureStore } from '@reduxjs/toolkit';
import { cardReducer } from "@/redux/slice/cardSlice";

// 1. Store 설정: reducer가 없을 때 빈 객체 {}를 사용합니다.
export const store = configureStore({
  // 아직 정의된 슬라이스 리듀서가 없으므로 빈 객체를 사용합니다.
  reducer: {
    card: cardReducer,
  },
  // 개발 환경에서 유용한 기본 미들웨어 및 DevTools 설정이 포함됩니다.
});

// 2. TypeScript 타입 정의 (필수)
// RootState: Store의 전체 상태 타입을 추론합니다.
// 현재는 리듀서가 비어있으므로 빈 상태({}) 타입이 추론됩니다.
export type RootState = ReturnType<typeof store.getState>;

// AppDispatch: Store의 dispatch 타입을 추론합니다.
// 이 타입은 컴포넌트에서 useDispatch를 사용할 때 필요합니다.
export type AppDispatch = typeof store.dispatch;