const express = require('express');
const router = express.Router();
const youtubeService = require('../services/youtube.service');
const logger = require('../utils/logger');

/**
 * All routes require a valid access token in the Authorization header.
 * The frontend sends the user's real Google OAuth access token.
 */
function getAccessToken(req) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null;
  }
  return authHeader.split(' ')[1];
}

// POST /api/youtube/broadcast — Create a real YouTube broadcast
router.post('/api/youtube/broadcast', async (req, res) => {
  try {
    const accessToken = getAccessToken(req);
    if (!accessToken) {
      return res.status(401).json({ success: false, message: 'Access token required' });
    }

    const { title, description, privacyStatus } = req.body;
    if (!title || title.trim() === '') {
      return res.status(400).json({ success: false, message: 'Title is required' });
    }

    // Step 1: Create the broadcast
    const broadcast = await youtubeService.createBroadcast(accessToken, {
      title,
      description,
      privacyStatus,
    });

    // Step 2: Create the stream (gets RTMP URL + stream key)
    const stream = await youtubeService.createStream(accessToken, { title });

    // Step 3: Bind broadcast to stream
    await youtubeService.bindBroadcastToStream(accessToken, broadcast.id, stream.id);

    const streamKey = stream.cdn?.ingestionInfo?.streamName;
    const rtmpUrl = stream.cdn?.ingestionInfo?.ingestionAddress;

    logger.info(`Broadcast setup complete: ${broadcast.id}, Stream Key: ${streamKey}`);

    res.json({
      success: true,
      broadcast,
      stream,
      streamKey,
      rtmpUrl,
      liveChatId: broadcast.snippet?.liveChatId || null,
    });
  } catch (error) {
    logger.error(`YouTube broadcast creation failed: ${error.message}`);
    res.status(500).json({ success: false, message: error.message });
  }
});

// POST /api/youtube/broadcast/transition — Transition broadcast status
router.post('/api/youtube/broadcast/transition', async (req, res) => {
  try {
    const accessToken = getAccessToken(req);
    if (!accessToken) {
      return res.status(401).json({ success: false, message: 'Access token required' });
    }

    const { broadcastId, status } = req.body;
    if (!broadcastId || !status) {
      return res.status(400).json({ success: false, message: 'broadcastId and status required' });
    }

    const result = await youtubeService.transitionBroadcast(accessToken, broadcastId, status);
    res.json({ success: true, broadcast: result });
  } catch (error) {
    logger.error(`Broadcast transition failed: ${error.message}`);
    res.status(500).json({ success: false, message: error.message });
  }
});

// GET /api/youtube/broadcasts — List user's broadcasts
router.get('/api/youtube/broadcasts', async (req, res) => {
  try {
    const accessToken = getAccessToken(req);
    if (!accessToken) {
      return res.status(401).json({ success: false, message: 'Access token required' });
    }

    const { status = 'all' } = req.query;
    const result = await youtubeService.listBroadcasts(accessToken, status);
    res.json({ success: true, ...result });
  } catch (error) {
    logger.error(`List broadcasts failed: ${error.message}`);
    res.status(500).json({ success: false, message: error.message });
  }
});

// GET /api/youtube/channel — Get user's channel info
router.get('/api/youtube/channel', async (req, res) => {
  try {
    const accessToken = getAccessToken(req);
    if (!accessToken) {
      return res.status(401).json({ success: false, message: 'Access token required' });
    }

    const result = await youtubeService.getChannelInfo(accessToken);
    res.json({ success: true, ...result });
  } catch (error) {
    logger.error(`Get channel info failed: ${error.message}`);
    res.status(500).json({ success: false, message: error.message });
  }
});

// GET /api/youtube/chat/:liveChatId — Get live chat messages
router.get('/api/youtube/chat/:liveChatId', async (req, res) => {
  try {
    const accessToken = getAccessToken(req);
    if (!accessToken) {
      return res.status(401).json({ success: false, message: 'Access token required' });
    }

    const { liveChatId } = req.params;
    const { pageToken } = req.query;
    const result = await youtubeService.getLiveChatMessages(accessToken, liveChatId, pageToken);
    res.json({ success: true, ...result });
  } catch (error) {
    logger.error(`Get chat messages failed: ${error.message}`);
    res.status(500).json({ success: false, message: error.message });
  }
});

module.exports = router;
