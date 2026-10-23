import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  padding?: 'sm' | 'md' | 'lg' | 'none';
  className?: string;
}

export function Card({ children, padding = 'md', className = '', ...props }: CardProps) {
  const paddingStyles = {
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div
      className={`bg-white border border-[#DCE5EF] rounded-radius-lg shadow-card ${paddingStyles[padding]} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, action, className = '' }: { title: string; subtitle?: string; action?: React.ReactNode; className?: string }) {
  return (
    <div className={`flex flex-col sm:flex-row sm:items-center sm:justify-between pb-4 mb-4 border-b border-[#DCE5EF] gap-2 ${className}`}>
      <div>
        <h3 className="text-lg font-semibold text-[#10243A]">{title}</h3>
        {subtitle && <p className="text-sm text-[#66778B] mt-0.5">{subtitle}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
}
