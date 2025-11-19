"use client"

import React, {
    useMemo,
    useCallback,
    useState,
    createContext,
    PropsWithChildren, useContext,
} from "react";

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

export type Mode = "" | "register" | "upgrade" | "delete" | "reset"

const initialEmpInfo: EmployeeInfo
    = {id:0, name: 'Jo', age: 0, job: "", language: "", pay: 0}

interface ModeItem {
    id: Mode;
    label: string;
}

interface EmployeeContextValue {
    mode: Mode;
    modes:ModeItem[];
    infos: EmployeeInfo[];
    upInfo: EmployeeInfo;
    selectedId: number;
    handleMode: (mode: Mode) => void;
    handleSelectedId: (id: number) => void;
    handleRegister: (obj: EmployeeInfo) => void;
    handleUpgrade: (obj: EmployeeInfo) => void;
}

export const EmployeeContext = createContext<EmployeeContextValue | undefined>(undefined);

export const EmployeeProvider = ({children}:PropsWithChildren) =>{
    const [infos, setInfos] = useState<EmployeeInfo[]>(initialTotal);
    const [upInfo, setUpInfo] = useState<EmployeeInfo | null>(initialEmpInfo);
    const [selectedId, setSelectedId] = useState<number | string | null>(0);
    const [mode, setMode] = useState<Mode | string>('');

    const modes = useMemo<ModeItem[]>(() => [
        {id:"register" as Mode, label:"register"},
        {id:"upgrade" as Mode, label:"upgrade"},
        {id:"delete" as Mode, label:"delete"},
        {id:"reset"as Mode, label:"reset"}], [])

    const handleMode = (mod: Mode) =>{
        if(mod === "delete"){
            if(!selectedId){
                alert("직원을 선택해 주세요!!!")
                return;
            }
            const targetObj = infos.find(x => x.id === selectedId)
            if(!targetObj){
                alert("해당 직원을 찾을 수 없습니다.")
                return;
            }
            if(confirm(`${targetObj.name} 직원을 삭제할까요?`)){
                setInfos(prev => prev.filter(item => item.id !== selectedId))
                setMode("");
                setUpInfo(null);
                setSelectedId('');
            }
            return;
        }
        if(mod === 'reset'){
            if(confirm("목록을 초기 데이터로 되돌릴까요?")){
                setInfos(initialTotal)
                setMode("");
                setUpInfo(null);
                setSelectedId('');
            }
            return;
        }
        if(mod === "upgrade"){
            if(!selectedId){
                alert("수정할 직원을 먼저 선택해 주세요!!")
                return;
            }
        }
        setMode(mod)
    }

    const handleSelectedId = (id: number) =>{
        setSelectedId(id)
        const found: EmployeeInfo | null =
            infos.filter(info => info.id === id)[0] ?? null;
        setUpInfo(found);
    }

    const handleRegister = (obj: EmployeeInfo) => {
        if (!obj.name){
            alert("이름은 필수입니다.")
            return;
        }
        if (!obj.age || Number(obj.age)<0){
            alert("나이는 필수입니다.")
            return;
        }
        if (!obj.pay || Number(obj.pay)<0){
            alert("급여는 필수입니다.")
            return;
        }

        if (infos.some(item => item.name === obj.name)){
            alert("이미 존재하는 이름입니다.")
            return;
        }
        const nextId = infos.length ? Math.max(...infos.map((i) => i.id)) + 1 : 1;
        setInfos(prev => ([...prev, {...obj, id:nextId}]))
    }

    const handleUpgrade = (obj: EmployeeInfo) => {
        if (Number(obj.age)<0){
            alert("나이는 0 이상입니다.")
            return;
        }
        if (Number(obj.pay)<0){
            alert("급여는 0 이상입니다.")
            return;
        }
        setInfos(prev => prev.map(item =>
            item.id === obj.id ?
                {...item,
                    age: obj.age,
                    job: obj.job,
                    language: obj.language,
                    pay: obj.pay,
                } : item
        ));
        setMode('')
    }

    const value = useMemo(()=>(
        {
            mode,
            infos,
            modes,
            upInfo,
            selectedId,
            handleMode,
            handleUpgrade,
            handleRegister,
            handleSelectedId
        }
    ), [
        mode,
        infos,
        modes,
        upInfo,
        selectedId,
        handleMode,
        handleUpgrade,
        handleRegister,
        handleSelectedId
    ])

    return(
        <EmployeeContext.Provider value={value}>
            {children}
        </EmployeeContext.Provider>
    )
}

// 사용자 hook: 맨 앞에 use 사용
export const useEmployee = () =>{
    const context = useContext(EmployeeContext);
    if (!context){
        throw new Error("useContext() not found!");
    }
    return context;
}

