require('dotenv').config();
const path = require('path');

module.exports = {
  PORT: process.env.PORT || 4000,
  CORS_ORIGIN: process.env.CORS_ORIGIN || 'http://localhost:3000',
  YOUTUBE_RTMP_BASE_URL: process.env.YOUTUBE_RTMP_BASE_URL || 'rtmp://a.rtmp.youtube.com/live2',
  FFMPEG_PATH: process.env.FFMPEG_PATH || 'ffmpeg',
  NODE_ENV: process.env.NODE_ENV || 'development',
  UPLOAD_DIR: path.join(process.cwd(), 'uploads'),
};
