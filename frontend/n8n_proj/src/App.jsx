// client/src/App.jsx
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setQuestion, fetchAnswer } from './redux/n8n_api_slice.js';

function App() {
    const dispatch = useDispatch();
    const { question, answer, loading, error } = useSelector(
        (state) => state.answer
    );

    const handleChange = (e) => {
        console.log(e.target.value);
        dispatch(setQuestion(e.target.value));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!question.trim()) return;
        dispatch(fetchAnswer(question));
    };

    return (
        <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'sans-serif' }}>
            <h1>React + Redux + API 예제</h1>

            <form onSubmit={handleSubmit}>
                <label htmlFor="question">질문을 입력하세요:</label>
                <br />
                <input
                    id="question"
                    type="text"
                    value={question}
                    onChange={handleChange}
                    style={{ width: '100%', padding: '8px', marginTop: '8px' }}
                    placeholder="예: 오늘 날씨 어때?"
                />
                <button
                    type="submit"
                    style={{ marginTop: '12px', padding: '8px 16px', cursor: 'pointer' }}
                    disabled={loading}
                >
                    {loading ? '요청 중...' : '서버에 보내기'}
                </button>
            </form>

            <div style={{ marginTop: '24px' }}>
                <h2>서버 응답</h2>
                {loading && <p>서버에 질문을 보내는 중입니다...</p>}
                {error && <p style={{ color: 'red' }}>에러: {error}</p>}
                {answer && (
                    <p
                        style={{
                            border: '1px solid #ddd',
                            borderRadius: 8,
                            padding: 12,
                            background: '#f9f9f9',
                        }}
                    >
                        {answer}
                    </p>
                )}
            </div>
        </div>
    );
}

export default App;
