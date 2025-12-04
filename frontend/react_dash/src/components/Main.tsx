'use client'
import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchSalesViewAll } from "@/redux/api/salesAPI"; // Thunk
import { RootState, AppDispatch } from "@/redux/store"; // Redux Store 타입 가정


// 통화 형식 포맷 함수 (예시: 10000 -> 10,000)
const formatCurrency = (value: number) => new Intl.NumberFormat('ko-KR').format(value);

const Main = () => {// Redux 훅을 사용하여 상태와 디스패치를 가져옵니다.
    const dispatch = useDispatch<AppDispatch>();
    const { cardData, loading, error } = useSelector((state: RootState) => state.card);

    // (선택 사항) Dash처럼 필터링 로직이 있다면 여기 추가:
    // const selectedRegion = useSelector(...);
    // const selectedCategory = useSelector(...);

    // 💡 컴포넌트가 마운트될 때 데이터 로드 (Dash의 초기 업데이트와 유사)
    useEffect(() => {
        // Dash의 update_dashboard 콜백처럼 데이터를 가져옵니다.
        // 여기서는 필터링 없이 전체 데이터를 가져오는 예시입니다.
        dispatch(fetchSalesViewAll({ limit: 20000 }));
    }, [dispatch]);

    if (loading) {
        return <div className="dashboard-cards-loading">데이터 로딩 중...</div>;
    }
    if (error) {
        return <div className="dashboard-cards-error">오류 발생: {error}</div>;
    }
    if (!cardData) {
        return <div className="dashboard-cards-empty">데이터가 없습니다.</div>;
    }

    return (
        <>
            <div>
                <h2>매출 분석 대시보드</h2>
                <div>
                    {/* 총 매출액 카드 */}
                    <div id="card_total_sales" className="card-style">
                        <h4 className="card-title">총 매출액</h4>
                        <h2 className="card-value">{formatCurrency(cardData.totalSales)}원</h2>
                    </div>

                    {/* 전체 순이익 카드 */}
                    <div id="card_total_profit" className="card-style">
                        <h4 className="card-title">전체 순이익</h4>
                        <h2 className="card-value">{formatCurrency(cardData.totalProfit)}원</h2>
                    </div>

                    {/* 총 고객수 카드 */}
                    <div id="card_total_customers" className="card-style">
                        <h4 className="card-title">총 고객수</h4>
                        <h2 className="card-value">{formatCurrency(cardData.totalCustomers)}명</h2>
                    </div>

                    {/* 총 거래 건수 카드 */}
                    <div id="card_total_qnty" className="card-style">
                        <h4 className="card-title">총 거래 건수</h4>
                        <h2 className="card-value">{formatCurrency(cardData.totalQnty)}건</h2>
                    </div>
                </div>
                <div>
                    <div>
                        {/*<Graph1/>*/}
                    </div>
                    <div>
                        {/*<Graph2/>*/}
                    </div>
                </div>
                <div>
                    <div>
                        {/*<Dropdown3/>*/}
                        {/*<Graph3/>*/}
                    </div>
                    <div>
                        {/*<Dropdown4/>*/}
                        {/*<Graph4/>*/}
                    </div>
                </div>
            </div>
        </>
    )
}

export default Main;