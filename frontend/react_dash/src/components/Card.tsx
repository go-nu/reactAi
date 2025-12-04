import React from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";

// 통화 형식 포맷 함수 (예시: 10000 -> 10,000)
const formatCurrency = (value: number) => new Intl.NumberFormat('ko-KR').format(value);

const CardDiv = () => {
    const cardData = useSelector((state: RootState) => state.card);

    return (
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
    )
}