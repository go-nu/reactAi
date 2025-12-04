import type { Metadata } from "next";
import Providers from "@/redux/Providers";

export const metadata: Metadata = {
    title: "DashBoard",
    description: "The Sales DashBoard",
}
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>
      <Providers>
          {children}
      </Providers>
      </body>
    </html>
  );
}