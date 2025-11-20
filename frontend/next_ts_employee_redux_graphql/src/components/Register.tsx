'use client';
import React, {useState} from 'react';
import {useDispatch, useSelector} from "react-redux";
import {EmployeeInfo} from "@/redux/slice/employeeSlice";
import {fetchPostEmployeeInfo} from "@/redux/api/employeeAPI";
import {RootDispatch, RootState} from "@/redux/store";

export const formStyle: React.CSSProperties = {
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
export const labelStyle: React.CSSProperties = {
    marginBottom: '10px',
    display: 'flex',
    flexDirection: 'column',
    fontWeight: 'bold',
    color: '#333',
};
export const inputStyle: React.CSSProperties = {
    padding: '8px',
    borderRadius: '5px',
    border: '1px solid #ccc',
    fontSize: '14px',
};
const initialEmpInfo: EmployeeInfo
    = {id:0, name: '', age: 0, job: "", language: "", pay: 0}

const Register = () => {
    const dispatch = useDispatch<RootDispatch>();
    const {infos} = useSelector((state:RootState)=> state.emp)

    const [info, setInfo] = useState<EmployeeInfo>(initialEmpInfo);
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        // console.log(name, value)
        setInfo((prev) => ({ ...prev, [name]: value })); // id는 그대로 유지
    };
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!info.name) {
            alert("이름은 필수입니다.")
            return;
        }
        if (!info.age || Number(info.age) < 0) {
            alert("나이는 필수입니다.")
            return;
        }
        if (!info.pay || Number(info.pay) < 0) {
            alert("급여는 필수입니다.")
            return;
        }
        if (infos.some(item => item.name === info.name)) {
            alert("이미 존재하는 이름입니다.")
            return;
        }

        dispatch(fetchPostEmployeeInfo(info))
        setInfo(initialEmpInfo);

    };
    return (
        <form style={formStyle} onSubmit={handleSubmit}>
            <label style={labelStyle}>
                Name
                <input
                    type="text"
                    name="name"
                    style={inputStyle}
                    onChange={handleChange}
                    required
                />
            </label>
            <label style={labelStyle}>
                Age
                <input
                    type="number"
                    name="age"
                    style={inputStyle}
                    onChange={handleChange}
                    min={1}
                    required
                />
            </label>
            <label style={labelStyle}>
                Job
                <input
                    type="text"
                    name="job"
                    style={inputStyle}
                    onChange={handleChange}
                />
            </label>
            <label style={labelStyle}>
                Language
                <input
                    type="text"
                    name="language"
                    style={inputStyle}
                    onChange={handleChange}
                />
            </label>
            <label style={labelStyle}>
                Pay
                <input
                    type="number"
                    name="pay"
                    style={inputStyle}
                    onChange={handleChange}
                    min={0}
                    required
                />
            </label>
            <button type="submit">등록</button>
        </form>
    );
};

export default Register;
