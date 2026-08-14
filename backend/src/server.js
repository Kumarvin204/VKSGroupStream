require('dotenv').config();
const express = require('express');
const http = require('http');
const { WebSocketServer } = require('ws');
const url = require('url');

const config = require('./utils/config');
const logger = require('./utils/logger');
const getCorsMiddleware = require('./middleware/cors');
const streamRoutes = require('./routes/stream');
const youtubeRoutes = require('./routes/youtube');
const streamService = require('./services/stream.service');
const ffmpegService = require('./services/ffmpeg.service');

const app = express();
const server = http.createServer(app);

// Express Setup
app.use(getCorsMiddleware());
app.use(express.json());

// Routes
app.use('/', streamRoutes);
app.use('/', youtubeRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    activeStreams: streamService.getActiveSessions().length,
    uptime: process.uptime()
  });
});

// WebSocket Setup
const wss = new WebSocketServer({ noServer: true });

server.on('upgrade', (request, socket, head) => {
  const { pathname, query } = url.parse(request.url, true);

  if (pathname === '/ws/stream') {
    wss.handleUpgrade(request, socket, head, (ws) => {
      wss.emit('connection', ws, request, query);
    });
  } else {
    socket.destroy();
  }
});

wss.on('connection', (ws, request, query) => {
  const streamKey = query.streamKey;

  if (!streamKey) {
    logger.warn('WebSocket connection attempted without streamKey');
    ws.close(4001, 'streamKey is required');
    return;
  }

  const session = streamService.createSession(streamKey);
  streamService.updateSession(session.id, { status: 'live' });
  
  ffmpegService.startStream(session.id, streamKey);
  
  // ws.binaryType = 'arraybuffer'; // Optional on server, but often 'nodebuffer' is used

  logger.info(`WebSocket connected for session: ${session.id}`);
  
  ws.send(JSON.stringify({ type: 'connected', sessionId: session.id }));

  ws.on('message', (message) => {
    // Assuming binary data for stream
    const isSuccess = ffmpegService.writeData(session.id, message);
    if (!isSuccess) {
      logger.debug(`Failed to write data for session ${session.id}, possibly backpressured or closed`);
    }
  });

  ws.on('close', () => {
    logger.info(`WebSocket closed for session: ${session.id}`);
    ffmpegService.stopStream(session.id);
    streamService.updateSession(session.id, { status: 'stopped', stoppedAt: new Date() });
  });

  ws.on('error', (err) => {
    logger.error(`WebSocket error for session ${session.id}: ${err.message}`);
    ffmpegService.stopStream(session.id);
    streamService.updateSession(session.id, { status: 'error', stoppedAt: new Date(), metadata: { error: err.message } });
  });
});

// Graceful Shutdown
const shutdown = () => {
  logger.info('Shutting down server...');
  ffmpegService.stopAll();
  
  wss.close(() => {
    logger.info('WebSocket server closed');
    server.close(() => {
      logger.info('HTTP server closed');
      process.exit(0);
    });
  });
  
  // Force exit if taking too long
  setTimeout(() => process.exit(1), 10000).unref();
};

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);

// Start
server.listen(config.PORT, () => {
  logger.info(`Server running on port ${config.PORT}`);
  logger.info(`WebSocket endpoint: ws://localhost:${config.PORT}/ws/stream`);
  logger.info(`Health check: http://localhost:${config.PORT}/api/health`);
});
