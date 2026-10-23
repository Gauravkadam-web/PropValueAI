import React from 'react';
import { AlertCircleIcon, CheckCircleIcon, InfoIcon } from './Icons';

interface AlertProps {
  variant?: 'success' | 'danger' | 'warning' | 'info';
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export function Alert({ variant = 'info', title, children, className = '' }: AlertProps) {
  const styles = {
    success: {
      bg: 'bg-[#EAF8EF]',
      border: 'border-[#bbf7d0]',
      text: 'text-[#15803D]',
      icon: <CheckCircleIcon className="w-5 h-5 text-[#15803D] shrink-0" />,
    },
    danger: {
      bg: 'bg-[#FEF0EF]',
      border: 'border-[#fecdca]',
      text: 'text-[#B42318]',
      icon: <AlertCircleIcon className="w-5 h-5 text-[#B42318] shrink-0" />,
    },
    warning: {
      bg: 'bg-[#FFF7E6]',
      border: 'border-[#fedf89]',
      text: 'text-[#B45309]',
      icon: <AlertCircleIcon className="w-5 h-5 text-[#B45309] shrink-0" />,
    },
    info: {
      bg: 'bg-[#EAF2FF]',
      border: 'border-[#b2ccff]',
      text: 'text-[#1769E0]',
      icon: <InfoIcon className="w-5 h-5 text-[#1769E0] shrink-0" />,
    },
  };

  const current = styles[variant];

  return (
    <div
      role="alert"
      className={`flex items-start gap-3 p-4 rounded-radius-md border ${current.bg} ${current.border} ${className}`}
    >
      <div className="mt-0.5">{current.icon}</div>
      <div className="flex-1 text-sm">
        {title && <h5 className={`font-semibold mb-1 ${current.text}`}>{title}</h5>}
        <div className={current.text}>{children}</div>
      </div>
    </div>
  );
}
