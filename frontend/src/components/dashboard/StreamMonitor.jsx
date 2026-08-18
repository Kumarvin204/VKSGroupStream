'use client';

import React, { useState, useEffect } from 'react';
import Button from '@/components/ui/Button';
import { BACKEND_URL } from '@/lib/constants';

export default function StreamMonitor() {
  const [slots, setSlots] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchSlots = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/api/stream/slots`);
      if (!res.ok) throw new Error('Failed to fetch scheduled streams');
      const data = await res.json();
      setSlots(data.slots || []);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Could not load slots.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSlots();
    
    // Poll slots every 5 seconds to catch live transitions
    const interval = setInterval(fetchSlots, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleCancel = async (slotId) => {
    if (!confirm('Are you sure you want to cancel this scheduled stream?')) return;

    try {
      const res = await fetch(`${BACKEND_URL}/api/stream/slots/cancel`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slotId })
      });
      
      const data = await res.json();
      if (data.success) {
        fetchSlots();
      } else {
        throw new Error(data.message || 'Failed to cancel slot');
      }
    } catch (err) {
      console.error(err);
      alert(err.message || 'Error cancelling stream');
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'live':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-red-500/10 text-red-400 border border-red-500/20">
            <span className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse" />
            LIVE
          </span>
        );
      case 'scheduled':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
            SCHEDULED
          </span>
        );
      case 'completed':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-surface-800 text-surface-400 border border-surface-700">
            COMPLETED
          </span>
        );
      case 'cancelled':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-red-950/20 text-red-600 border border-red-950/30 line-through">
            CANCELLED
          </span>
        );
      default:
        return null;
    }
  };

  const formatDate = (dateString) => {
    const d = new Date(dateString);
    return d.toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="w-8 h-8 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <span className="text-xl">📊</span> Stream Schedule Monitor
        </h2>
        <Button variant="secondary" size="sm" onClick={fetchSlots}>
          Refresh
        </Button>
      </div>

      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl mb-6 text-sm">
          {error}
        </div>
      )}

      {slots.length === 0 ? (
        <div className="text-center py-12 text-surface-400 border border-dashed border-surface-700 rounded-2xl">
          <span className="text-3xl block mb-2">📅</span>
          No streams scheduled yet. Fill out the form to add one.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-surface-800 text-surface-400 text-sm">
                <th className="py-4 px-4 font-semibold">Title</th>
                <th className="py-4 px-4 font-semibold">Status</th>
                <th className="py-4 px-4 font-semibold">Scheduled Range</th>
                <th className="py-4 px-4 font-semibold">Settings</th>
                <th className="py-4 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {slots.map((slot) => (
                <tr key={slot.id} className="border-b border-surface-800/50 hover:bg-surface-800/10 transition-colors">
                  <td className="py-4 px-4 font-medium text-white max-w-[200px] truncate" title={slot.title}>
                    {slot.title}
                  </td>
                  <td className="py-4 px-4">
                    {getStatusBadge(slot.status)}
                  </td>
                  <td className="py-4 px-4 text-sm text-surface-300">
                    <div className="flex flex-col">
                      <span>Start: {formatDate(slot.startTime)}</span>
                      <span className="text-xs text-surface-500">End: {formatDate(slot.endTime)}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-sm">
                    <div className="flex flex-col text-surface-400 text-xs">
                      <span>File: {slot.filePath.split(/[/\\]/).pop()}</span>
                      <span>Looping: {slot.loop ? 'On 🔄' : 'Off'}</span>
                    </div>
                  </td>
                  <td className="py-4 px-4 text-right">
                    {(slot.status === 'scheduled' || slot.status === 'live') && (
                      <Button
                        variant="danger"
                        size="sm"
                        className="py-1 px-3 text-xs rounded-lg"
                        onClick={() => handleCancel(slot.id)}
                      >
                        Cancel
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
