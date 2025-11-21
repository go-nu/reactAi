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
    const handleModeChange = (modeId: Mode) => {
        // 1) 먼저 모드 변경
        dispatch(handleMode(modeId));

        // 2) 삭제 모드 버튼을 눌렀을 때 처리
        if (modeId === "delete") {
            if (selectedId == null) {
                alert("삭제할 직원을 먼저 선택해 주세요.");
                return;
            }

            // 필요하면 confirm 추가
            const ok = window.confirm(`정말 ID ${selectedId} 직원을 삭제하시겠습니까?`);
            if (!ok) return;

            // 3) 선택된 직원 ID로 삭제 API 호출
            dispatch(fetchDeleteEmployeeInfoById(selectedId));
        }
    };

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