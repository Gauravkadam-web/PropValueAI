'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/AuthContext';
import { BuildingIcon, MenuIcon, CloseIcon } from '@/components/ui/Icons';
import { Button } from '@/components/ui/Button';

export function PublicNavbar() {
  const { isAuthenticated, user } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-sm border-b border-[#DCE5EF]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-radius-md bg-[#10243A] flex items-center justify-center text-white shadow-sm group-hover:bg-[#1769E0] transition-colors">
              <BuildingIcon className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-lg font-bold text-[#10243A] tracking-tight">PropValue<span className="text-[#1769E0]">AI</span></span>
              <span className="hidden sm:block text-[11px] text-[#66778B] font-medium leading-none">Residential Valuation Platform</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/" className="text-sm font-medium text-[#172B42] hover:text-[#1769E0] transition-colors">
              Overview
            </Link>
            <a
              href="https://github.com/Gauravkadam-web/PropValueAI"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-[#66778B] hover:text-[#172B42] transition-colors"
            >
              GitHub Repository
            </a>

            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <span className="text-xs text-[#66778B]">
                  Signed in as <strong className="text-[#172B42]">{user?.first_name}</strong>
                </span>
                <Link href="/dashboard">
                  <Button size="sm" variant="primary">
                    Open Dashboard
                  </Button>
                </Link>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link href="/login">
                  <Button size="sm" variant="secondary">
                    Sign In
                  </Button>
                </Link>
                <Link href="/register">
                  <Button size="sm" variant="primary">
                    Get Started
                  </Button>
                </Link>
              </div>
            )}
          </nav>

          {/* Mobile menu button */}
          <div className="flex md:hidden">
            <button
              type="button"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-radius-sm text-[#172B42] hover:bg-[#F4F7FB] focus:outline-none"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <CloseIcon className="w-6 h-6" /> : <MenuIcon className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-[#DCE5EF] bg-white px-4 pt-2 pb-6 space-y-3">
          <Link
            href="/"
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-base font-medium text-[#172B42] hover:text-[#1769E0]"
          >
            Overview
          </Link>
          <a
            href="https://github.com/Gauravkadam-web/PropValueAI"
            target="_blank"
            rel="noopener noreferrer"
            className="block py-2 text-base font-medium text-[#66778B] hover:text-[#172B42]"
          >
            GitHub Repository
          </a>
          <div className="pt-2 border-t border-[#DCE5EF] flex flex-col gap-2">
            {isAuthenticated ? (
              <Link href="/dashboard" onClick={() => setMobileMenuOpen(false)}>
                <Button className="w-full" variant="primary">
                  Go to Dashboard
                </Button>
              </Link>
            ) : (
              <>
                <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                  <Button className="w-full" variant="secondary">
                    Sign In
                  </Button>
                </Link>
                <Link href="/register" onClick={() => setMobileMenuOpen(false)}>
                  <Button className="w-full" variant="primary">
                    Get Started
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
