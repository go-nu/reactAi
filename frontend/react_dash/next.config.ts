// next.config.ts

import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* 다른 config options (생략) */

  webpack: (config, { isServer }) => {
    // isServer가 false일 때 (즉, 클라이언트 빌드일 때)만 실행
    if (!isServer) {
      config.resolve.fallback = {
        // Node.js 코어 모듈들을 빈 객체(false)로 대체하여 번들링에서 제외합니다.
        fs: false,
        net: false,
        tls: false,
        dns: false,
        path: false, // path 모듈도 종종 문제를 일으키므로 포함합니다.
      };
    }
    
    // 수정된 config 객체를 반드시 반환해야 합니다.
    return config;
  },
};

export default nextConfig;