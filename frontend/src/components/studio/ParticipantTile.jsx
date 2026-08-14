'use client';

import React, { useRef, useEffect } from 'react';
import { Eye, EyeOff, Mic, MicOff } from 'lucide-react';

export default function ParticipantTile({ 
  id, 
  name, 
  type = 'camera', 
  stream,
  isVisible = true, 
  isAudioEnabled = true,
  onToggleVisibility 
}) {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream;
      videoRef.current.play().catch(err => console.error('Error playing preview:', err));
    }
  }, [stream]);

  return (
    <div className={`relative bg-slate-900 border border-slate-700 rounded-lg overflow-hidden group aspect-video min-w-[240px] max-w-[320px] transition-opacity ${!isVisible ? 'opacity-50 grayscale' : ''}`}>
      {stream ? (
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full object-cover"
        />
      ) : (
        <div className="w-full h-full bg-slate-800 flex items-center justify-center">
          <span className="text-slate-500">{type === 'screen' ? 'Screen Share' : 'Camera Feed'}</span>
        </div>
      )}

      <div className="absolute bottom-0 inset-x-0 p-2 bg-gradient-to-t from-black/80 to-transparent flex items-center justify-between">
        <div className="flex items-center gap-2">
          {type === 'camera' && (
            <div className={`p-1 rounded-full ${isAudioEnabled ? 'bg-green-500/20 text-green-500' : 'bg-red-500/20 text-red-500'}`}>
              {isAudioEnabled ? <Mic size={12} /> : <MicOff size={12} />}
            </div>
          )}
          <span className="text-white text-sm font-medium truncate">{name}</span>
        </div>
      </div>

      {/* Hover Controls */}
      <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
        <button 
          onClick={() => onToggleVisibility?.(id)}
          className="p-1.5 bg-black/60 hover:bg-black/80 text-white rounded-md backdrop-blur-sm"
          title={isVisible ? "Hide from stream" : "Show on stream"}
        >
          {isVisible ? <Eye size={16} /> : <EyeOff size={16} />}
        </button>
      </div>
    </div>
  );
}
