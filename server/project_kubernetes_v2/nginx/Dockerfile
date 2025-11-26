FROM nginx:1.27-alpine

# 기본 default.conf는 삭제 (예전 spring-backend 설정 들어있을 수 있음)
RUN rm -f /etc/nginx/conf.d/default.conf

# 우리가 만든 nginx.conf를 메인 설정으로 사용
COPY nginx.conf /etc/nginx/nginx.conf

