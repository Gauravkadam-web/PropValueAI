 'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/AuthContext';
import { api } from '@/lib/api/client';
import { PredictionHistoryItem } from '@/types/api';
import { AppShell } from '@/components/layout/AppShell';
import { Card, CardHeader } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import {
  CalculatorIcon,
  HistoryIcon,
  ShieldIcon,
  BuildingIcon,
  CheckCircleIcon,
  ChevronRightIcon,
} from '@/components/ui/Icons';

export default function DashboardPage() {
  const { user, token, isAdmin } = useAuth();
  const [recentItems, setRecentItems] = useState<PredictionHistoryItem[]>([]);
  const [totalCount, setTotalCount] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadDashboardData() {
      if (!token) return;
      try {
        const pageResponse = await api.predictions.getHistory(0, 5, token);
        setRecentItems(pageResponse.content);
        setTotalCount(pageResponse.total_elements);
      } catch {
        // Fallback gracefully without breaking page
      } finally {
        setIsLoading(false);
      }
    }

    loadDashboardData();
  }, [token]);

  return (
    <AppShell title="Dashboard">
      {/* Welcome Section */}
      <div className="bg-white border border-[#DCE5EF] rounded-radius-lg p-6 sm:p-8 shadow-card flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold uppercase tracking-wider text-[#1769E0]">
              User Workspace
            </span>
            <span>•</span>
            <Badge variant={isAdmin ? 'primary' : 'neutral'}>
              {isAdmin ? 'ADMINISTRATOR' : 'VERIFIED USER'}
            </Badge>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#10243A] tracking-tight">
            Welcome back, {user?.first_name} {user?.last_name}
          </h2>
          <p className="text-sm text-[#66778B] mt-1">
            Execute residential valuations, view historical records, and inspect model telemetry.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Link href="/predictions/new">
            <Button size="md" variant="primary">
              <CalculatorIcon className="w-4 h-4" />
              New Valuation
            </Button>
          </Link>
          <Link href="/predictions">
            <Button size="md" variant="secondary">
              <HistoryIcon className="w-4 h-4" />
              View History
            </Button>
          </Link>
        </div>
      </div>

      {/* System & Architecture Info Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="hover:border-[#1769E0]/40 transition-colors">
          <span className="text-xs font-semibold text-[#66778B] uppercase tracking-wider block">
            My Valuations
          </span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-[#10243A] tabular-nums">
              {totalCount !== null ? totalCount : '—'}
            </span>
            <span className="text-xs text-[#66778B]">persisted records</span>
          </div>
        </Card>

        <Card className="hover:border-[#1769E0]/40 transition-colors">
          <span className="text-xs font-semibold text-[#66778B] uppercase tracking-wider block">
            Fitted Model
          </span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-xl font-bold text-[#10243A]">Random Forest</span>
            <Badge variant="primary" className="text-[10px]">v1.0.0</Badge>
          </div>
          <span className="text-xs text-[#66778B] mt-1 block">scikit-learn pipeline</span>
        </Card>

        <Card className="hover:border-[#1769E0]/40 transition-colors">
          <span className="text-xs font-semibold text-[#66778B] uppercase tracking-wider block">
            Target Unit
          </span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-xl font-bold text-[#10243A]">Lakhs INR</span>
          </div>
          <span className="text-xs text-[#66778B] mt-1 block">1 Lakh = 100,000 INR</span>
        </Card>

        <Card className="hover:border-[#1769E0]/40 transition-colors">
          <span className="text-xs font-semibold text-[#66778B] uppercase tracking-wider block">
            Backend Tier
          </span>
          <div className="mt-2 flex items-center gap-1.5 text-[#15803D]">
            <CheckCircleIcon className="w-4 h-4 shrink-0" />
            <span className="text-sm font-bold text-[#10243A]">Spring Boot + JPA</span>
          </div>
          <span className="text-xs text-[#66778B] mt-1 block">PostgreSQL + Flyway</span>
        </Card>
      </div>

      {/* Recent Predictions Preview Table */}
      <Card>
        <CardHeader
          title="Recent Valuations"
          subtitle="Latest property valuation records associated with your account"
          action={
            <Link href="/predictions">
              <Button size="sm" variant="secondary">
                View All Records
                <ChevronRightIcon className="w-3.5 h-3.5" />
              </Button>
            </Link>
          }
        />

        {isLoading ? (
          <div className="py-8 text-center text-sm text-[#66778B]">
            Loading recent valuations...
          </div>
        ) : recentItems.length === 0 ? (
          <div className="py-8 text-center text-sm text-[#66778B]">
            No recent valuations. Click &ldquo;New Valuation&rdquo; to estimate your first property price.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="border-b border-[#DCE5EF] text-xs font-semibold text-[#66778B] uppercase">
                  <th className="py-2.5 px-3">Record ID</th>
                  <th className="py-2.5 px-3">Date</th>
                  <th className="py-2.5 px-3">Area (SqFt)</th>
                  <th className="py-2.5 px-3">Size</th>
                  <th className="py-2.5 px-3 text-right">Predicted Price</th>
                  <th className="py-2.5 px-3 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#DCE5EF]">
                {recentItems.map((item) => {
                  const formatted = typeof item.predicted_price === 'number'
                    ? item.predicted_price.toFixed(2)
                    : item.predicted_price;
                  return (
                    <tr key={item.id} className="hover:bg-[#F4F7FB]/50">
                      <td className="py-3 px-3 font-semibold text-[#10243A]">#{item.id}</td>
                      <td className="py-3 px-3 text-[#66778B]">
                        {new Date(item.created_at).toLocaleDateString('en-IN', {
                          month: 'short',
                          day: 'numeric',
                        })}
                      </td>
                      <td className="py-3 px-3 text-[#172B42] font-medium tabular-nums">{item.total_sqft} sqft</td>
                      <td className="py-3 px-3 text-[#172B42]">{item.size || '—'}</td>
                      <td className="py-3 px-3 text-right font-bold text-[#10243A] tabular-nums">
                        ₹ {formatted} {item.target_unit || 'Lakhs'}
                      </td>
                      <td className="py-3 px-3 text-right">
                        <Link href={`/predictions/${item.id}`}>
                          <span className="text-xs font-semibold text-[#1769E0] hover:underline cursor-pointer">
                            View →
                          </span>
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </AppShell>
  );
}
