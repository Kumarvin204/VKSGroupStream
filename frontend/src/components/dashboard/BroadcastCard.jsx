'use client';

import { useRouter } from 'next/navigation';

export default function BroadcastCard({ broadcast }) {
  const router = useRouter();

  // Determine status color and label based on lifeCycleStatus
  const getStatusInfo = (status) => {
    switch (status) {
      case 'live':
      case 'testing':
        return { color: 'bg-red-500 text-white', label: 'LIVE', glow: 'shadow-[0_0_10px_rgba(239,68,68,0.5)]' };
      case 'ready':
        return { color: 'bg-yellow-500 text-surface-950', label: 'READY', glow: '' };
      case 'complete':
        return { color: 'bg-surface-700 text-surface-300', label: 'ENDED', glow: '' };
      case 'created':
      default:
        return { color: 'bg-brand-500 text-white', label: 'UPCOMING', glow: '' };
    }
  };

  const statusInfo = getStatusInfo(broadcast.snippet?.actualEndTime ? 'complete' : broadcast.status?.lifeCycleStatus);
  
  const privacy = broadcast.status?.privacyStatus || 'public';
  const privacyIcons = {
    public: <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>,
    unlisted: <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>,
    private: <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
  };

  const publishAt = new Date(broadcast.snippet?.scheduledStartTime || broadcast.snippet?.publishedAt);
  const formattedDate = publishAt.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });

  return (
    <div 
      onClick={() => router.push(`/studio/${broadcast.id}`)}
      className="group bg-surface-900 border border-surface-800 hover:border-brand-500/50 rounded-2xl overflow-hidden cursor-pointer transition-all duration-300 hover:shadow-lg hover:shadow-brand-500/10 flex flex-col h-full"
    >
      <div className="relative aspect-video bg-surface-800 overflow-hidden">
        {broadcast.snippet?.thumbnails?.high?.url ? (
          <img 
            src={broadcast.snippet.thumbnails.high.url} 
            alt={broadcast.snippet.title} 
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-surface-600">
            <svg className="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        
        {/* Status Badge */}
        <div className={`absolute top-3 left-3 px-2.5 py-1 rounded-md text-[10px] font-bold tracking-wider ${statusInfo.color} ${statusInfo.glow}`}>
          {statusInfo.label}
        </div>
      </div>
      
      <div className="p-4 flex-1 flex flex-col">
        <h3 className="text-white font-medium line-clamp-2 mb-2 group-hover:text-brand-300 transition-colors">
          {broadcast.snippet?.title || 'Untitled Broadcast'}
        </h3>
        
        <div className="mt-auto pt-3 border-t border-surface-800/50 flex items-center justify-between text-xs text-surface-400">
          <div className="flex items-center gap-1.5 capitalize">
            {privacyIcons[privacy]}
            {privacy}
          </div>
          <div>{formattedDate}</div>
        </div>
      </div>
    </div>
  );
}
