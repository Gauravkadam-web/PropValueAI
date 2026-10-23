'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth/AuthContext';
import {
  HomeIcon,
  CalculatorIcon,
  HistoryIcon,
  ShieldIcon,
  BuildingIcon,
  LogOutIcon,
  UserIcon,
} from '@/components/ui/Icons';
import { Badge } from '@/components/ui/Badge';

interface AppSidebarProps {
  onCloseMobile?: () => void;
}

export function AppSidebar({ onCloseMobile }: AppSidebarProps) {
  const pathname = usePathname();
  const { user, isAdmin, logout } = useAuth();

  const navItems = [
    {
      label: 'Dashboard',
      href: '/dashboard',
      icon: <HomeIcon className="w-5 h-5 shrink-0" />,
      active: pathname === '/dashboard',
    },
    {
      label: 'New Prediction',
      href: '/predictions/new',
      icon: <CalculatorIcon className="w-5 h-5 shrink-0" />,
      active: pathname === '/predictions/new',
    },
    {
      label: 'My Predictions',
      href: '/predictions',
      icon: <HistoryIcon className="w-5 h-5 shrink-0" />,
      active: pathname === '/predictions' || (pathname.startsWith('/predictions/') && pathname !== '/predictions/new'),
    },
  ];

  if (isAdmin) {
    navItems.push({
      label: 'Admin History',
      href: '/admin',
      icon: <ShieldIcon className="w-5 h-5 shrink-0" />,
      active: pathname === '/admin',
    });
  }

  return (
    <aside className="w-[248px] h-screen bg-[#10243A] text-white flex flex-col shrink-0 select-none border-r border-[#183652]">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 border-b border-[#183652] gap-3">
        <div className="w-9 h-9 rounded-radius-md bg-[#1769E0] flex items-center justify-center text-white shadow-sm">
          <BuildingIcon className="w-5 h-5" />
        </div>
        <div>
          <span className="font-bold text-base tracking-tight text-white block leading-tight">
            PropValue<span className="text-[#1769E0]">AI</span>
          </span>
          <span className="text-[10px] text-[#A2B4C9] font-medium uppercase tracking-wider">
            Real Estate ML
          </span>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-6 space-y-1.5 overflow-y-auto">
        <div className="px-3 pb-2 text-[11px] font-semibold text-[#A2B4C9] uppercase tracking-wider">
          Main Menu
        </div>
        {navItems.map((item) => {
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onCloseMobile}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-radius-md text-sm font-medium transition-all ${
                item.active
                  ? 'bg-[#1769E0] text-white shadow-sm'
                  : 'text-[#DCE5EF] hover:bg-[#183652] hover:text-white'
              }`}
            >
              {item.icon}
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* User Section & Logout */}
      <div className="p-4 border-t border-[#183652] bg-[#0c1c2e]">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-9 h-9 rounded-full bg-[#183652] border border-[#2b4c6e] flex items-center justify-center text-white shrink-0">
            <UserIcon className="w-4 h-4 text-[#A2B4C9]" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-semibold text-white truncate">
              {user?.first_name} {user?.last_name}
            </div>
            <div className="text-xs text-[#A2B4C9] truncate">{user?.email}</div>
          </div>
        </div>
        <div className="flex items-center justify-between">
          <Badge variant={isAdmin ? 'primary' : 'neutral'} className="text-[10px]">
            {isAdmin ? 'ADMIN' : 'USER'}
          </Badge>
          <button
            onClick={logout}
            className="inline-flex items-center gap-1.5 text-xs text-[#A2B4C9] hover:text-[#FEF0EF] hover:underline transition-colors cursor-pointer"
            title="Sign out"
          >
            <LogOutIcon className="w-3.5 h-3.5" />
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
