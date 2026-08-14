'use client';

import React, { useRef, useEffect, useState } from 'react';
import useStudioStore from '@/store/useStudioStore';
import useCanvasCompositor from '@/hooks/useCanvasCompositor';

export default function VideoCanvas() {
  const canvasRef = useRef(null);
  const { isLive } = useStudioStore();
  const [uptime, setUptime] = useState('00:00:00');
  
  useCanvasCompositor(canvasRef);

  useEffect(() => {
    if (!isLive) {
      setUptime('00:00:00');
      return;
    }

    const startTime = Date.now();
    const interval = setInterval(() => {
      const diff = Date.now() - startTime;
      const hours = Math.floor(diff / 3600000).toString().padStart(2, '0');
      const minutes = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
      const seconds = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
      setUptime(`${hours}:${minutes}:${seconds}`);
    }, 1000);

    return () => clearInterval(interval);
  }, [isLive]);

  return (
    <div className="relative w-full aspect-video bg-gray-900 rounded-lg shadow-[0_0_20px_rgba(168,85,247,0.4)] overflow-hidden flex items-center justify-center border border-slate-700">
      <canvas
        ref={canvasRef}
        width={1280}
        height={720}
        className="w-full h-full object-contain"
      />
      
      {!isLive && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm z-10 pointer-events-none">
          <h2 className="text-3xl font-bold text-white mb-2">OFFLINE</h2>
          <p className="text-gray-400">Waiting to go live...</p>
        </div>
      )}

      {isLive && (
        <div className="absolute top-4 left-4 flex items-center gap-2 bg-black/50 px-3 py-1.5 rounded-full border border-red-500/30 z-20 pointer-events-none">
          <div className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse" />
          <span className="text-red-500 font-bold text-sm tracking-wider">LIVE</span>
          <span className="text-white/90 text-sm ml-2 font-mono">
            {uptime}
          </span>
        </div>
      )}
    </div>
  );
}
