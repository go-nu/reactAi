// src/app/api/sales/route.ts (새로 생성)
// 이 파일은 Node.js 서버 환경에서 실행됩니다.

import { NextResponse } from 'next/server';
import { queryPostgres } from '@/redux/api/dbConn'; // 👈 dbConn.ts의 DB 쿼리 함수 사용
import { SalesData } from '@/redux/types'; // (가정) SalesData 타입 import

export async function GET(request: Request) {
    // URLSearchParams를 사용하여 limit 값을 가져옵니다.
    const url = new URL(request.url);
    const limit = url.searchParams.get('limit') || '20000';
    const limitNum = parseInt(limit, 10);

    const sqlQuery = `
        SELECT
            date_id,
            year,
            quarter,
            month_no,
            month_name,
            customer_name,
            gender,
            birth_date,
            age,
            product_name,
            color,
            product_category_name,
            category_name,
            sido,
            sigungu,
            region,
            channel_name,
            promotion_name,
            discount_rate,
            quantity,
            sales_unit_price,
            sales_amount,
            cost_price,
            cost_amount,
            net_profit
        FROM sales_view_table
        ORDER BY date_id
        LIMIT $1
    `;

    try {
        // 💡 서버에서 안전하게 DB 쿼리 실행
        const salesData = await queryPostgres<SalesData>(sqlQuery, [limitNum]);

        if (!salesData || salesData.length === 0) {
             return new NextResponse("No sales data found", { status: 404 });
        }

        return NextResponse.json(salesData);

    } catch (error) {
        console.error("API DB Fetch Error:", error);
        return new NextResponse("데이터 로드 실패: DB 연결 또는 쿼리 오류", { status: 500 });
    }
}