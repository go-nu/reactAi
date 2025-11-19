'use client'
import React, {useMemo, useState, useContext} from 'react';
import EmployeeList from "@/components/EmployeeList";
import Register from "@/components/Register";
import Upgrade from "@/components/Upgrade";
import {EmployeeContext, EmployeeProvider, useEmployee} from "@/context/EmployeeContext";

export const buttonBarStyle:React.CSSProperties = {
    display: "flex",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: "10px",
    padding: "20px",
}

const MainContent = () => {
    const {mode, modes, handleMode} = useEmployee()

    return (
        <>
            <div>
                <EmployeeList /> {/*자식: InfoTable*/}
            </div>
            <div style={buttonBarStyle}>
                {modes.map(item => (
                    <button key={item.id} onClick={()=>handleMode(item.id)}>{item.label}</button>
                ))}
            </div>
            <div>
                {mode==="register" && (<Register />)}
                {mode==='upgrade' && <Upgrade />}
            </div>
        </>
    );
};

const Main = () => {
    return (
        <EmployeeProvider>
            <MainContent />
        </EmployeeProvider>
    )
}

export default Main;