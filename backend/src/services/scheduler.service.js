const { v4: uuidv4 } = require('uuid');
const ffmpegService = require('./ffmpeg.service');
const logger = require('../utils/logger');
const fs = require('fs');

// Helper to safely delete video file from disk to save space
function deleteFile(filePath) {
  if (filePath && fs.existsSync(filePath)) {
    fs.unlink(filePath, (err) => {
      if (err) {
        logger.error(`Error deleting video file ${filePath}: ${err.message}`);
      } else {
        logger.info(`Successfully deleted video file from disk: ${filePath}`);
      }
    });
  }
}


class SchedulerService {
  constructor() {
    this.slots = new Map();
    this.timers = new Map();
  }

  scheduleSlot(slotData) {
    const { title, startTime, endTime, streamKey, filePath, loop = false } = slotData;
    
    const id = uuidv4();
    const slot = {
      id,
      title,
      startTime: new Date(startTime),
      endTime: new Date(endTime),
      streamKey,
      filePath,
      loop,
      status: 'scheduled'
    };

    this.slots.set(id, slot);
    logger.info(`Scheduled slot ${id} - ${title} from ${slot.startTime} to ${slot.endTime}`);

    const now = Date.now();
    const startDelay = slot.startTime.getTime() - now;
    const endDelay = slot.endTime.getTime() - now;

    if (startDelay > 0) {
      const startTimer = setTimeout(() => {
        const currentSlot = this.slots.get(id);
        if (currentSlot && currentSlot.status === 'scheduled') {
          currentSlot.status = 'live';
          logger.info(`Starting scheduled stream for slot ${id}`);
          ffmpegService.startFileStream(id, currentSlot.streamKey, currentSlot.filePath, currentSlot.loop);
        }
      }, startDelay);
      
      this.timers.set(`${id}_start`, startTimer);
    } else if (endDelay > 0) {
      // Already started
      slot.status = 'live';
      ffmpegService.startFileStream(id, streamKey, filePath, loop);
    }

    if (endDelay > 0) {
      const endTimer = setTimeout(() => {
        const currentSlot = this.slots.get(id);
        if (currentSlot && currentSlot.status === 'live') {
          currentSlot.status = 'completed';
          logger.info(`Stopping scheduled stream for slot ${id}`);
          ffmpegService.stopStream(id);
          // Delete file upon natural completion to save server storage space
          deleteFile(currentSlot.filePath);
          // Remove slot from memory so it is fully cleaned up from the dashboard list
          this.slots.delete(id);
        }
      }, endDelay);
      
      this.timers.set(`${id}_end`, endTimer);
    } else {
      slot.status = 'completed';
      // If it has already completed, delete the file immediately
      deleteFile(filePath);
      // Remove from slot list
      this.slots.delete(id);
    }

    return slot;
  }

  cancelSlot(slotId) {
    const slot = this.slots.get(slotId);
    if (!slot) return false;

    if (slot.status === 'live') {
      ffmpegService.stopStream(slotId);
    }

    // Delete the file immediately from disk
    deleteFile(slot.filePath);

    const startTimer = this.timers.get(`${slotId}_start`);
    if (startTimer) {
      clearTimeout(startTimer);
      this.timers.delete(`${slotId}_start`);
    }

    const endTimer = this.timers.get(`${slotId}_end`);
    if (endTimer) {
      clearTimeout(endTimer);
      this.timers.delete(`${slotId}_end`);
    }

    // Remove the slot completely from memory to clean it from the project dashboard
    this.slots.delete(slotId);

    logger.info(`Cancelled and fully deleted slot ${slotId} from project`);
    return true;
  }

  getSlots() {
    return Array.from(this.slots.values());
  }

  getSlot(id) {
    return this.slots.get(id);
  }
}

module.exports = new SchedulerService();
