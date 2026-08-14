const express = require('express');
const router = express.Router();
const streamService = require('../services/stream.service');
const ffmpegService = require('../services/ffmpeg.service');
const logger = require('../utils/logger');
const schedulerService = require('../services/scheduler.service');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Ensure uploads directory exists
const uploadDir = path.join(__dirname, '../../uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + '-' + file.originalname);
  }
});
const upload = multer({ storage: storage });
// POST /api/stream/start
router.post('/api/stream/start', (req, res) => {
  try {
    const { streamKey } = req.body;
    
    if (!streamKey || typeof streamKey !== 'string' || streamKey.trim() === '') {
      return res.status(400).json({ success: false, message: 'Valid streamKey is required' });
    }

    const session = streamService.createSession(streamKey);
    ffmpegService.startStream(session.id, streamKey);
    
    streamService.updateSession(session.id, { status: 'live' });

    res.json({
      success: true,
      sessionId: session.id,
      message: 'Stream started'
    });
  } catch (error) {
    logger.error(`Error starting stream: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// POST /api/stream/stop
router.post('/api/stream/stop', (req, res) => {
  try {
    const { sessionId } = req.body;
    
    if (!sessionId) {
      return res.status(400).json({ success: false, message: 'sessionId is required' });
    }

    ffmpegService.stopStream(sessionId);
    streamService.updateSession(sessionId, { status: 'stopped', stoppedAt: new Date() });

    res.json({ success: true, message: 'Stream stopped' });
  } catch (error) {
    logger.error(`Error stopping stream: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// GET /api/stream/status/:sessionId
router.get('/api/stream/status/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    let session = streamService.getSession(sessionId);
    let type = 'camera';
    
    if (!session) {
      const slot = schedulerService.getSlot(sessionId);
      if (!slot) {
        return res.status(404).json({ success: false, message: 'Session or Slot not found' });
      }
      session = slot;
      type = 'scheduled';
    }

    const isRunning = ffmpegService.isStreaming(sessionId);

    res.json({
      success: true,
      session,
      type,
      isRunning
    });
  } catch (error) {
    logger.error(`Error getting stream status: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// GET /api/stream/active
router.get('/api/stream/active', (req, res) => {
  try {
    const activeSessions = streamService.getActiveSessions();
    res.json({ success: true, activeSessions });
  } catch (error) {
    logger.error(`Error getting active streams: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});
// POST /api/stream/upload
router.post('/api/stream/upload', upload.single('video'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, message: 'No file uploaded' });
    }
    res.json({
      success: true,
      filePath: req.file.path,
      fileName: req.file.filename
    });
  } catch (error) {
    logger.error(`Error uploading file: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// POST /api/stream/schedule
router.post('/api/stream/schedule', (req, res) => {
  try {
    const { title, startTime, endTime, streamKey, filePath, loop } = req.body;
    
    if (!title || !startTime || !endTime || !streamKey || !filePath) {
      return res.status(400).json({ success: false, message: 'Missing required fields' });
    }

    const slot = schedulerService.scheduleSlot({
      title,
      startTime,
      endTime,
      streamKey,
      filePath,
      loop
    });

    res.json({ success: true, slot });
  } catch (error) {
    logger.error(`Error scheduling stream: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// GET /api/stream/slots
router.get('/api/stream/slots', (req, res) => {
  try {
    const slots = schedulerService.getSlots();
    res.json({ success: true, slots });
  } catch (error) {
    logger.error(`Error getting slots: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

// POST /api/stream/slots/cancel
router.post('/api/stream/slots/cancel', (req, res) => {
  try {
    const { slotId } = req.body;
    if (!slotId) {
      return res.status(400).json({ success: false, message: 'slotId is required' });
    }
    
    const success = schedulerService.cancelSlot(slotId);
    if (success) {
      res.json({ success: true, message: 'Slot cancelled' });
    } else {
      res.status(404).json({ success: false, message: 'Slot not found' });
    }
  } catch (error) {
    logger.error(`Error cancelling slot: ${error.message}`);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

module.exports = router;
