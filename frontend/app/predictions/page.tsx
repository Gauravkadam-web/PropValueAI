'use client';

import React, { useEffect, useState, useCallback } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/AuthContext';
import { api, ApiError } from '@/lib/api/client';
import { PredictionHistoryItem } from '@/types/api';
import { AppShell } from '@/components/layout/AppShell';
import { PredictionHistoryTable } from '@/components/prediction/PredictionHistoryTable';
import { Button } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Alert';
import { CalculatorIcon } from '@/components/ui/Icons';

export default function MyPredictionsPage() {
  const { token } = useAuth();
  const [items, setItems] = useState<PredictionHistoryItem[]>([]);
  const [page, setPage] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalElements, setTotalElements] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fetchHistory = useCallback(async (targetPage: number) => {
    if (!token) return;
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const response = await api.predictions.getHistory(targetPage, 10, token);
      setItems(response.content);
      setPage(response.page);
      setTotalPages(response.total_pages);
      setTotalElements(response.total_elements);
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Failed to load prediction history. Please check connection to the backend.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchHistory(page);
  }, [fetchHistory, page]);

  return (
    <AppShell title="My Prediction History">
      <div className="space-y-6">
        {/* Header action bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-[#10243A]">Personal Valuation History</h2>
            <p className="text-sm text-[#66778B] mt-0.5">
              Historical records of your residential property valuations sorted chronologically.
            </p>
          </div>
          <Link href="/predictions/new">
            <Button variant="primary">
              <CalculatorIcon className="w-4 h-4" />
              New Valuation
            </Button>
          </Link>
        </div>

        {errorMessage && (
          <Alert variant="danger" title="Error Loading History">
            {errorMessage}
          </Alert>
        )}

        <PredictionHistoryTable
          items={items}
          isLoading={isLoading}
          page={page}
          totalPages={totalPages}
          totalElements={totalElements}
          onPageChange={(newPage) => setPage(newPage)}
        />
      </div>
    </AppShell>
  );
}
