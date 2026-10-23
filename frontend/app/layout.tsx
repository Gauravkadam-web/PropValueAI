import type { Metadata } from 'next';
import './globals.css';
import { AuthProvider } from '@/lib/auth/AuthContext';

export const metadata: Metadata = {
  title: 'PropValueAI — Real Estate Price Prediction',
  description:
    'Educational residential real-estate price prediction platform powered by machine learning and decoupled Spring Boot backend.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen flex flex-col bg-[#F4F7FB] text-[#172B42]">
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
