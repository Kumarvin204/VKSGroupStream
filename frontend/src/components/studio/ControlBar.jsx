'use client';

import React, { useState } from 'react';
import useStudioStore from '@/store/useStudioStore';
import useScreenShare from '@/hooks/useScreenShare';
import { useStreamSocket } from '@/hooks/useStreamSocket';
import useAuthStore from '@/store/useAuthStore';
import { Mic, MicOff, Video, VideoOff, MonitorUp, MonitorOff, Settings, LayoutGrid, MonitorPlay, LogOut } from 'lucide-react';

export default function ControlBar() {
  const { 
    isLive, setIsLive,
    isMicMuted, toggleMic,
    isCamOff, toggleCam,
    isScreenSharing,
    layout, setLayout
  } = useStudioStore();

  const { startScreenShare, stopScreenShare } = useScreenShare();
  const { startStreaming, stopStreaming } = useStreamSocket();
  const streamKey = useAuthStore(state => state.streamKey);
  const [isConnecting, setIsConnecting] = useState(false);

  const handleGoLive = async () => {
    if (isLive) {
      stopStreaming();
    } else {
      setIsConnecting(true);
      const key = streamKey || new URLSearchParams(window.location.search).get('key') || 'demo-session-id';
      if (!key) {
        console.warn("No stream key found!");
      }
      startStreaming(key);
      setIsConnecting(false);
    }
  };

  return (
    <div className="flex items-center justify-between p-4 bg-slate-900 border border-slate-800 rounded-xl mt-4 shadow-lg">
      <div className="flex items-center gap-3">
        <button 
          onClick={toggleMic}
          className={`p-3 rounded-full flex items-center justify-center transition-all ${!isMicMuted ? 'bg-slate-800 hover:bg-slate-700 text-white' : 'bg-red-500/10 hover:bg-red-500/20 text-red-500'}`}
          title={isMicMuted ? "Unmute Mic" : "Mute Mic"}
        >
          {!isMicMuted ? <Mic size={20} /> : <MicOff size={20} />}
        </button>

        <button 
          onClick={toggleCam}
          className={`p-3 rounded-full flex items-center justify-center transition-all ${!isCamOff ? 'bg-slate-800 hover:bg-slate-700 text-white' : 'bg-red-500/10 hover:bg-red-500/20 text-red-500'}`}
          title={isCamOff ? "Turn Cam On" : "Turn Cam Off"}
        >
          {!isCamOff ? <Video size={20} /> : <VideoOff size={20} />}
        </button>

        <div className="w-px h-8 bg-slate-700 mx-2" />

        <button 
          onClick={isScreenSharing ? stopScreenShare : startScreenShare}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-all font-medium ${isScreenSharing ? 'bg-purple-600 hover:bg-purple-700 text-white' : 'bg-slate-800 hover:bg-slate-700 text-slate-300'}`}
        >
          {isScreenSharing ? <MonitorOff size={18} /> : <MonitorUp size={18} />}
          {isScreenSharing ? 'Stop Share' : 'Share Screen'}
        </button>
      </div>

      <div className="flex items-center gap-3">
        <div className="flex bg-slate-800 p-1 rounded-lg">
          <button 
            onClick={() => setLayout('grid')}
            className={`p-2 rounded-md ${layout === 'grid' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            <LayoutGrid size={18} />
          </button>
          <button 
            onClick={() => setLayout('presentation')}
            className={`p-2 rounded-md ${layout === 'presentation' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            <MonitorPlay size={18} />
          </button>
        </div>

        <button className="p-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-full transition-colors">
          <Settings size={20} />
        </button>

        <div className="w-px h-8 bg-slate-700 mx-2" />

        <button 
          onClick={handleGoLive}
          disabled={isConnecting}
          className={`px-6 py-2.5 rounded-lg flex items-center gap-2 font-bold transition-all disabled:opacity-70 ${
            isLive 
              ? 'bg-red-500 hover:bg-red-600 text-white' 
              : 'bg-purple-600 hover:bg-purple-700 text-white shadow-[0_0_15px_rgba(147,51,234,0.3)] hover:shadow-[0_0_20px_rgba(147,51,234,0.5)]'
          }`}
        >
          {isConnecting ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : isLive ? (
            <LogOut size={18} />
          ) : (
            <MonitorPlay size={18} />
          )}
          {isConnecting ? 'Connecting...' : isLive ? 'End Stream' : 'Go Live'}
        </button>
      </div>
    </div>
  );
}
