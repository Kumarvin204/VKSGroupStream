import React from 'react';

const Input = React.forwardRef(({ 
  label, 
  error, 
  helperText, 
  type = 'text', 
  textarea = false, 
  className = '', 
  id,
  rows = 4,
  ...props 
}, ref) => {
  const inputId = id || label?.toLowerCase().replace(/\s+/g, '-');
  
  const baseClasses = `bg-surface-800 border ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : 'border-surface-600 focus:border-brand-500 focus:ring-brand-500/20'} text-white rounded-xl px-4 py-3 placeholder-surface-400 focus:outline-none focus:ring-2 transition-all duration-200 w-full disabled:opacity-50 disabled:cursor-not-allowed ${className}`;

  return (
    <div className="w-full">
      {label && (
        <label htmlFor={inputId} className="text-sm font-medium text-surface-300 mb-1.5 block">
          {label}
        </label>
      )}
      
      {textarea ? (
        <textarea
          ref={ref}
          id={inputId}
          rows={rows}
          className={baseClasses}
          {...props}
        />
      ) : (
        <input
          ref={ref}
          type={type}
          id={inputId}
          className={baseClasses}
          {...props}
        />
      )}
      
      {error && (
        <p className="text-sm text-red-400 mt-1">{error}</p>
      )}
      
      {helperText && !error && (
        <p className="text-xs text-surface-400 mt-1">{helperText}</p>
      )}
    </div>
  );
});

Input.displayName = 'Input';
export default Input;
