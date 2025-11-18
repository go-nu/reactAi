'use client'
import React, {useEffect, useMemo, useState} from 'react';
import EmployeeList from "@/components/EmployeeList";
import Register from "@/components/Register";
import Upgrade from "@/components/Upgrade";

export const buttonBarStyle:React.CSSProperties = {
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: "10px",
    padding: "20px",
}

export type EmployeeInfo = {
    id: number;
    name: string;
    age: number | string;
    job: string;
    language: string;
    pay: number | string;
}

// Fact Table
const initialTotal:EmployeeInfo[]= [
    {id:1, name: 'John', age: 35, job: "frontend", language: "react", pay: 1},
    {id:2, name: 'Peter', age: 35, job: "frontend", language: "react", pay: 1},
    {id:3, name: 'Sue', age: 35, job: "frontend", language: "react", pay: 1},
    {id:4, name: 'Susan', age: 35, job: "frontend", language: "react", pay: 1},
]

type Mode = "" | "register" | "upgrade" | "delete" | "reset"

const initialEmpInfo: EmployeeInfo
    = {id:1, name: 'John', age: 35, job: "frontend", language: "react", pay: 1}

const Main = () => {
    const [infos, setInfos] = useState<EmployeeInfo[]>(initialTotal);
    const [upInfo, setUpInfo] = useState<EmployeeInfo>(initialEmpInfo);
    const [selectedId, setSelectedId] = useState<number>(0);
    const [mode, setMode] = useState<Mode>('');
    const modes = useMemo(() => [{id:"register" as const, label:"register"},
        {id:"upgrade" as const, label:"upgrade"},
        {id:"delete" as const, label:"delete"},
        {id:"reset"as const, label:"reset"}], [])

    const handleMode = (mod: Mode) =>{
        setMode(mod)
    }
    const handleSelectedId = (id: number) =>{
        setSelectedId(id)
        const found: EmployeeInfo | null =
            infos.filter(info => info.id === id)[0] ?? null;
        setUpInfo(found);
    }

    const handleRegister = (obj: EmployeeInfo) => {
        const nextId = infos.length ? Math.max(...infos.map(i => i.id)) + 1 : 1;
        setInfos(prev => ([...prev, {...obj, id:nextId}]))
    }

    const handleUpgrade = (obj: EmployeeInfo) => {
        setInfos(prev => prev.map(item =>
            item.id === obj.id ? {...item, age: obj.age, job: obj.job,
                language: obj.language, pay: obj.pay} : item
        ));
        setMode("")
    }

    return (
        <>
            <div>
                <EmployeeList
                    infos = {infos}
                    selectedId = {selectedId}
                    handleSelectedId = {handleSelectedId}
                /> {/*자식: InfoTable*/}
            </div>
            <div style={buttonBarStyle}>
                {modes.map(mode => (
                    <button key={mode.id} onClick={()=>handleMode(mode.id)} >{mode.label}</button>
                ))}
            </div>
            <div>
                {mode==="register" && (<Register  handleRegister = {handleRegister}/>)}
                {mode==='upgrade' && <Upgrade
                selectedId = {selectedId}
                upInfo = {upInfo}
                handleUpgrade = {handleUpgrade}
                />}
            </div>
        </>
    );
};

export default Main;