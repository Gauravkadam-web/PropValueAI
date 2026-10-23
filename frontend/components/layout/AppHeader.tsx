'use client';

import React from 'react';
import { useAuth } from '@/lib/auth/AuthContext';
import { MenuIcon, LogOutIcon } from '@/components/ui/Icons';
import { Badge } from '@/components/ui/Badge';

interface AppHeaderProps {
  onOpenMobileMenu: () => void;
  title?: string;
}

export function AppHeader({ onOpenMobileMenu, title = 'PropValueAI Analytics' }: AppHeaderProps) {
  const { user, isAdmin, logout } = useAuth();

  return (
    <header className="h-16 bg-white border-b border-[#DCE5EF] flex items-center justify-between px-4 sm:px-8 shrink-0 z-20">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onOpenMobileMenu}
          className="lg:hidden p-2 text-[#172B42] hover:bg-[#F4F7FB] rounded-radius-sm"
          aria-label="Open navigation menu"
        >
          <MenuIcon className="w-5 h-5" />
        </button>
        <h1 className="text-lg sm:text-xl font-bold text-[#10243A] tracking-tight">{title}</h1>
      </div>

      <div className="flex items-center gap-4">
        {/* System Health / Status Indicator */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-[#EAF8EF] border border-[#bbf7d0] rounded-full text-xs font-medium text-[#15803D]">
          <span className="w-2 h-2 rounded-full bg-[#15803D] animate-pulse"></span>
          <span>FastAPI Engine Ready</span>
        </div>

        {/* User preview */}
        <div className="flex items-center gap-3 pl-2 sm:border-l sm:border-[#DCE5EF]">
          <div className="text-right hidden sm:block">
            <span className="block text-sm font-semibold text-[#172B42]">
              {user?.first_name} {user?.last_name}
            </span>
            <span className="block text-xs text-[#66778B]">{user?.email}</span>
          </div>
          <Badge variant={isAdmin ? 'primary' : 'neutral'}>
            {isAdmin ? 'ADMIN' : 'USER'}
          </Badge>
          <button
            onClick={logout}
            className="p-2 text-[#66778B] hover:text-[#B42318] hover:bg-[#FEF0EF] rounded-radius-sm transition-colors cursor-pointer"
            title="Sign out"
            aria-label="Sign out"
          >
            <LogOutIcon className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
