import React from 'react';
import { InfoIcon } from './Icons';

export const MANDATORY_DISCLAIMER_TEXT =
  'PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.';

interface DisclaimerBannerProps {
  className?: string;
}

export function DisclaimerBanner({ className = '' }: DisclaimerBannerProps) {
  return (
    <div
      role="note"
      aria-label="Educational Disclaimer"
      className={`bg-[#EAF2FF] border border-[#b2ccff] text-[#1769E0] rounded-radius-md p-3.5 flex items-start gap-2.5 text-xs sm:text-sm ${className}`}
    >
      <InfoIcon className="w-5 h-5 text-[#1769E0] shrink-0 mt-0.5" />
      <div>
        <span className="font-semibold block sm:inline mr-1">Educational Notice:</span>
        <span className="text-[#10243A]">{MANDATORY_DISCLAIMER_TEXT}</span>
      </div>
    </div>
  );
}
