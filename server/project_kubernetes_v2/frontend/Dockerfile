# --- Build stage -------------------------------------------------
FROM node:20-alpine AS builder

# 작업 디렉터리
WORKDIR /app

# 의존성 설치 (package.json / package-lock.json 사용)
COPY package*.json ./
RUN npm install

# 나머지 소스 복사 후 빌드
COPY . .
RUN npm run build


# --- Runtime stage -----------------------------------------------
FROM node:20-alpine AS runner

WORKDIR /app
ENV NODE_ENV=production

# 빌드 결과와 소스, 의존성 복사
COPY --from=builder /app ./

# Next.js 기본 포트
EXPOSE 3000

# package.json 의 "start": "next start" 를 사용
CMD ["npm", "start"]

