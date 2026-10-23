'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@/lib/auth/AuthContext';
import { api, ApiError } from '@/lib/api/client';
import { PredictionHistoryItem } from '@/types/api';
import { AppShell } from '@/components/layout/AppShell';
import { PredictionHistoryTable } from '@/components/prediction/PredictionHistoryTable';
import { Alert } from '@/components/ui/Alert';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { ShieldIcon } from '@/components/ui/Icons';

export default function AdminPredictionsPage() {
  const { token, isAdmin } = useAuth();
  const [items, setItems] = useState<PredictionHistoryItem[]>([]);
  const [page, setPage] = useState<number>(0);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalElements, setTotalElements] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fetchAdminHistory = useCallback(async (targetPage: number) => {
    if (!token) return;
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const response = await api.admin.getAllPredictions(targetPage, 10, token);
      setItems(response.content);
      setPage(response.page);
      setTotalPages(response.total_pages);
      setTotalElements(response.total_elements);
    } catch (err) {
      if (err instanceof ApiError) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Failed to retrieve system-wide prediction history.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [token]);

  useEffect(() => {
    if (isAdmin) {
      fetchAdminHistory(page);
    }
  }, [fetchAdminHistory, isAdmin, page]);

  return (
    <AppShell title="System Audit & Prediction History" adminOnly={true}>
      <div className="space-y-6">
        <div className="bg-white border border-[#DCE5EF] rounded-radius-lg p-6 shadow-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-radius-md bg-[#E8F1FF] text-[#1769E0] flex items-center justify-center">
              <ShieldIcon className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-[#10243A]">System-Wide Prediction Audit</h2>
                <Badge variant="primary">ROLE_ADMIN</Badge>
              </div>
              <p className="text-sm text-[#66778B] mt-0.5">
                Full platform persistence log queried from Spring Boot administrative endpoint.
              </p>
            </div>
          </div>

          <div className="text-right">
            <span className="text-xs text-[#66778B] block font-medium">Total Platform Valuations</span>
            <span className="text-2xl font-bold text-[#10243A] tabular-nums">{totalElements}</span>
          </div>
        </div>

        {errorMessage && (
          <Alert variant="danger" title="Administrative Access Error">
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
          isAdminView={true}
        />
      </div>
    </AppShell>
  );
}
