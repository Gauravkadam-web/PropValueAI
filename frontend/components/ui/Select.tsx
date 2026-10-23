import React, { forwardRef } from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: SelectOption[];
  helperText?: string;
  error?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, options, helperText, error, id, className = '', disabled, required, ...props }, ref) => {
    const selectId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={selectId} className="block text-sm font-medium text-[#172B42] mb-1.5">
            {label}
            {required && <span className="text-[#B42318] ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          <select
            id={selectId}
            ref={ref}
            disabled={disabled}
            required={required}
            className={`w-full h-11 px-3 text-base sm:text-sm text-[#172B42] bg-white border ${
              error ? 'border-[#B42318] focus:ring-[#B42318]' : 'border-[#DCE5EF] focus:ring-[#1769E0] focus:border-[#1769E0]'
            } rounded-radius-md transition-colors focus:outline-none focus:ring-2 disabled:bg-[#F4F7FB] disabled:text-[#66778B] disabled:cursor-not-allowed appearance-none cursor-pointer ${className}`}
            {...props}
          >
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-[#66778B]">
            <svg className="h-4 w-4 fill-current" viewBox="0 0 20 20">
              <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
            </svg>
          </div>
        </div>
        {error && <p className="mt-1.5 text-xs text-[#B42318] font-medium">{error}</p>}
        {!error && helperText && <p className="mt-1.5 text-xs text-[#66778B]">{helperText}</p>}
      </div>
    );
  }
);

Select.displayName = 'Select';
