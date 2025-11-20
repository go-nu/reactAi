'use client'
import React from 'react';
import EmployeeList from "@/components/EmployeeList";
import Register from "@/components/Register";
import Upgrade from "@/components/Upgrade";
import {useDispatch, useSelector} from "react-redux";
import {RootDispatch, RootState} from "@/redux/store";
import {handleMode, handleSelectedId} from "@/redux/slice/employeeSlice";
import type {Mode} from "@/redux/slice/employeeSlice";
import {fetchDeleteEmployeeInfoById} from "@/redux/api/employeeAPI";


export const Style:React.CSSProperties = {
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: "10px",
    padding: "20px",
}

const Main = () => {
    const {mode, selectedId, modes} = useSelector((state: RootState) => state.emp);
    const dispatch = useDispatch<RootDispatch>();
    const handleModeChange = (id:Mode) => {
        dispatch(handleMode(id));
        if (mode === "delete" && typeof selectedId === "number") {
            dispatch(fetchDeleteEmployeeInfoById(selectedId))
        }
    }

    return (
        <>
            <div>
                <EmployeeList/> {/*자식: InfoTable*/}
            </div>
            <div style={Style}>
                {modes.map(item => (
                    <button key={item.id} onClick={() => handleModeChange(item.id)}>
                        {item.label}
                    </button>
                ))}
            </div>
            <div>
                {mode==="register" && (<Register/>)}
                {mode==='upgrade' && <Upgrade/>}
            </div>

        </>

    );
};



export default Main;