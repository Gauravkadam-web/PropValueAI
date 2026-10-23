import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  className = '',
  children,
  ...props
}: ButtonProps) {
  const baseStyles =
    'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#1769E0] disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer select-none';

  const sizeStyles = {
    sm: 'h-9 px-3 text-sm rounded-radius-sm gap-1.5',
    md: 'h-11 px-4 text-sm rounded-radius-md gap-2',
    lg: 'h-12 px-6 text-base rounded-radius-md gap-2.5',
  };

  const variantStyles = {
    primary: 'bg-[#1769E0] text-white hover:bg-[#1254B8] active:bg-[#0f4496] shadow-sm',
    secondary: 'bg-white text-[#172B42] border border-[#DCE5EF] hover:bg-[#F4F7FB] active:bg-[#E8F1FF]',
    tertiary: 'bg-[#E8F1FF] text-[#1769E0] hover:bg-[#d5e5ff] active:bg-[#bcd6ff]',
    danger: 'bg-[#B42318] text-white hover:bg-[#911c13] active:bg-[#6e150e]',
  };

  return (
    <button
      disabled={disabled || isLoading}
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {isLoading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      )}
      {children}
    </button>
  );
}
