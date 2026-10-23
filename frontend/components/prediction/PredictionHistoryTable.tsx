import React from 'react';
import Link from 'next/link';
import { PredictionHistoryItem } from '@/types/api';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';
import { ChevronLeftIcon, ChevronRightIcon, HistoryIcon, CalculatorIcon } from '@/components/ui/Icons';

interface PredictionHistoryTableProps {
  items: PredictionHistoryItem[];
  isLoading?: boolean;
  page: number;
  totalPages: number;
  totalElements: number;
  onPageChange: (newPage: number) => void;
  isAdminView?: boolean;
}

export function PredictionHistoryTable({
  items,
  isLoading = false,
  page,
  totalPages,
  totalElements,
  onPageChange,
  isAdminView = false,
}: PredictionHistoryTableProps) {
  if (isLoading) {
    return (
      <div className="bg-white border border-[#DCE5EF] rounded-radius-lg p-12 text-center shadow-card">
        <div className="w-8 h-8 border-3 border-[#DCE5EF] border-t-[#1769E0] rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm text-[#66778B] font-medium">Loading prediction history...</p>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="bg-white border border-[#DCE5EF] rounded-radius-lg p-12 text-center shadow-card">
        <div className="w-12 h-12 rounded-full bg-[#E8F1FF] text-[#1769E0] flex items-center justify-center mx-auto mb-4">
          <HistoryIcon className="w-6 h-6" />
        </div>
        <h3 className="text-base font-semibold text-[#10243A]">No Prediction History</h3>
        <p className="text-sm text-[#66778B] mt-1 max-w-sm mx-auto">
          {isAdminView
            ? 'No records found across the platform.'
            : 'You haven’t performed any property valuations yet. Create your first valuation to track it here.'}
        </p>
        {!isAdminView && (
          <div className="mt-5">
            <Link href="/predictions/new">
              <Button size="sm" variant="primary">
                <CalculatorIcon className="w-4 h-4" />
                Make First Prediction
              </Button>
            </Link>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="bg-white border border-[#DCE5EF] rounded-radius-lg shadow-card overflow-hidden">
      {/* Table Container with responsive horizontal scroll */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-sm">
          <thead>
            <tr className="bg-[#F4F7FB] border-b border-[#DCE5EF] text-xs font-semibold text-[#66778B] uppercase tracking-wider">
              <th className="py-3 px-4 sm:px-6">Record</th>
              <th className="py-3 px-4">Date</th>
              <th className="py-3 px-4">Total SqFt</th>
              <th className="py-3 px-4">BHK</th>
              <th className="py-3 px-4">Bath / Balcony</th>
              <th className="py-3 px-4">Area Type</th>
              <th className="py-3 px-4 text-right">Predicted Price</th>
              <th className="py-3 px-4 sm:px-6 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#DCE5EF]">
            {items.map((item) => {
              const formattedPrice = typeof item.predicted_price === 'number'
                ? item.predicted_price.toFixed(2)
                : item.predicted_price;

              return (
                <tr key={item.id} className="hover:bg-[#F4F7FB]/60 transition-colors">
                  <td className="py-3.5 px-4 sm:px-6 font-semibold text-[#10243A]">
                    #{item.id}
                  </td>
                  <td className="py-3.5 px-4 text-[#66778B] whitespace-nowrap">
                    {new Date(item.created_at).toLocaleDateString('en-IN', {
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </td>
                  <td className="py-3.5 px-4 text-[#172B42] font-medium tabular-nums">
                    {item.total_sqft} sqft
                  </td>
                  <td className="py-3.5 px-4 text-[#172B42]">
                    {item.size || '—'}
                  </td>
                  <td className="py-3.5 px-4 text-[#66778B]">
                    {item.bath ?? '—'} Bath / {item.balcony ?? '—'} Balc
                  </td>
                  <td className="py-3.5 px-4 text-[#66778B] max-w-[180px] truncate" title={item.area_type || ''}>
                    {item.area_type || '—'}
                  </td>
                  <td className="py-3.5 px-4 text-right whitespace-nowrap">
                    <span className="font-bold text-[#10243A] tabular-nums text-base">
                      ₹ {formattedPrice}
                    </span>
                    <span className="text-xs text-[#66778B] ml-1">
                      {item.target_unit || 'Lakhs'}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 sm:px-6 text-right whitespace-nowrap">
                    <Link href={`/predictions/${item.id}`}>
                      <span className="text-xs font-semibold text-[#1769E0] hover:text-[#1254B8] hover:underline cursor-pointer">
                        Details →
                      </span>
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="py-3 px-4 sm:px-6 border-t border-[#DCE5EF] bg-[#F4F7FB]/40 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[#66778B]">
        <div>
          Showing page <strong className="text-[#172B42]">{page + 1}</strong> of{' '}
          <strong className="text-[#172B42]">{Math.max(totalPages, 1)}</strong> (Total{' '}
          <strong className="text-[#172B42]">{totalElements}</strong> records)
        </div>
        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant="secondary"
            disabled={page <= 0}
            onClick={() => onPageChange(page - 1)}
          >
            <ChevronLeftIcon className="w-3.5 h-3.5" />
            Previous
          </Button>
          <Button
            size="sm"
            variant="secondary"
            disabled={page + 1 >= totalPages}
            onClick={() => onPageChange(page + 1)}
          >
            Next
            <ChevronRightIcon className="w-3.5 h-3.5" />
          </Button>
        </div>
      </div>
    </div>
  );
}
