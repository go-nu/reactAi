import React, {useState} from 'react';
import {useDispatch} from "react-redux";
import {EmployeeInfo, handleRegister} from "@/redux/employeeSlice";
import {RootDispatch} from "@/redux/store";

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

const initialEmpInfo: EmployeeInfo = {
    id: 0, name: "", age: 0, job: "", language: "", pay: 0
}

const Register = () => {
    const dispatch = useDispatch<RootDispatch>();
    const [info, setInfo] = useState<EmployeeInfo>(initialEmpInfo);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        // console.log(e.target);
        setInfo(prev => ({...prev, [name]: value}));
    }
    const handleSubmit = (e:React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); // 페이지 이동하지 않는다.
        dispatch(handleRegister(info));
    }

    return (
        <form style={formStyle} onSubmit={handleSubmit}>
            <label style={labelStyle}>
                Name
                <input type="text" name="name"
                       onChange={handleChange}
                       style={inputStyle} required/>
            </label>
            <label style={labelStyle}>
                Age
                <input type="number" name="age"
                       min={1} onChange={handleChange}
                       style={inputStyle} required/>
            </label>
            <label style={labelStyle}>
                Job
                <input type="text" name="job"
                       onChange={handleChange} style={inputStyle}/>
            </label>
            <label style={labelStyle}>
                Language
                <input type="text" name="language"
                       onChange={handleChange} style={inputStyle}/>
            </label>
            <label style={labelStyle}>
                Pay
                <input type="number" name="pay"
                       min={0} onChange={handleChange}
                       style={inputStyle} required/>
            </label>
            <button type="submit">등록</button>
        </form>
    );
};

export default Register;