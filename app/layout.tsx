import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "SENTINEL Analyst",
  description: "Chat with the security agent. Graph query runs in the background; answers come from cited documents.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, minHeight: "100vh" }}>
        {children}
      </body>
    </html>
  );
}
