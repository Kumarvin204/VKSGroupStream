'use client';

import React, { useState } from 'react';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';

export default function ScheduleStream() {
  const [title, setTitle] = useState('');
  const [streamKey, setStreamKey] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [loop, setLoop] = useState(false);
  
  const [videoFile, setVideoFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [videoPath, setVideoPath] = useState('');
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState({ type: '', message: '' });

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setVideoFile(e.target.files[0]);
      setStatus({ type: '', message: '' });
      setVideoPath('');
      setUploadProgress(0);
    }
  };

  const handleUpload = async () => {
    if (!videoFile) {
      setStatus({ type: 'error', message: 'Please select a video file first.' });
      return;
    }

    setIsUploading(true);
    setStatus({ type: '', message: '' });
    
    const formData = new FormData();
    formData.append('video', videoFile);

    try {
      // Custom XHR to track progress
      const xhr = new XMLHttpRequest();
      
      const uploadPromise = new Promise((resolve, reject) => {
        xhr.upload.onprogress = (event) => {
          if (event.lengthComputable) {
            const percent = Math.round((event.loaded / event.total) * 100);
            setUploadProgress(percent);
          }
        };

        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            resolve(JSON.parse(xhr.response));
          } else {
            reject(new Error(xhr.statusText || 'Upload failed'));
          }
        };

        xhr.onerror = () => reject(new Error('Network error during upload'));
        
        xhr.open('POST', '/api/stream/upload');
        xhr.send(formData);
      });

      const res = await uploadPromise;
      if (res.success) {
        setVideoPath(res.filePath);
        setStatus({ type: 'success', message: `Video uploaded successfully: ${res.fileName}` });
      } else {
        throw new Error(res.message || 'Upload failed');
      }
    } catch (err) {
      console.error(err);
      setStatus({ type: 'error', message: err.message || 'Failed to upload video.' });
      setUploadProgress(0);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !streamKey.trim() || !startTime || !endTime || !videoPath) {
      setStatus({ type: 'error', message: 'All fields are required. Please upload the video first.' });
      return;
    }

    setIsSubmitting(true);
    setStatus({ type: '', message: '' });

    try {
      const res = await fetch('/api/stream/schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title,
          streamKey,
          startTime,
          endTime,
          filePath: videoPath,
          loop,
        }),
      });

      const data = await res.json();
      if (data.success) {
        setStatus({ type: 'success', message: 'Stream slot scheduled successfully!' });
        setTitle('');
        setStreamKey('');
        setStartTime('');
        setEndTime('');
        setLoop(false);
        setVideoFile(null);
        setVideoPath('');
        setUploadProgress(0);
      } else {
        throw new Error(data.message || 'Failed to schedule stream.');
      }
    } catch (err) {
      console.error(err);
      setStatus({ type: 'error', message: err.message || 'Failed to schedule stream.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <span className="text-xl">⏰</span> Schedule Automated Stream
      </h2>

      {status.message && (
        <div className={`p-4 rounded-xl mb-6 border text-sm ${
          status.type === 'success' 
            ? 'bg-green-500/10 border-green-500/20 text-green-400' 
            : 'bg-red-500/10 border-red-500/20 text-red-400'
        }`}>
          {status.message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <Input
          label="Stream Title"
          placeholder="e.g. 24/7 Looped Music Broadcast"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />

        <Input
          label="YouTube Stream Key"
          placeholder="Paste your rtmp stream key here"
          type="password"
          value={streamKey}
          onChange={(e) => setStreamKey(e.target.value)}
          required
        />

        <div className="border border-surface-700 rounded-xl p-4 bg-surface-950/40 space-y-4">
          <label className="text-sm font-medium text-surface-300 block mb-1">
            Video Source File
          </label>
          <div className="flex gap-4 items-center">
            <input
              type="file"
              accept="video/*"
              onChange={handleFileChange}
              className="file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-brand-600/20 file:text-brand-300 hover:file:bg-brand-600/30 text-sm text-surface-400 flex-1"
            />
            {videoFile && !videoPath && (
              <Button
                type="button"
                variant="secondary"
                size="sm"
                onClick={handleUpload}
                isLoading={isUploading}
              >
                Upload File
              </Button>
            )}
          </div>
          {isUploading && (
            <div className="w-full bg-surface-800 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-brand-500 h-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          )}
          {videoPath && (
            <div className="text-xs text-green-400 flex items-center gap-1.5">
              <span>✓ Ready to stream</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Start Date & Time"
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            required
          />
          <Input
            label="End Date & Time"
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            required
          />
        </div>

        <div className="flex items-center gap-3 p-3 bg-surface-800/40 rounded-xl border border-surface-700/50">
          <input
            id="loop-toggle"
            type="checkbox"
            checked={loop}
            onChange={(e) => setLoop(e.target.checked)}
            className="w-4 h-4 text-brand-600 border-surface-600 bg-surface-800 rounded focus:ring-brand-500 focus:ring-offset-surface-950"
          />
          <label htmlFor="loop-toggle" className="text-sm font-medium text-surface-300 cursor-pointer select-none">
            Loop video continuously until end time
          </label>
        </div>

        <Button
          type="submit"
          variant="primary"
          className="w-full"
          isLoading={isSubmitting}
        >
          Schedule Stream
        </Button>
      </form>
    </div>
  );
}
