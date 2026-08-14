'use client';

import React, { useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import VideoCanvas from '@/components/studio/VideoCanvas';
import ControlBar from '@/components/studio/ControlBar';
import ParticipantTile from '@/components/studio/ParticipantTile';
import LiveChat from '@/components/studio/LiveChat';
import useStudioStore from '@/store/useStudioStore';
import useMediaDevices from '@/hooks/useMediaDevices';

export default function StudioPage() {
  const params = useParams();
  const router = useRouter();
  const { sessionId } = params;
  
  const { setSessionId, localStream, screenStream, isMicMuted, isCamOff, isScreenSharing } = useStudioStore();
  const { requestPermissions, startPreview, stopPreview } = useMediaDevices();

  useEffect(() => {
    if (!sessionId) {
      router.push('/');
      return;
    }

    setSessionId(sessionId);
    
    const init = async () => {
      await requestPermissions();
      await startPreview();
    };
    init();

    return () => {
      stopPreview();
    };
  }, [sessionId, router, setSessionId, requestPermissions, startPreview, stopPreview]);

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col font-sans">
      {/* Header */}
      <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg flex items-center justify-center font-bold">
            S
          </div>
          <h1 className="text-xl font-bold tracking-tight">Studio</h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-slate-400 text-sm">Session: {sessionId}</span>
        </div>
      </header>

      {/* Main Studio Area */}
      <main className="flex-1 flex overflow-hidden p-4 gap-4">
        {/* Left/Center Stage */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Canvas Area */}
          <div className="flex-1 flex flex-col justify-center max-h-[calc(100vh-200px)]">
            <VideoCanvas />
          </div>

          {/* Participant Strip */}
          <div className="mt-4 flex gap-4 overflow-x-auto pb-2 custom-scrollbar">
            {localStream && (
              <ParticipantTile 
                id="local-cam" 
                name="Your Camera" 
                type="camera"
                stream={localStream}
                isVisible={!isCamOff}
                isAudioEnabled={!isMicMuted}
              />
            )}
            {screenStream && (
              <ParticipantTile 
                id="local-screen" 
                name="Your Screen Share" 
                type="screen"
                stream={screenStream}
                isVisible={isScreenSharing}
                isAudioEnabled={false}
              />
            )}
          </div>

          {/* Controls */}
          <ControlBar />
        </div>

        {/* Right Sidebar - Chat */}
        <div className="w-[380px] flex-shrink-0 hidden lg:block">
          <LiveChat liveChatId={sessionId} />
        </div>
      </main>
    </div>
  );
}
