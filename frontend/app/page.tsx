'use client';

import React from 'react';
import Link from 'next/link';
import { PublicNavbar } from '@/components/layout/PublicNavbar';
import { Footer } from '@/components/layout/Footer';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { DisclaimerBanner } from '@/components/ui/DisclaimerBanner';
import {
  CalculatorIcon,
  ShieldIcon,
  BuildingIcon,
  HistoryIcon,
  CheckCircleIcon,
} from '@/components/ui/Icons';
import { useAuth } from '@/lib/auth/AuthContext';

export default function LandingPage() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen flex flex-col bg-[#F4F7FB]">
      <PublicNavbar />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-gradient-to-b from-white to-[#F4F7FB] pt-12 pb-20 border-b border-[#DCE5EF]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto text-center space-y-6">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E8F1FF] text-[#1769E0] text-xs font-semibold tracking-wide uppercase border border-[#b2ccff]">
                <span>Educational ML Platform</span>
                <span>•</span>
                <span>Pune Residential Market</span>
              </div>

              <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-[#10243A] tracking-tight leading-tight">
                Simulated Real Estate Price Prediction with Machine Learning
              </h1>

              <p className="text-base sm:text-lg text-[#66778B] max-w-2xl mx-auto leading-relaxed">
                Estimate residential property values from historical Pune housing attributes using a fitted scikit-learn regression pipeline orchestrated by Spring Boot and Python FastAPI.
              </p>

              <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-4">
                {isAuthenticated ? (
                  <Link href="/dashboard" className="w-full sm:w-auto">
                    <Button size="lg" variant="primary" className="w-full sm:w-auto">
                      Go to Dashboard
                    </Button>
                  </Link>
                ) : (
                  <>
                    <Link href="/register" className="w-full sm:w-auto">
                      <Button size="lg" variant="primary" className="w-full sm:w-auto">
                        Get Started (Create Account)
                      </Button>
                    </Link>
                    <Link href="/login" className="w-full sm:w-auto">
                      <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                        Sign In to Existing Account
                      </Button>
                    </Link>
                  </>
                )}
              </div>

              {/* Mandatory Disclaimer inside Hero */}
              <div className="pt-4 max-w-2xl mx-auto text-left">
                <DisclaimerBanner />
              </div>
            </div>
          </div>
        </section>

        {/* Feature Grid grounded in actual implementation */}
        <section className="py-16 sm:py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-[#10243A] tracking-tight">
              Production-Grade Decoupled Architecture
            </h2>
            <p className="text-sm text-[#66778B] mt-2">
              Engineered with clean architectural boundaries across frontend, application backend, and inference services.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="hover:shadow-dropdown transition-shadow">
              <div className="w-10 h-10 rounded-radius-md bg-[#E8F1FF] text-[#1769E0] flex items-center justify-center mb-4">
                <CalculatorIcon className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold text-[#10243A] mb-2">Fitted ML Pipeline</h3>
              <p className="text-sm text-[#66778B] leading-relaxed">
                Offline-trained scikit-learn model executing automated preprocessing, range parsing, and outlier handling for accurate valuation estimations.
              </p>
            </Card>

            <Card className="hover:shadow-dropdown transition-shadow">
              <div className="w-10 h-10 rounded-radius-md bg-[#EAF8EF] text-[#15803D] flex items-center justify-center mb-4">
                <ShieldIcon className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold text-[#10243A] mb-2">Stateless JWT Security</h3>
              <p className="text-sm text-[#66778B] leading-relaxed">
                Role-based access control with BCrypt password hashing. Authentication is required for every prediction request to maintain audit integrity.
              </p>
            </Card>

            <Card className="hover:shadow-dropdown transition-shadow">
              <div className="w-10 h-10 rounded-radius-md bg-[#FFF7E6] text-[#B45309] flex items-center justify-center mb-4">
                <HistoryIcon className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-semibold text-[#10243A] mb-2">Deterministic History</h3>
              <p className="text-sm text-[#66778B] leading-relaxed">
                PostgreSQL persistence with Flyway migrations. Deterministic secondary sorting guarantees consistent history pagination for all users.
              </p>
            </Card>
          </div>
        </section>

        {/* Input Parameters Supported */}
        <section className="bg-white py-16 border-t border-[#DCE5EF]">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-10">
              <h2 className="text-2xl font-bold text-[#10243A]">Verified Prediction Feature Set</h2>
              <p className="text-sm text-[#66778B] mt-1">
                The model accepts standard property parameters verified during exploratory data analysis.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 rounded-radius-md bg-[#F4F7FB] border border-[#DCE5EF]">
                <span className="text-xs font-semibold text-[#1769E0] block uppercase">Dimension</span>
                <span className="text-sm font-bold text-[#10243A] block mt-1">Total Square Feet</span>
                <span className="text-xs text-[#66778B] mt-1 block">Property area in square feet (e.g., 1200)</span>
              </div>
              <div className="p-4 rounded-radius-md bg-[#F4F7FB] border border-[#DCE5EF]">
                <span className="text-xs font-semibold text-[#1769E0] block uppercase">Layout</span>
                <span className="text-sm font-bold text-[#10243A] block mt-1">BHK Configuration</span>
                <span className="text-xs text-[#66778B] mt-1 block">Number of bedrooms (1 BHK to 5 BHK)</span>
              </div>
              <div className="p-4 rounded-radius-md bg-[#F4F7FB] border border-[#DCE5EF]">
                <span className="text-xs font-semibold text-[#1769E0] block uppercase">Amenities</span>
                <span className="text-sm font-bold text-[#10243A] block mt-1">Baths & Balconies</span>
                <span className="text-xs text-[#66778B] mt-1 block">Count of bathrooms and outdoor balconies</span>
              </div>
              <div className="p-4 rounded-radius-md bg-[#F4F7FB] border border-[#DCE5EF]">
                <span className="text-xs font-semibold text-[#1769E0] block uppercase">Deed Category</span>
                <span className="text-sm font-bold text-[#10243A] block mt-1">Area Type</span>
                <span className="text-xs text-[#66778B] mt-1 block">Super built-up, Plot, Built-up, or Carpet</span>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
