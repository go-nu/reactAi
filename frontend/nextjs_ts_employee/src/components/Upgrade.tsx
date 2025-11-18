'use client';

import React, { useEffect, useState } from 'react';
import type { EmployeeInfo } from './Main';

const formStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: '300px',
    margin: '20px auto',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '10px',
    backgroundColor: '#f9f9f9',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
};

const labelStyle: React.CSSProperties = {
    marginBottom: '10px',
    display: 'flex',
    flexDirection: 'column',
    fontWeight: 'bold',
    color: '#333',
};

const inputStyle: React.CSSProperties = {
    padding: '8px',
    borderRadius: '5px',
    border: '1px solid #ccc',
    fontSize: '14px',
};

// 매번 새로운 객체를 만드는 초기 상태
const createInitialState = (): EmployeeInfo => ({
    id: 0,
    name: '',
    age: '',
    job: '',
    language: '',
    pay: '',
});

interface UpgradeProps {
    selectedId: number;
    upInfo: EmployeeInfo | null;
    handleUpgrade: (info: EmployeeInfo) => void;
}

const Upgrade = ({ selectedId, upInfo, handleUpgrade }: UpgradeProps) => {
    const [info, setInfo] = useState<EmployeeInfo>(() => createInitialState());

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setInfo((prev) => ({ ...prev, [name]: value })); // id는 그대로 유지
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        handleUpgrade(info);
    };

    /* eslint-disable react-hooks/set-state-in-effect */
    useEffect(() => {
        if (selectedId && upInfo) {
            setInfo({
                id: upInfo.id,
                name: upInfo.name,
                age: String(upInfo.age ?? ''),
                job: upInfo.job ?? '',
                language: upInfo.language ?? '',
                pay: String(upInfo.pay ?? ''),
            });
        } else {
            setInfo(createInitialState());
        }
    }, [selectedId, upInfo]);
    /* eslint-enable react-hooks/set-state-in-effect */

    return (
        <form style={formStyle} onSubmit={handleSubmit}>
            <label style={labelStyle}>
                Name
                <input type="text" name="name" style={inputStyle} value={info.name} disabled />
            </label>
            <label style={labelStyle}>
                Age
                <input
                    type="number"
                    name="age"
                    style={inputStyle}
                    value={info.age}
                    onChange={handleChange}
                    min={1}
                />
            </label>
            <label style={labelStyle}>
                Job
                <input
                    type="text"
                    name="job"
                    style={inputStyle}
                    value={info.job}
                    onChange={handleChange}
                />
            </label>
            <label style={labelStyle}>
                Language
                <input
                    type="text"
                    name="language"
                    style={inputStyle}
                    value={info.language}
                    onChange={handleChange}
                />
            </label>
            <label style={labelStyle}>
                Pay
                <input
                    type="number"
                    name="pay"
                    style={inputStyle}
                    value={info.pay}
                    onChange={handleChange}
                    min={0}
                />
            </label>
            <button type="submit">수정</button>
        </form>
    );
};

export default Upgrade;