'use client';
import React, {useEffect} from 'react';
import InfoTable from "@/components/InfoTable";
import {buttonBarStyle} from './Main';

import {useDispatch, useSelector} from "react-redux";
import {handleSelectedId} from "@/redux/slice/employeeSlice";
import {RootDispatch, RootState} from "@/redux/store";
import {fetchGetEmployeeInfos} from "@/redux/api/employeeAPI";

const EmployeeList = () => {
    const {infos} = useSelector((state: RootState) => state.emp);
    const dispatch = useDispatch<RootDispatch>();

    useEffect(() => {
        dispatch(fetchGetEmployeeInfos());
    }, [dispatch]);

    return (
        <>
            <div style={buttonBarStyle}>
                {infos?.map(info => (
                        <button
                            key={info.id}
                            onClick={() => dispatch(handleSelectedId(info.id))}
                        >
                            {info.name}
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