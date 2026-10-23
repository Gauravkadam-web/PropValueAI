import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'primary' | 'success' | 'warning' | 'danger' | 'neutral';
  className?: string;
}

export function Badge({ children, variant = 'neutral', className = '' }: BadgeProps) {
  const variantStyles = {
    primary: 'bg-[#E8F1FF] text-[#1769E0] border border-[#b2ccff]',
    success: 'bg-[#EAF8EF] text-[#15803D] border border-[#bbf7d0]',
    warning: 'bg-[#FFF7E6] text-[#B45309] border border-[#fedf89]',
    danger: 'bg-[#FEF0EF] text-[#B42318] border border-[#fecdca]',
    neutral: 'bg-[#F4F7FB] text-[#66778B] border border-[#DCE5EF]',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
