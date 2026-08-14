import React from 'react';

const Button = React.forwardRef(({ 
  variant = 'primary', 
  size = 'md', 
  isLoading = false, 
  icon, 
  children, 
  className = '', 
  disabled,
  ...props 
}, ref) => {
  const baseStyles = 'inline-flex items-center justify-center transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-surface-900 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-brand-600 hover:bg-brand-500 text-white font-semibold rounded-xl shadow-[0_0_15px_rgba(139,92,246,0.3)] hover:shadow-[0_0_25px_rgba(139,92,246,0.5)] focus:ring-brand-400',
    secondary: 'bg-surface-800 hover:bg-surface-700 text-surface-200 border border-surface-600 hover:border-surface-500 rounded-xl focus:ring-surface-400',
    danger: 'bg-red-600 hover:bg-red-500 text-white rounded-xl focus:ring-red-400',
    live: 'bg-red-600 hover:bg-red-500 text-white font-bold rounded-xl shadow-lg shadow-red-500/30 hover:shadow-red-500/50 animate-pulse-slow focus:ring-red-400'
  };

  const sizes = {
    sm: 'py-1.5 px-4 text-sm',
    md: 'py-2.5 px-6 text-base',
    lg: 'py-3 px-8 text-lg'
  };

  return (
    <button
      ref={ref}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      )}
      {!isLoading && icon && (
        <span className="mr-2">{icon}</span>
      )}
      {children}
    </button>
  );
});

Button.displayName = 'Button';
export default Button;
