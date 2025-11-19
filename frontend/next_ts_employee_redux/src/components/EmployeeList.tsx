import React from 'react';
import InfoTable from "@/components/InfoTable";
import {buttonBarStyle} from "./Main";

import {useDispatch, useSelector} from "react-redux";
import {handleSelectedId} from "@/redux/employeeSlice";
import {RootDispatch, RootState} from "@/redux/store";

// {키:값}인데 키=값이면 {키}로 적는 문법
const EmployeeList = () => {
    const {infos} = useSelector((state: RootState) => state.emp);
    const dispatch = useDispatch<RootDispatch>();

    return (
        <>
            <div style={buttonBarStyle}>
                {infos?.map((info) => (
                            <button
                                    key={info.id}
                                    onClick={() => dispatch(handleSelectedId(info.id))}
                                >{info.name}
                            </button>
                        )
                    )
                }
            </div>
            <InfoTable/>
        </>
    );
};

export default EmployeeList;