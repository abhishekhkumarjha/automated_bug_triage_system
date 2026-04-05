import React from 'react';
import { cn } from '@/src/lib/utils';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'error' | 'info' | 'default';
  className?: string;
}

export const Badge = ({ children, variant = 'default', className }: BadgeProps) => {
  const variants = {
    default: 'bg-slate-100 text-slate-700',
    success: 'bg-emerald-100 text-emerald-700',
    warning: 'bg-amber-100 text-amber-700',
    error: 'bg-rose-100 text-rose-700',
    info: 'bg-sky-100 text-sky-700',
  };

  return (
    <span className={cn('px-2 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider', variants[variant], className)}>
      {children}
    </span>
  );
};
