import React from 'react';
import Link from 'next/link';
import { MANDATORY_DISCLAIMER_TEXT } from '@/components/ui/DisclaimerBanner';

export function Footer() {
  return (
    <footer className="bg-white border-t border-[#DCE5EF] py-10 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-start justify-between gap-8 pb-8 border-b border-[#DCE5EF]">
          <div className="max-w-md">
            <span className="text-lg font-bold text-[#10243A]">
              PropValue<span className="text-[#1769E0]">AI</span>
            </span>
            <p className="mt-2 text-sm text-[#66778B] leading-relaxed">
              Residential property price estimation using Python, machine learning, and decoupled Spring Boot architecture.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-8 text-sm">
            <div>
              <h4 className="font-semibold text-[#10243A] mb-3">Navigation</h4>
              <ul className="space-y-2">
                <li>
                  <Link href="/" className="text-[#66778B] hover:text-[#1769E0] transition-colors">
                    Home
                  </Link>
                </li>
                <li>
                  <Link href="/login" className="text-[#66778B] hover:text-[#1769E0] transition-colors">
                    Sign In
                  </Link>
                </li>
                <li>
                  <Link href="/register" className="text-[#66778B] hover:text-[#1769E0] transition-colors">
                    Register
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-[#10243A] mb-3">Engineering</h4>
              <ul className="space-y-2">
                <li>
                  <a
                    href="https://github.com/Gauravkadam-web/PropValueAI"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[#66778B] hover:text-[#1769E0] transition-colors"
                  >
                    GitHub Source
                  </a>
                </li>
                <li>
                  <span className="text-xs text-[#66778B] block">Next.js 16 + Spring Boot 3 + FastAPI</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div className="pt-6 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-[#66778B]">
          <p>© 2026 PropValueAI. Educational Demonstration Project.</p>
          <p className="text-center md:text-right max-w-xl">
            <strong>Disclaimer:</strong> {MANDATORY_DISCLAIMER_TEXT}
          </p>
        </div>
      </div>
    </footer>
  );
}
