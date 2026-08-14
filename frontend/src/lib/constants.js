export const APP_NAME = 'VKSGroupStream';
export const APP_DESCRIPTION = 'Broadcast to YouTube Live — Camera, Screen Share, Pre-recorded Videos';

export const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:4000';
export const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:4000';

export const STREAM_SETTINGS = {
  VIDEO_BITRATE: '4500k',
  AUDIO_BITRATE: '128k',
  FRAME_RATE: 30,
  RESOLUTION: { width: 1920, height: 1080 },
  CANVAS_RESOLUTION: { width: 1280, height: 720 },
  MEDIA_RECORDER_TIMESLICE: 250, // ms between data chunks
  MEDIA_RECORDER_MIME: 'video/webm;codecs=vp8,opus',
};

export const PRIVACY_OPTIONS = [
  { value: 'public', label: 'Public', description: 'Everyone can watch' },
  { value: 'unlisted', label: 'Unlisted', description: 'Anyone with the link' },
  { value: 'private', label: 'Private', description: 'Only you' },
];
