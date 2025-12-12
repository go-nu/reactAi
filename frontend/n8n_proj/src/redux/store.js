// client/src/store/store.js
import { configureStore } from '@reduxjs/toolkit';
import answer from './n8n_api_slice.js';

export const store = configureStore({
    reducer: {
        answer,
    },
});
