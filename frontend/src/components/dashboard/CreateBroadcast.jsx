'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { createBroadcast, createStream, bindBroadcastToStream } from '@/lib/youtube';
import useAuthStore from '@/store/useAuthStore';

const PRIVACY_OPTIONS = [
  { value: 'public', label: 'Public - Anyone can search for and view' },
  { value: 'unlisted', label: 'Unlisted - Anyone with the link can view' },
  { value: 'private', label: 'Private - Only you can view' }
];

export default function CreateBroadcast({ accessToken }) {
  const router = useRouter();
  const setStreamData = useAuthStore(state => state.setStreamData);
  
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [privacyStatus, setPrivacyStatus] = useState('unlisted');
  const [useManualKey, setUseManualKey] = useState(false);
  const [manualStreamKey, setManualStreamKey] = useState('');
  
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!accessToken) {
      setUseManualKey(true);
    }
  }, [accessToken]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError('Stream title is required');
      return;
    }

    if (useManualKey && !manualStreamKey.trim()) {
      setError('Stream key is required when using manual mode');
      return;
    }

    setIsCreating(true);

    try {
      if (useManualKey) {
        // Just store the manual key and redirect
        setStreamData({
          broadcast: { title, description, privacyStatus, id: 'manual' },
          streamKey: manualStreamKey
        });
        router.push('/studio/manual');
      } else {
        // Real YouTube API flow
        if (!accessToken) throw new Error("Not authenticated");
        
        // 1. Create Broadcast
        const broadcast = await createBroadcast(accessToken, { 
          title, 
          description, 
          privacyStatus 
        });
        
        // 2. Create Stream
        const stream = await createStream(accessToken, { title });
        
        // 3. Bind them
        await bindBroadcastToStream(accessToken, broadcast.id, stream.id);
        
        // Extract key
        const streamKey = stream.cdn?.ingestionInfo?.streamName;
        if (!streamKey) throw new Error("Could not retrieve stream key from YouTube");
        
        // Store in global state
        setStreamData({ broadcast, streamKey });
        
        // Redirect to studio
        router.push(`/studio/${broadcast.id}`);
      }
    } catch (err) {
      console.error("Failed to create broadcast:", err);
      setError(err.message || 'Failed to create broadcast. Please try again.');
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="bg-surface-900 border border-surface-800 rounded-3xl p-6 shadow-xl h-full">
      <div className="mb-6">
        <h2 className="text-xl font-bold text-white mb-1">New Broadcast</h2>
        <p className="text-sm text-surface-400">Set up your next live stream</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        <Input
          label="Stream Title *"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="My Awesome Live Stream"
          maxLength={100}
        />

        <Input
          textarea
          rows={3}
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Tell viewers what this stream is about..."
          maxLength={5000}
        />

        <div>
          <label className="text-sm font-medium text-surface-300 mb-1.5 block">
            Privacy
          </label>
          <select
            value={privacyStatus}
            onChange={(e) => setPrivacyStatus(e.target.value)}
            className="w-full bg-surface-800 border border-surface-600 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 transition-all duration-200 appearance-none"
            style={{ backgroundImage: 'url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%239CA3AF%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E")', backgroundRepeat: 'no-repeat', backgroundPosition: 'right 1rem top 50%', backgroundSize: '0.65rem auto' }}
          >
            {PRIVACY_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </div>

        {accessToken && (
          <div className="pt-2 border-t border-surface-800">
            <label className="flex items-center cursor-pointer group">
              <div className="relative">
                <input 
                  type="checkbox" 
                  className="sr-only" 
                  checked={useManualKey}
                  onChange={(e) => setUseManualKey(e.target.checked)}
                />
                <div className={`block w-10 h-6 rounded-full transition-colors ${useManualKey ? 'bg-brand-500' : 'bg-surface-700 group-hover:bg-surface-600'}`}></div>
                <div className={`absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform ${useManualKey ? 'translate-x-4' : ''}`}></div>
              </div>
              <div className="ml-3">
                <span className="text-sm font-medium text-surface-200">Use Manual RTMP Key</span>
              </div>
            </label>
          </div>
        )}

        {useManualKey && (
          <div className="animate-fade-in-up">
            <Input
              label="Stream Key"
              type="password"
              value={manualStreamKey}
              onChange={(e) => setManualStreamKey(e.target.value)}
              placeholder="xxxx-xxxx-xxxx-xxxx"
              helperText="Paste your existing YouTube stream key"
            />
          </div>
        )}

        {error && (
          <div className="p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
            {error}
          </div>
        )}

        <Button 
          type="submit" 
          variant="primary" 
          className="w-full mt-4" 
          isLoading={isCreating}
          icon={<svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>}
        >
          {useManualKey ? 'Enter Studio' : 'Create Broadcast'}
        </Button>
      </form>
    </div>
  );
}
