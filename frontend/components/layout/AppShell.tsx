'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth/AuthContext';
import { AppSidebar } from './AppSidebar';
import { AppHeader } from './AppHeader';
import { DisclaimerBanner } from '@/components/ui/DisclaimerBanner';
import { Alert } from '@/components/ui/Alert';

interface AppShellProps {
  children: React.ReactNode;
  title?: string;
  adminOnly?: boolean;
}

export function AppShell({ children, title, adminOnly = false }: AppShellProps) {
  const router = useRouter();
  const { isAuthenticated, isAdmin, isLoading } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#F4F7FB] flex flex-col items-center justify-center p-4">
        <div className="w-12 h-12 border-4 border-[#DCE5EF] border-t-[#1769E0] rounded-full animate-spin mb-4" />
        <p className="text-sm font-medium text-[#66778B]">Loading PropValueAI Session...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect via useEffect
  }

  if (adminOnly && !isAdmin) {
    return (
      <div className="flex h-screen bg-[#F4F7FB] overflow-hidden">
        <div className="hidden lg:block">
          <AppSidebar />
        </div>
        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
          <AppHeader onOpenMobileMenu={() => setMobileMenuOpen(true)} title="Access Restricted" />
          <main className="p-4 sm:p-8 max-w-4xl mx-auto w-full">
            <Alert variant="danger" title="Admin Privileges Required">
              You do not have administrative authorization to view system-wide predictions. Please contact the system administrator.
            </Alert>
          </main>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-[#F4F7FB] overflow-hidden">
      {/* Desktop Sidebar */}
      <div className="hidden lg:block shrink-0">
        <AppSidebar />
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden flex">
          <div
            className="fixed inset-0 bg-black/50 backdrop-blur-xs transition-opacity"
            onClick={() => setMobileMenuOpen(false)}
          />
          <div className="relative z-10">
            <AppSidebar onCloseMobile={() => setMobileMenuOpen(false)} />
          </div>
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <AppHeader onOpenMobileMenu={() => setMobileMenuOpen(true)} title={title} />

        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <div className="max-w-[1440px] mx-auto space-y-6">
            <DisclaimerBanner />
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
