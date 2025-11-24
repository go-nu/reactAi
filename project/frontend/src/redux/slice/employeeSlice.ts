import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {
    fetchDeleteEmployeeInfoById,
    fetchGetEmployeeInfos,
    fetchPostEmployeeInfo,
    fetchPutEmployeeInfoById
} from "@/redux/api/employeeAPI";


export type Mode = "" | "register" | "upgrade" | "delete" | "reset"

interface ModeItem {
    id: Mode;
    label: string;
}
// mode data
const modes: ModeItem[] =  [
    {id:"register" as Mode, label:"register" as string},
    {id:"upgrade" as Mode, label:"upgrade" as string},
    {id:"delete" as Mode, label:"delete" as string},
    {id:"reset"as Mode, label:"reset" as string}
]

export type EmployeeInfo = {
    id: number;
    name: string;
    age: number | string;
    job: string;
    language: string;
    pay: number | string;
}

interface EmployeeStateType {
    mode: Mode;
    modes:ModeItem[];
    infos: EmployeeInfo[];
    upInfo: EmployeeInfo | null;
    selectedId: number | null;
    error: string | null;
    loading: boolean;
}

// initialState 설정
const initialState: EmployeeStateType = {
    mode: '',
    modes,
    infos: [],
    upInfo: null,
    selectedId: 0,
    error: null,
    loading: false
}


// Action Reducers 설정
const handleModeReducer = (
    state: EmployeeStateType,
    action: PayloadAction<Mode>
) =>{
    const mod = action.payload;

    if(mod === "delete"){
        if(!state.selectedId){
            alert("직원을 선택해 주세요!!!")
            return;
        }
        const targetObj = state.infos.find(x => x.id === state.selectedId)
        if(!targetObj){
            alert("해당 직원을 찾을 수 없습니다.")
            return;
        }
        if(confirm(`${targetObj.name} 직원을 삭제할까요?`)){

            state.infos = [...state.infos].filter(item => item.id !== state.selectedId)
            state.mode = "";
            state.upInfo= null;
            state.selectedId = null;
        }
        return;
    }
    if(mod === 'reset'){
        if(confirm("목록을 초기 데이터로 되돌릴까요?")){
            state.mode = "";
            state.upInfo= null;
            state.selectedId = null;
        }
        return;
    }
    if(mod === "upgrade"){
        if(!state.selectedId){
            alert("수정할 직원을 먼저 선택해 주세요!!")
            return;
        }
    }
    state.mode = mod
}

const handleSelectedIdReducer = (
    state:EmployeeStateType,
    action:PayloadAction<number>
) =>{
    const id = action.payload;
    state.selectedId = id
    state.upInfo = state.infos.filter(info => info.id === id)[0] ?? null;
}

const handleRegisterReducer = (
    state: EmployeeStateType,
    action: PayloadAction<EmployeeInfo>
) => {
    const obj = action.payload;
    if (!obj.name) {
        alert("이름은 필수입니다.")
        return;
    }
    if (!obj.age || Number(obj.age) < 0) {
        alert("나이는 필수입니다.")
        return;
    }
    if (!obj.pay || Number(obj.pay) < 0) {
        alert("급여는 필수입니다.")
        return;
    }
    if (state.infos.some(item => item.name === obj.name)) {
        alert("이미 존재하는 이름입니다.")
        return;
    }
    const nextId = state.infos.length ? Math.max(...state.infos.map((i) => i.id)) + 1 : 1;
    state.infos = [...state.infos, {...obj, id: nextId}];
}


// thunk Slice 담기
const employeeSlice = createSlice({
    name: "employeeSlice",
    initialState,
    reducers:{
        handleMode: handleModeReducer,
        handleRegister: handleRegisterReducer,
        // handleUpgrade: handleUpgradeReducer,
        handleSelectedId: handleSelectedIdReducer
    },
    extraReducers: (builder) => {
        //Get 전체 데이터 fetchGetEmployeeInfos
        builder
            .addCase(fetchGetEmployeeInfos.pending, (state) =>{
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchGetEmployeeInfos.fulfilled, (state, action) =>{
                state.loading = false;
                console.log("total", action.payload);
                state.infos = action.payload;
                console.log("state.total", state.infos);
            })
            .addCase(fetchGetEmployeeInfos.rejected, (state, action) =>{
                state.loading = false;
                state.error = action.payload ?? "로드 실패";
            })
        builder
            .addCase(fetchPostEmployeeInfo.pending, (state) =>{
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchPostEmployeeInfo.fulfilled, (state, action) =>{
                state.loading = false;
                state.infos =[...state.infos, action.payload];
                if(action.payload){
                    state.mode = '';
                }
                console.log("infos", state.infos)
            })
            .addCase(fetchPostEmployeeInfo.rejected, (state, action) =>{
                state.loading = false;
                state.error = action.payload ?? "로드 실패";
            })
        builder
            .addCase(fetchPutEmployeeInfoById.pending, (state) =>{
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchPutEmployeeInfoById.fulfilled, (state, action) =>{
                const obj = action.payload;
                state.loading = false;
                state.upInfo = action.payload;
                state.infos = [...state.infos].map(item =>
                    item.id === obj.id ?
                        {...item,
                            age: obj.age,
                            job: obj.job,
                            language: obj.language,
                            pay: obj.pay,
                        } : item
                );
                if(action.payload){
                    state.mode = '';
                }
            })
            .addCase(fetchPutEmployeeInfoById.rejected, (state, action) =>{
                state.loading = false;
                state.error = action.payload ?? "로드 실패";
            })
        builder
            .addCase(fetchDeleteEmployeeInfoById.pending, (state) =>{
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchDeleteEmployeeInfoById.fulfilled, (state, action) =>{
                const id = action.payload;
                state.infos = [...state.infos].filter(item => item.id !== id);
                state.loading = false;

            })
            .addCase(fetchDeleteEmployeeInfoById.rejected, (state, action) =>{
                state.loading = false;
                state.error = action.payload ?? "로드 실패";
            })
    }

});

export const {
    handleMode,
    // handleRegister,
    // handleUpgrade,
    handleSelectedId
} = employeeSlice.actions;

export default employeeSlice.reducer;