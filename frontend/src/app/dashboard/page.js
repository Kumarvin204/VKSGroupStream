'use client';

import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import CreateBroadcast from '@/components/dashboard/CreateBroadcast';
import BroadcastCard from '@/components/dashboard/BroadcastCard';
import ScheduleStream from '@/components/dashboard/ScheduleStream';
import StreamMonitor from '@/components/dashboard/StreamMonitor';
import { getChannelInfo, listBroadcasts } from '@/lib/youtube';

export default function DashboardPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  
  const [activeTab, setActiveTab] = useState('live'); // 'live' or 'scheduled'
  const [isGuest, setIsGuest] = useState(false);
  const [channel, setChannel] = useState(null);
  const [broadcasts, setBroadcasts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const guest = typeof window !== 'undefined' && localStorage.getItem('guestMode') === 'true';
    setIsGuest(guest);
    
    if (status === 'unauthenticated' && !guest) {
      router.push('/');
    }
  }, [status, router]);

  useEffect(() => {
    async function fetchData() {
      if (session?.accessToken) {
        try {
          setIsLoading(true);
          const [channelData, broadcastsData] = await Promise.all([
            getChannelInfo(session.accessToken),
            listBroadcasts(session.accessToken).catch(() => null)
          ]);
          setChannel(channelData);
          setBroadcasts(broadcastsData?.items || broadcastsData || []);
        } catch (err) {
          console.error("Failed to fetch dashboard data", err);
          setError("Failed to load channel data. Please make sure Google Cloud Client ID is configured and refresh.");
        } finally {
          setIsLoading(false);
        }
      }
    }

    if (session?.accessToken) {
      fetchData();
    } else if (typeof window !== 'undefined' && localStorage.getItem('guestMode') === 'true') {
      setIsLoading(false);
    }
  }, [session]);

  if (status === 'loading' || (status === 'authenticated' && isLoading)) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-10 h-10 border-4 border-surface-700 border-t-brand-500 rounded-full animate-spin"></div>
          <p className="text-surface-400 text-sm animate-pulse">Loading studio data...</p>
        </div>
      </div>
    );
  }

  const isUserAuthenticated = session || isGuest;
  if (!isUserAuthenticated) return null;

  return (
    <div className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      
      {/* Welcome & Channel Info */}
      <div className="bg-surface-900/50 backdrop-blur-md border border-surface-800 rounded-3xl p-6 md:p-8 flex flex-col md:flex-row items-center md:items-start gap-6 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-brand-600/10 rounded-full blur-3xl -z-10 translate-x-1/2 -translate-y-1/2"></div>
        
        {channel?.items?.[0]?.snippet?.thumbnails?.default?.url ? (
          <img 
            src={channel.items[0].snippet.thumbnails.default.url} 
            alt={session?.user?.name} 
            className="w-20 h-20 rounded-2xl object-cover shadow-lg border border-surface-700" 
          />
        ) : (
          <div className="w-20 h-20 rounded-2xl bg-surface-800 flex items-center justify-center text-3xl shadow-lg border border-surface-700">📺</div>
        )}
        
        <div className="text-center md:text-left flex-1">
          <h1 className="text-3xl font-bold text-white mb-2">Welcome back, {isGuest ? 'Streamer' : session?.user?.name?.split(' ')[0]}!</h1>
          {isGuest ? (
            <div className="space-y-1">
              <p className="text-surface-300 font-medium text-lg">Direct Stream Key Ingestion Mode</p>
              <p className="text-sm text-surface-400">Stream directly to YouTube without Google Developer Client setup. Enter your YouTube Live Stream Key in the form below.</p>
            </div>
          ) : channel?.items?.[0] ? (
            <div className="space-y-1">
              <p className="text-surface-300 font-medium text-lg">{channel.items[0].snippet.title}</p>
              <div className="flex items-center justify-center md:justify-start gap-4 text-sm text-surface-400">
                <span className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                  {Number(channel.items[0].statistics.subscriberCount).toLocaleString()} Subscribers
                </span>
                <span className="flex items-center gap-1">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                  {Number(channel.items[0].statistics.videoCount).toLocaleString()} Videos
                </span>
              </div>
            </div>
          ) : (
            <p className="text-surface-400">Connecting to YouTube channel...</p>
          )}
          {error && <p className="text-red-400 text-sm mt-2">{error}</p>}
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="flex border-b border-surface-850 gap-2">
        <button
          onClick={() => setActiveTab('live')}
          className={`py-3 px-6 text-sm font-semibold border-b-2 transition-all duration-200 ${
            activeTab === 'live'
              ? 'border-brand-500 text-white font-bold'
              : 'border-transparent text-surface-400 hover:text-white'
          }`}
        >
          📹 Live Studio (StreamYard Style)
        </button>
        <button
          onClick={() => setActiveTab('scheduled')}
          className={`py-3 px-6 text-sm font-semibold border-b-2 transition-all duration-200 ${
            activeTab === 'scheduled'
              ? 'border-brand-500 text-white font-bold'
              : 'border-transparent text-surface-400 hover:text-white'
          }`}
        >
          ⏰ 24/7 Automated Streams (StreamAdda Style)
        </button>
      </div>

      {/* Tabs Content */}
      {activeTab === 'live' ? (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          
          {/* Create Broadcast form */}
          <div className="xl:col-span-1">
            <CreateBroadcast accessToken={session?.accessToken} />
          </div>

          {/* Broadcast list */}
          <div className="xl:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                <svg className="w-6 h-6 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                {isGuest ? 'Manual Streams Studio' : 'Recent YouTube Broadcasts'}
              </h2>
            </div>
            
            {isGuest ? (
              <div className="bg-surface-900/30 border border-surface-800 border-dashed rounded-2xl p-12 text-center">
                <div className="w-16 h-16 bg-surface-800 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-brand-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                </div>
                <h3 className="text-lg font-medium text-white mb-2">Direct Key Stream Studio</h3>
                <p className="text-surface-400 max-w-md mx-auto">Fill in a title, paste your stream key on the left, and click "Enter Studio" to start your WebRTC mic/webcam and screen capture stage.</p>
              </div>
            ) : broadcasts.length === 0 ? (
              <div className="bg-surface-900/30 border border-surface-800 border-dashed rounded-2xl p-12 text-center">
                <div className="w-16 h-16 bg-surface-800 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-surface-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                </div>
                <h3 className="text-lg font-medium text-white mb-2">No broadcasts yet</h3>
                <p className="text-surface-400">Create a new live broadcast using the form on the left.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {broadcasts.map(broadcast => (
                  <BroadcastCard key={broadcast.id} broadcast={broadcast} />
                ))}
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Schedule Form */}
          <div className="xl:col-span-1">
            <ScheduleStream />
          </div>

          {/* Monitoring Screen */}
          <div className="xl:col-span-2">
            <StreamMonitor />
          </div>
        </div>
      )}
    </div>
  );
}
