'use client';

import { useEffect } from 'react';
import { useSession, signIn } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';

export default function LandingPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (session || (typeof window !== 'undefined' && localStorage.getItem('guestMode') === 'true')) {
      router.push('/dashboard');
    }
  }, [session, router]);

  const handleEnterAsGuest = () => {
    localStorage.setItem('guestMode', 'true');
    router.push('/dashboard');
  };

  if (status === 'loading' || session || (typeof window !== 'undefined' && localStorage.getItem('guestMode') === 'true')) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="relative flex-1 flex flex-col items-center justify-center overflow-hidden py-20 px-4">
      {/* Animated Background Elements */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-600/20 rounded-full blur-3xl -z-10 animate-pulse-slow mix-blend-screen"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-3xl -z-10 animate-pulse-slow mix-blend-screen" style={{ animationDelay: '2s' }}></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-3xl h-full bg-gradient-to-b from-brand-900/10 to-surface-950 -z-20"></div>

      {/* Hero Content */}
      <div className="text-center max-w-4xl mx-auto space-y-8 z-10 relative">
        <div className="inline-block py-1 px-3 rounded-full bg-surface-800/50 border border-surface-700 backdrop-blur-md mb-4 animate-fade-in-up">
          <span className="text-sm font-medium text-brand-300">✨ The easiest way to stream</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
          <span className="bg-gradient-to-r from-white via-brand-100 to-surface-400 bg-clip-text text-transparent">Go Live on</span>
          <br className="hidden md:block" />
          <span className="bg-gradient-to-r from-brand-400 to-indigo-500 bg-clip-text text-transparent drop-shadow-[0_0_30px_rgba(139,92,246,0.3)]"> YouTube</span>
        </h1>
        
        <p className="text-xl md:text-2xl text-surface-300 max-w-2xl mx-auto font-light leading-relaxed animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
          Stream your camera, screen, or pre-recorded videos directly to YouTube Live. No downloads needed.
        </p>

        <div className="pt-8 flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
          <Button 
            size="lg" 
            className="group px-8 py-4 text-lg font-bold rounded-2xl bg-white text-surface-950 hover:bg-surface-100 shadow-[0_0_40px_rgba(255,255,255,0.15)] hover:shadow-[0_0_60px_rgba(255,255,255,0.25)] hover:-translate-y-1 transition-all duration-300 border-none w-full sm:w-auto flex justify-center"
            onClick={() => signIn('google')}
            icon={
              <svg className="w-6 h-6 group-hover:scale-110 transition-transform duration-300" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
            }
          >
            Sign in with Google
          </Button>

          <Button
            size="lg"
            variant="secondary"
            className="px-8 py-4 text-lg font-bold rounded-2xl border border-surface-700/80 hover:bg-surface-800 hover:border-surface-600 transition-all duration-300 w-full sm:w-auto flex justify-center text-white"
            onClick={handleEnterAsGuest}
            icon={<span className="text-xl">🔑</span>}
          >
            Direct Stream Key Mode
          </Button>
        </div>
        <p className="text-sm text-surface-500 mt-4 text-center">No setup required for Direct Mode. Just paste your YouTube Stream Key!</p>
      </div>

      {/* Feature Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto mt-32 px-4 z-10">
        {[
          {
            icon: "📹",
            title: "Live Camera",
            desc: "Broadcast your webcam and mic in real-time with ultra-low latency.",
            color: "from-blue-500/20 to-blue-600/5",
            borderColor: "group-hover:border-blue-500/50"
          },
          {
            icon: "🖥️",
            title: "Screen Share",
            desc: "Share your screen, presentations, or demos with picture-in-picture mode.",
            color: "from-brand-500/20 to-brand-600/5",
            borderColor: "group-hover:border-brand-500/50"
          },
          {
            icon: "⏰",
            title: "24/7 Streaming",
            desc: "Schedule pre-recorded videos to stream automatically, even while you sleep.",
            color: "from-purple-500/20 to-purple-600/5",
            borderColor: "group-hover:border-purple-500/50"
          }
        ].map((feature, i) => (
          <div 
            key={i} 
            className={`group bg-surface-900/50 backdrop-blur-xl border border-surface-800 rounded-2xl p-8 hover:-translate-y-2 transition-all duration-300 shadow-xl shadow-black/50 ${feature.borderColor} animate-fade-in-up`}
            style={{ animationDelay: `${0.4 + (i * 0.1)}s` }}
          >
            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center text-2xl mb-6 border border-white/5 group-hover:scale-110 transition-transform duration-300`}>
              {feature.icon}
            </div>
            <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
            <p className="text-surface-400 leading-relaxed">{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
