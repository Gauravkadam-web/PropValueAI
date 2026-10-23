import React from 'react';
import Link from 'next/link';
import { PredictionResponse } from '@/types/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { CheckCircleIcon, CalculatorIcon, HistoryIcon } from '@/components/ui/Icons';
import { MANDATORY_DISCLAIMER_TEXT } from '@/components/ui/DisclaimerBanner';

interface PredictionResultCardProps {
  result: PredictionResponse;
  onReset?: () => void;
}

export function PredictionResultCard({ result, onReset }: PredictionResultCardProps) {
  // Format price with 2 decimals
  const formattedPrice = typeof result.predicted_price === 'number'
    ? result.predicted_price.toFixed(2)
    : result.predicted_price;

  return (
    <Card padding="none" className="overflow-hidden border-2 border-[#1769E0]/20 animate-in fade-in duration-300">
      {/* Top Banner */}
      <div className="bg-[#10243A] text-white p-6 sm:p-8">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-[#15803D]/20 text-[#4ade80] flex items-center justify-center">
              <CheckCircleIcon className="w-5 h-5 text-[#4ade80]" />
            </div>
            <span className="text-sm font-semibold uppercase tracking-wider text-[#A2B4C9]">
              ML Valuation Computed
            </span>
          </div>
          <Badge variant="primary" className="bg-[#1769E0] text-white border-0">
            {result.model_name} v{result.model_version}
          </Badge>
        </div>

        <div className="mt-2">
          <span className="text-xs sm:text-sm text-[#A2B4C9] block font-medium">Estimated Property Value:</span>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-tight tabular-nums">
              ₹ {formattedPrice}
            </span>
            <span className="text-lg sm:text-xl font-bold text-[#A2B4C9]">
              {result.target_unit || 'Lakhs INR'}
            </span>
          </div>
        </div>
      </div>

      {/* Metadata & Details */}
      <div className="p-6 sm:p-8 bg-white space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 pb-6 border-b border-[#DCE5EF] text-sm">
          <div>
            <span className="text-xs text-[#66778B] block font-medium">Record ID</span>
            <span className="font-semibold text-[#172B42] tabular-nums">#{result.id}</span>
          </div>
          <div>
            <span className="text-xs text-[#66778B] block font-medium">FastAPI Prediction ID</span>
            <span className="font-mono text-xs text-[#172B42] break-all">{result.fastapi_prediction_id}</span>
          </div>
          <div>
            <span className="text-xs text-[#66778B] block font-medium">Timestamp</span>
            <span className="text-[#172B42]">
              {new Date(result.created_at).toLocaleString('en-IN', {
                dateStyle: 'medium',
                timeStyle: 'short',
              })}
            </span>
          </div>
        </div>

        {/* Mandatory Disclaimer Display */}
        <div className="bg-[#FFF7E6] border border-[#fedf89] rounded-radius-md p-4 text-xs sm:text-sm text-[#B45309]">
          <strong className="block font-semibold mb-1">Mandatory Disclaimer:</strong>
          <p className="text-[#78350f]">{result.disclaimer || MANDATORY_DISCLAIMER_TEXT}</p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
          {onReset && (
            <Button onClick={onReset} variant="primary" className="w-full sm:w-auto">
              <CalculatorIcon className="w-4 h-4" />
              New Valuation Request
            </Button>
          )}
          <Link href="/predictions" className="w-full sm:w-auto">
            <Button variant="secondary" className="w-full sm:w-auto">
              <HistoryIcon className="w-4 h-4" />
              View Prediction History
            </Button>
          </Link>
        </div>
      </div>
    </Card>
  );
}
