'use client';

import React from 'react';
import Link from 'next/link';
import { useSession, signIn, signOut } from 'next-auth/react';
import Button from '@/components/ui/Button';

export default function Navbar() {
  const { data: session, status } = useSession();
  const [isGuest, setIsGuest] = React.useState(false);

  React.useEffect(() => {
    const checkGuest = () => {
      const guest = typeof window !== 'undefined' && localStorage.getItem('guestMode') === 'true';
      setIsGuest(guest);
    };
    checkGuest();
    
    // Set up a quick check interval to update when routing changes locally
    const interval = setInterval(checkGuest, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSignOut = () => {
    if (isGuest) {
      localStorage.removeItem('guestMode');
      setIsGuest(false);
      window.location.href = '/';
    } else {
      signOut({ callbackUrl: '/' });
    }
  };

  const isLoggedIn = session || isGuest;

  return (
    <nav className="fixed top-0 left-0 w-full h-16 bg-surface-950/80 backdrop-blur-xl border-b border-surface-800/50 z-50 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
        <div className="flex items-center justify-between h-full">
          
          {/* Left: Logo */}
          <div className="flex items-center flex-shrink-0">
            <Link href={isLoggedIn ? '/dashboard' : '/'} className="flex items-center gap-2 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center shadow-lg shadow-brand-500/20 group-hover:shadow-brand-500/40 transition-all duration-300">
                <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white to-surface-300 bg-clip-text text-transparent group-hover:from-brand-200 group-hover:to-white transition-all duration-300">
                VKSGroupStream
              </span>
            </Link>
          </div>

          {/* Center: Links */}
          {isLoggedIn && (
            <div className="hidden md:flex items-center space-x-1">
              <Link href="/dashboard" className="px-4 py-2 text-sm font-medium text-surface-200 hover:text-white hover:bg-surface-800/50 rounded-lg transition-all duration-200">
                Dashboard
              </Link>
              <Link href="/studio/manual" className="px-4 py-2 text-sm font-medium text-surface-200 hover:text-white hover:bg-surface-800/50 rounded-lg transition-all duration-200">
                Studio
              </Link>
            </div>
          )}

          {/* Right: Auth / User */}
          <div className="flex items-center gap-4">
            {status === 'loading' && !isGuest ? (
              <div className="w-24 h-8 bg-surface-800 rounded-lg animate-pulse"></div>
            ) : isLoggedIn ? (
              <div className="flex items-center gap-4">
                <div className="hidden sm:flex items-center gap-3">
                  <span className="text-sm font-medium text-surface-200">
                    {isGuest ? 'Guest Streamer' : session?.user?.name}
                  </span>
                  {isGuest ? (
                    <div className="w-8 h-8 rounded-full bg-brand-600 flex items-center justify-center text-xs font-bold text-white border border-surface-600">
                      G
                    </div>
                  ) : (
                    session?.user?.image && (
                      <img src={session.user.image} alt={session.user.name} className="w-8 h-8 rounded-full border border-surface-600" />
                    )
                  )}
                </div>
                <Button 
                  variant="secondary" 
                  size="sm" 
                  onClick={handleSignOut}
                >
                  Sign Out
                </Button>
              </div>
            ) : (
              <Button 
                variant="primary" 
                size="sm" 
                onClick={() => signIn('google')}
                icon={
                  <svg className="w-4 h-4" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                  </svg>
                }
              >
                Sign In
              </Button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
