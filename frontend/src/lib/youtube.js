const YOUTUBE_API_BASE = 'https://www.googleapis.com/youtube/v3';

// Create a YouTube live broadcast
export async function createBroadcast(accessToken, { title, description, privacyStatus = 'public' }) {
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
          description,
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
    throw new Error(error.error?.message || 'Failed to create broadcast');
  }
  
  return response.json();
}

// Create a YouTube live stream (gets the RTMP URL and stream key)
export async function createStream(accessToken, { title = 'Stream' }) {
  const response = await fetch(
    `${YOUTUBE_API_BASE}/liveStreams?part=snippet,cdn,status`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        snippet: {
          title,
        },
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
    throw new Error(error.error?.message || 'Failed to create stream');
  }
  
  return response.json();
}

// Bind broadcast to stream
export async function bindBroadcastToStream(accessToken, broadcastId, streamId) {
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
    throw new Error(error.error?.message || 'Failed to bind broadcast to stream');
  }
  
  return response.json();
}

// Transition broadcast status (to 'testing' or 'live')
export async function transitionBroadcast(accessToken, broadcastId, status) {
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
    throw new Error(error.error?.message || 'Failed to transition broadcast');
  }
  
  return response.json();
}

// List user's live broadcasts
export async function listBroadcasts(accessToken, broadcastStatus = 'all') {
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

// Get live chat messages
export async function getLiveChatMessages(accessToken, liveChatId, pageToken = '') {
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

// Send a chat message
export async function sendChatMessage(accessToken, liveChatId, messageText) {
  const response = await fetch(
    `${YOUTUBE_API_BASE}/liveChat/messages?part=snippet`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        snippet: {
          liveChatId,
          type: 'textMessageEvent',
          textMessageDetails: {
            messageText,
          },
        },
      }),
    }
  );
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || 'Failed to send chat message');
  }
  
  return response.json();
}

// Get user's YouTube channel info
export async function getChannelInfo(accessToken) {
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
