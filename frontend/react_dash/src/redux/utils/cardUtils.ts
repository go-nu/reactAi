// cardDataUtils.ts (유틸리티 파일 생성)

import { SalesData } from "@/redux/types"; // SalesData 타입을 가정합니다.

export interface CardData {
    totalSales: number;
    totalProfit: number;
    totalCustomers: number;
    totalQnty: number;
}

/**
 * 대시보드 카드에 표시할 요약 데이터를 계산합니다.
 * @param data fetchSalesViewAll Thunk에서 반환된 SalesData 배열
 * @returns 계산된 요약 데이터 객체
 */

// src/redux/utils/cardUtils.ts
export const calculateCardData = (data: SalesData[]): CardData => {
    // 1. 고객명(customer_name)의 유니크한 개수를 구합니다.
    const customerNames = new Set(data.map(d => d.customer_name));
    const totalCustomers = customerNames.size;

    // 2. 총합을 계산합니다.
    const totals = data.reduce(
        (acc, d) => {
            acc.sales_amount += Number(d.sales_amount);
            acc.net_profit += Number(d.net_profit);
            acc.quantity += Number(d.quantity);
            return acc;
        },
        { sales_amount: 0, net_profit: 0, quantity: 0 }
    );

    return {
        totalSales: Math.round(totals.sales_amount),
        totalProfit: Math.round(totals.net_profit),
        totalCustomers: totalCustomers,
        totalQnty: totals.quantity,
    };
};