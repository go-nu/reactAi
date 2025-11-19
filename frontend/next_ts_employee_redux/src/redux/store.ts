import {configureStore} from "@reduxjs/toolkit";
import emp from "@/redux/employeeSlice";

export const store = configureStore({
    reducer: {
        emp,
    }
});

export type RootState = ReturnType<typeof store.getState>; // initialState
export type RootDispatch = typeof store.dispatch; // action을 잡는 곳