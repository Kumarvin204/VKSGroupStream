const logger = require('../utils/logger');

const YOUTUBE_API_BASE = 'https://www.googleapis.com/youtube/v3';

class YouTubeService {
  /**
   * Create a YouTube live broadcast via the real YouTube Data API v3
   * @param {string} accessToken - User's OAuth access token
   * @param {object} params - Broadcast parameters
   * @returns {Promise<object>} - YouTube broadcast resource
   */
  async createBroadcast(accessToken, { title, description, privacyStatus = 'public' }) {
    logger.info(`Creating YouTube broadcast: "${title}"`);

    const response = await fetch(
      `${YOUTUBE_API_BASE}/liveBroadcasts?part=snippet,status,contentDetails`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          snippet: {
            title,
            description: description || '',
            scheduledStartTime: new Date().toISOString(),
          },
          status: {
            privacyStatus,
            selfDeclaredMadeForKids: false,
          },
          contentDetails: {
            enableAutoStart: true,
            enableAutoStop: true,
          },
        }),
      }
    );

    if (!response.ok) {
      const error = await response.json();
      logger.error(`YouTube createBroadcast failed: ${JSON.stringify(error)}`);
      throw new Error(error.error?.message || 'Failed to create broadcast');
    }

    const broadcast = await response.json();
    logger.info(`Broadcast created: ${broadcast.id}`);
    return broadcast;
  }

  /**
   * Create a YouTube live stream (returns RTMP URL + stream key)
   * @param {string} accessToken - User's OAuth access token
   * @param {object} params - Stream parameters
   * @returns {Promise<object>} - YouTube stream resource with cdn.ingestionInfo
   */
  async createStream(accessToken, { title = 'Stream' }) {
    logger.info(`Creating YouTube stream: "${title}"`);

    const response = await fetch(
      `${YOUTUBE_API_BASE}/liveStreams?part=snippet,cdn,status`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          snippet: { title },
          cdn: {
            frameRate: '30fps',
            ingestionType: 'rtmp',
            resolution: '1080p',
          },
        }),
      }
    );

    if (!response.ok) {
      const error = await response.json();
      logger.error(`YouTube createStream failed: ${JSON.stringify(error)}`);
      throw new Error(error.error?.message || 'Failed to create stream');
    }

    const stream = await response.json();
    logger.info(`Stream created: ${stream.id}, RTMP key: ${stream.cdn?.ingestionInfo?.streamName}`);
    return stream;
  }

  /**
   * Bind a broadcast to a stream
   */
  async bindBroadcastToStream(accessToken, broadcastId, streamId) {
    logger.info(`Binding broadcast ${broadcastId} to stream ${streamId}`);

    const response = await fetch(
      `${YOUTUBE_API_BASE}/liveBroadcasts/bind?id=${broadcastId}&streamId=${streamId}&part=id,contentDetails,snippet,status`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      const error = await response.json();
      logger.error(`YouTube bindBroadcast failed: ${JSON.stringify(error)}`);
      throw new Error(error.error?.message || 'Failed to bind broadcast to stream');
    }

    return response.json();
  }

  /**
   * Transition broadcast status (to 'live', 'complete', 'testing')
   */
  async transitionBroadcast(accessToken, broadcastId, status) {
    logger.info(`Transitioning broadcast ${broadcastId} to ${status}`);

    const response = await fetch(
      `${YOUTUBE_API_BASE}/liveBroadcasts/transition?broadcastStatus=${status}&id=${broadcastId}&part=id,status`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      const error = await response.json();
      logger.error(`YouTube transitionBroadcast failed: ${JSON.stringify(error)}`);
      throw new Error(error.error?.message || 'Failed to transition broadcast');
    }

    return response.json();
  }

  /**
   * List broadcasts for the authenticated user
   */
  async listBroadcasts(accessToken, broadcastStatus = 'all') {
    const response = await fetch(
      `${YOUTUBE_API_BASE}/liveBroadcasts?part=snippet,status,contentDetails&broadcastStatus=${broadcastStatus}&maxResults=10`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || 'Failed to list broadcasts');
    }

    return response.json();
  }

  /**
   * Get live chat messages
   */
  async getLiveChatMessages(accessToken, liveChatId, pageToken = '') {
    let url = `${YOUTUBE_API_BASE}/liveChat/messages?liveChatId=${liveChatId}&part=snippet,authorDetails&maxResults=200`;
    if (pageToken) url += `&pageToken=${pageToken}`;

    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || 'Failed to get chat messages');
    }

    return response.json();
  }

  /**
   * Get channel info for the authenticated user
   */
  async getChannelInfo(accessToken) {
    const response = await fetch(
      `${YOUTUBE_API_BASE}/channels?part=snippet,statistics&mine=true`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error?.message || 'Failed to get channel info');
    }

    return response.json();
  }
}

module.exports = new YouTubeService();
