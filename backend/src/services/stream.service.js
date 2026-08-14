const crypto = require('crypto');

class StreamService {
  constructor() {
    this.sessions = new Map();
  }

  createSession(streamKey) {
    const id = crypto.randomUUID();
    const session = {
      id,
      streamKey,
      status: 'idle',
      startedAt: new Date(),
      stoppedAt: null,
      metadata: {}
    };
    this.sessions.set(id, session);
    return session;
  }

  getSession(id) {
    return this.sessions.get(id);
  }

  updateSession(id, updates) {
    const session = this.sessions.get(id);
    if (session) {
      Object.assign(session, updates);
      this.sessions.set(id, session);
      return session;
    }
    return null;
  }

  removeSession(id) {
    return this.sessions.delete(id);
  }

  getAllSessions() {
    return Array.from(this.sessions.values());
  }

  getActiveSessions() {
    return this.getAllSessions().filter(s => s.status === 'live' || s.status === 'connecting');
  }
}

module.exports = new StreamService();
