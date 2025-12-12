// client/src/store/answerSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// 비동기 thunk: 서버에 질문을 보내고 답변을 받아옴
export const fetchAnswer = createAsyncThunk(
    'answer/fetchAnswer',
    async (question, { rejectWithValue }) => {

        try {
            const res = await fetch('http://localhost:5678/webhook/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ customer_text: question }),
            });

            // ✅ 항상 "텍스트"로 받기 (JSON 아님!)
            const text = await res.text();
            console.log('서버 원본 응답:', text);

            if (!res.ok) {
                return rejectWithValue(text || '서버 오류가 발생했습니다.');
            }

            // ✅ 그냥 텍스트 그대로 Redux state로 보냄
            return text;
        } catch (err) {
            return rejectWithValue(err.message || '네트워크 오류');
        }
    }
);


const answerSlice = createSlice({
    name: 'answer',
    initialState: {
        question: '',
        answer: '',
        loading: false,
        error: null,
    },
    reducers: {
        setQuestion(state, action) {
            state.question = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchAnswer.pending, (state) => {
                state.loading = true;
                state.error = null;
                state.answer = '';
            })
            .addCase(fetchAnswer.fulfilled, (state, action) => {
                state.loading = false;
                state.answer = action.payload;
            })
            .addCase(fetchAnswer.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || '알 수 없는 오류';
            });
    },
});

export const { setQuestion } = answerSlice.actions;
export default answerSlice.reducer;

