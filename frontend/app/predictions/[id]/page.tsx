'use client';

import React, { useEffect, useState, use, Suspense } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/AuthContext';
import { api, ApiError } from '@/lib/api/client';
import { PredictionHistoryItem } from '@/types/api';
import { AppShell } from '@/components/layout/AppShell';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { Alert } from '@/components/ui/Alert';
import { ChevronLeftIcon, CalculatorIcon, HistoryIcon } from '@/components/ui/Icons';
import { MANDATORY_DISCLAIMER_TEXT } from '@/components/ui/DisclaimerBanner';


function PredictionDetailContent({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const predictionId = parseInt(resolvedParams.id, 10);
  const { token } = useAuth();

  const [record, setRecord] = useState<PredictionHistoryItem | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<{ status: number; message: string } | null>(null);

  useEffect(() => {
    async function loadRecord() {
      if (!token || isNaN(predictionId)) return;
      setIsLoading(true);
      setError(null);

      try {
        const item = await api.predictions.getById(predictionId, token);
        setRecord(item);
      } catch (err) {
        if (err instanceof ApiError) {
          setError({ status: err.status, message: err.message });
        } else {
          setError({ status: 500, message: 'Failed to retrieve prediction record.' });
        }
      } finally {
        setIsLoading(false);
      }
    }

    loadRecord();
  }, [token, predictionId]);

  return (
    <AppShell title={`Valuation Record #${predictionId || ''}`}>
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Navigation Breadcrumb */}
        <div>
          <Link href="/predictions">
            <span className="inline-flex items-center gap-1.5 text-sm font-medium text-[#1769E0] hover:underline cursor-pointer">
              <ChevronLeftIcon className="w-4 h-4" />
              Back to Prediction History
            </span>
          </Link>
        </div>

        {isLoading ? (
          <Card className="text-center py-16">
            <div className="w-8 h-8 border-3 border-[#DCE5EF] border-t-[#1769E0] rounded-full animate-spin mx-auto mb-3" />
            <p className="text-sm text-[#66778B]">Retrieving valuation record...</p>
          </Card>
        ) : error ? (
          <Card>
            <Alert
              variant={error.status === 403 ? 'warning' : 'danger'}
              title={error.status === 403 ? 'Access Restricted' : 'Record Error'}
            >
              {error.message}
            </Alert>
            <div className="mt-4 pt-4 border-t border-[#DCE5EF] flex gap-3">
              <Link href="/predictions">
                <Button variant="secondary" size="sm">
                  Return to History
                </Button>
              </Link>
            </div>
          </Card>
        ) : record ? (
          <div className="space-y-6">
            {/* Price Header Card */}
            <Card padding="none" className="overflow-hidden border border-[#DCE5EF]">
              <div className="bg-[#10243A] text-white p-6 sm:p-8">
                <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
                  <span className="text-xs font-semibold text-[#A2B4C9] uppercase tracking-wider">
                    Record #{record.id} • {record.model_name} v{record.model_version}
                  </span>
                  <Badge variant="success" className="bg-[#15803D] text-white border-0">
                    {record.status}
                  </Badge>
                </div>
                <span className="text-xs text-[#A2B4C9] block font-medium">Estimated Valuation:</span>
                <div className="flex items-baseline gap-2 mt-1">
                  <span className="text-3xl sm:text-4xl font-extrabold text-white tabular-nums">
                    ₹ {typeof record.predicted_price === 'number' ? record.predicted_price.toFixed(2) : record.predicted_price}
                  </span>
                  <span className="text-lg font-bold text-[#A2B4C9]">
                    {record.target_unit || 'Lakhs INR'}
                  </span>
                </div>
              </div>

              {/* Property Specs Grid */}
              <div className="p-6 sm:p-8 bg-white space-y-6">
                <h3 className="text-base font-bold text-[#10243A] pb-3 border-b border-[#DCE5EF]">
                  Property Input Specifications
                </h3>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
                  <div className="p-3 bg-[#F4F7FB] rounded-radius-sm">
                    <span className="text-xs text-[#66778B] block font-medium">Total Area</span>
                    <span className="font-bold text-[#10243A] tabular-nums mt-0.5 block">
                      {record.total_sqft} sqft
                    </span>
                  </div>

                  <div className="p-3 bg-[#F4F7FB] rounded-radius-sm">
                    <span className="text-xs text-[#66778B] block font-medium">Configuration</span>
                    <span className="font-bold text-[#10243A] mt-0.5 block">
                      {record.size || '—'}
                    </span>
                  </div>

                  <div className="p-3 bg-[#F4F7FB] rounded-radius-sm">
                    <span className="text-xs text-[#66778B] block font-medium">Bathrooms</span>
                    <span className="font-bold text-[#10243A] tabular-nums mt-0.5 block">
                      {record.bath ?? '—'}
                    </span>
                  </div>

                  <div className="p-3 bg-[#F4F7FB] rounded-radius-sm">
                    <span className="text-xs text-[#66778B] block font-medium">Balconies</span>
                    <span className="font-bold text-[#10243A] tabular-nums mt-0.5 block">
                      {record.balcony ?? '—'}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm pt-2">
                  <div>
                    <span className="text-xs text-[#66778B] block font-medium">Area Classification</span>
                    <span className="text-sm font-semibold text-[#10243A] mt-0.5 block">
                      {record.area_type || '—'}
                    </span>
                  </div>
                  <div>
                    <span className="text-xs text-[#66778B] block font-medium">Valuation Timestamp</span>
                    <span className="text-sm text-[#10243A] mt-0.5 block">
                      {new Date(record.created_at).toLocaleString('en-IN', {
                        dateStyle: 'full',
                        timeStyle: 'medium',
                      })}
                    </span>
                  </div>
                </div>

                {/* Mandatory Disclaimer */}
                <div className="bg-[#FFF7E6] border border-[#fedf89] rounded-radius-md p-4 text-xs sm:text-sm text-[#B45309]">
                  <strong className="block font-semibold mb-1">Educational Notice & Disclaimer:</strong>
                  <p className="text-[#78350f]">{record.disclaimer || MANDATORY_DISCLAIMER_TEXT}</p>
                </div>

                {/* Action buttons */}
                <div className="pt-2 flex gap-3">
                  <Link href="/predictions/new">
                    <Button variant="primary">
                      <CalculatorIcon className="w-4 h-4" />
                      New Valuation Request
                    </Button>
                  </Link>
                  <Link href="/predictions">
                    <Button variant="secondary">
                      <HistoryIcon className="w-4 h-4" />
                      View All Valuations
                    </Button>
                  </Link>
                </div>
              </div>
            </Card>
          </div>
        ) : null}
      </div>
    </AppShell>
  );
}

export default function PredictionDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-[#F4F7FB] flex items-center justify-center p-4">
          <div className="w-8 h-8 border-3 border-[#DCE5EF] border-t-[#1769E0] rounded-full animate-spin" />
        </div>
      }
    >
      <PredictionDetailContent params={params} />
    </Suspense>
  );
}
