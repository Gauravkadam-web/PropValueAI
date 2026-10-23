import React, { forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, helperText, error, id, className = '', disabled, required, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="block text-sm font-medium text-[#172B42] mb-1.5">
            {label}
            {required && <span className="text-[#B42318] ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <input
            id={inputId}
            ref={ref}
            disabled={disabled}
            required={required}
            className={`w-full h-11 px-3 text-base sm:text-sm text-[#172B42] bg-white border ${
              error ? 'border-[#B42318] focus:ring-[#B42318]' : 'border-[#DCE5EF] focus:ring-[#1769E0] focus:border-[#1769E0]'
            } rounded-radius-md placeholder-[#66778B] transition-colors focus:outline-none focus:ring-2 disabled:bg-[#F4F7FB] disabled:text-[#66778B] disabled:cursor-not-allowed ${className}`}
            {...props}
          />
        </div>
        {error && <p className="mt-1.5 text-xs text-[#B42318] font-medium">{error}</p>}
        {!error && helperText && <p className="mt-1.5 text-xs text-[#66778B]">{helperText}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';
