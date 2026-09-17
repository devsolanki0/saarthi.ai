import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SAARTHI.AI",
  description: "Ancient Wisdom. Modern Intelligence."
};

export default function RootLayout({
  children
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}