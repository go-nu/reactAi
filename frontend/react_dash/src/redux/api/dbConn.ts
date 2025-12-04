// src/redux/api/dbConn.ts

import { Pool, QueryResult } from 'pg';

// DB 연결 풀 설정 (내용은 동일)
const pool = new Pool({
    user: 'kogo',
    host: 'localhost',
    database: 'mydb',
    password: 'math1106',
    port: 5433,
});

/**
 * PostgreSQL에서 SQL 쿼리를 실행하고 결과 데이터를 반환합니다.
 */
// 💡 Line 16 수정: any[] 대신 unknown[] 사용 (더 엄격한 타입 체크)
export async function queryPostgres<T>(text: string, params?: unknown[]): Promise<T[]> {
    const client = await pool.connect();

    try {
        // 💡 수정 2: QueryResult<T> 대신 QueryResult를 사용하고, rows를 T[]로 캐스팅하여 타입 오류 제거
        const result: QueryResult = await client.query(text, params);

        // 행 데이터만 추출하여 반환
        return result.rows as T[]; // rows를 T[]로 타입 캐스팅

    } catch (err) {
        console.error('PostgreSQL Query Error:', err);
        throw new Error("Failed to execute database query.");
    } finally {
        client.release();
    }
}