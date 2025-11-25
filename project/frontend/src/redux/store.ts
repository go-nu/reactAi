import {configureStore} from "@reduxjs/toolkit";
import emp from "@/redux/slice/employeeSlice";

export const store = configureStore({
    reducer: {
        emp,
    }
});

export type RootState = ReturnType<typeof store.getState>;
export type RootDispatch = typeof store.dispatch;