require('dotenv').config();
const path = require('path');

let ffmpegPath = process.env.FFMPEG_PATH || 'ffmpeg';

// If no custom FFMPEG_PATH is specified, attempt to resolve using the local portable ffmpeg installer package (essential for cloud platforms like Render)
if (!process.env.FFMPEG_PATH) {
  try {
    const ffmpegInstaller = require('@ffmpeg-installer/ffmpeg');
    if (ffmpegInstaller.path) {
      ffmpegPath = ffmpegInstaller.path;
    }
  } catch (err) {
    // Fallback to system globally-installed 'ffmpeg'
  }
}

module.exports = {
  PORT: process.env.PORT || 4000,
  CORS_ORIGIN: process.env.CORS_ORIGIN || 'http://localhost:3000',
  YOUTUBE_RTMP_BASE_URL: process.env.YOUTUBE_RTMP_BASE_URL || 'rtmp://a.rtmp.youtube.com/live2',
  FFMPEG_PATH: ffmpegPath,
  NODE_ENV: process.env.NODE_ENV || 'development',
  UPLOAD_DIR: path.join(process.cwd(), 'uploads'),
};
