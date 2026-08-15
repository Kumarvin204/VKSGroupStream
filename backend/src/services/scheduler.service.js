const { v4: uuidv4 } = require('uuid');
const ffmpegService = require('./ffmpeg.service');
const logger = require('../utils/logger');
const fs = require('fs');
const path = require('path');

const slotsFilePath = path.join(__dirname, '../../uploads/slots.json');

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
    
    // Load persisted slots from slots.json on startup (with 1s delay to let server initialize)
    setTimeout(() => {
      this.loadSlots();
    }, 1000);
  }

  saveSlots() {
    try {
      const slotsArray = Array.from(this.slots.values());
      // Ensure directory exists
      const dir = path.dirname(slotsFilePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(slotsFilePath, JSON.stringify(slotsArray, null, 2), 'utf8');
      logger.info(`Saved active slots to persistence file: ${slotsFilePath}`);
    } catch (err) {
      logger.error(`Error saving slots to persistence file: ${err.message}`);
    }
  }

  loadSlots() {
    try {
      if (fs.existsSync(slotsFilePath)) {
        const data = fs.readFileSync(slotsFilePath, 'utf8');
        const loadedSlots = JSON.parse(data);
        const now = Date.now();
        
        logger.info(`Loaded ${loadedSlots.length} slots from persistence file`);
        
        for (const slotData of loadedSlots) {
          const endTime = new Date(slotData.endTime);
          if (endTime.getTime() > now) {
            logger.info(`Re-scheduling persistent slot on startup: ${slotData.title} (ID: ${slotData.id})`);
            this.scheduleSlotDirect(slotData);
          } else {
            // Stream has already ended while server was offline, cleanup its file
            deleteFile(slotData.filePath);
          }
        }
      }
    } catch (err) {
      logger.error(`Error loading persistent slots: ${err.message}`);
    }
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

    logger.info(`Scheduling new slot ${id} - ${title} from ${slot.startTime} to ${slot.endTime}`);
    this.scheduleSlotDirect(slot);
    this.saveSlots(); // Persist changes
    return slot;
  }

  scheduleSlotDirect(slot) {
    const id = slot.id;
    // Normalize dates to Date objects
    slot.startTime = new Date(slot.startTime);
    slot.endTime = new Date(slot.endTime);
    slot.status = 'scheduled';
    this.slots.set(id, slot);

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
      // Already started (or server restarted during stream)
      slot.status = 'live';
      logger.info(`Resuming/Starting file stream for slot ${id} immediately`);
      ffmpegService.startFileStream(id, slot.streamKey, slot.filePath, slot.loop);
    }

    if (endDelay > 0) {
      const endTimer = setTimeout(() => {
        const currentSlot = this.slots.get(id);
        if (currentSlot && currentSlot.status === 'live') {
          currentSlot.status = 'completed';
          logger.info(`Stopping scheduled stream for slot ${id}`);
          ffmpegService.stopStream(id);
          deleteFile(currentSlot.filePath);
          this.slots.delete(id);
          this.saveSlots(); // Save updated slots list
        }
      }, endDelay);
      
      this.timers.set(`${id}_end`, endTimer);
    } else {
      slot.status = 'completed';
      deleteFile(slot.filePath);
      this.slots.delete(id);
      this.saveSlots(); // Save updated slots list
    }
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

    // Remove the slot completely from memory and persistence file
    this.slots.delete(slotId);
    this.saveSlots();

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
