const { spawn } = require('child_process');
const config = require('../utils/config');
const logger = require('../utils/logger');

class FFmpegService {
  constructor() {
    this.processes = new Map();
  }

  startStream(sessionId, streamKey) {
    const rtmpUrl = `${config.YOUTUBE_RTMP_BASE_URL}/${streamKey}`;
    
    logger.info(`Starting FFmpeg for session ${sessionId}`);
    
    const args = [
      '-f', 'webm',                            // Input container format (MediaRecorder WebM blobs)
      '-i', 'pipe:0',                          // Stdin pipe
      '-c:v', 'libx264',                       // Transcode video to H.264
      '-preset', 'ultrafast',                  // Ultrafast preset to ensure real-time speed (> 1.0x) under low CPU
      '-tune', 'zerolatency',                  // Zero latency tuning for instant stream ingestion
      '-threads', '0',                         // Let FFmpeg automatically choose the optimal thread count
      '-r', '30',                              // Force exactly 30 FPS output
      '-fps_mode', 'cfr',                      // Force constant frame rate to prevent timestamp gaps on variable camera FPS
      '-g', '60',                              // Force GOP size of 60 (exactly 2 seconds at 30 FPS)
      '-keyint_min', '60',                     // Minimum GOP size (prevents variable keyframes)
      '-sc_threshold', '0',                    // Disable scene cut detection to lock GOP frequency
      '-b:v', '3000k',                         // Target video bitrate (3 Mbps - Sweet spot for home upload speed)
      '-minrate', '3000k',                     // Min video bitrate (forces constant bitrate control)
      '-maxrate', '3000k',                     // Max video bitrate
      '-bufsize', '6000k',                     // Buffer size (2x bitrate)
      '-pix_fmt', 'yuv420p',                   // Force YUV 4:2:0 pixel format for standard playback
      '-c:a', 'aac',                           // Transcode audio to AAC
      '-b:a', '128k',                          // Audio bitrate
      '-ac', '2',                              // Force stereo channels
      '-ar', '44100',                          // Audio sample rate (44.1 kHz)
      '-f', 'flv',                             // Output FLV container (required for RTMP)
      rtmpUrl                                  // Target RTMP URL
    ];

    const ffmpegProcess = spawn(config.FFMPEG_PATH, args);

    this.processes.set(sessionId, ffmpegProcess);

    ffmpegProcess.stderr.on('data', (data) => {
      const message = data.toString();
      // Optional: Parse for fps, bitrate, etc., but here we just log it as debug/info
      // logger.debug(`FFmpeg (${sessionId}): ${message.trim()}`);
    });

    ffmpegProcess.on('close', (code) => {
      logger.info(`FFmpeg process for session ${sessionId} exited with code ${code}`);
      this.processes.delete(sessionId);
    });

    ffmpegProcess.on('error', (err) => {
      logger.error(`FFmpeg process error for session ${sessionId}: ${err.message}`);
    });

    return ffmpegProcess;
  }

  startFileStream(sessionId, streamKey, filePath, loop = false) {
    const rtmpUrl = `${config.YOUTUBE_RTMP_BASE_URL}/${streamKey}`;
    
    logger.info(`Starting file stream for session ${sessionId}, file: ${filePath}, loop: ${loop}`);
    
    const args = [
      '-fflags', '+genpts',                    // Generate missing presentation timestamps (PTS) from input file
      ...(process.platform === 'win32' ? ['-hwaccel', 'd3d11va'] : []), // Only use Direct3D 11 hardware decoding on Windows host locally, omit on Linux cloud servers
      '-thread_queue_size', '4096',             // Increase thread queue buffer size to handle non-interleaved mobile video tracks
      '-re',                                   // Read input video file at native frame rate (essential for files)
      '-readrate_initial_burst', '20.0',       // Initial 20-second read burst to fill the network buffers and prevent initial lags
      ...(loop ? ['-stream_loop', '-1'] : []), // Loop input infinitely if specified
      '-i', filePath,                          // Target video file input path
      '-map', '0:v',                           // Map only video stream to discard non-synchronized Apple metadata/timecode tracks
      '-map', '0:a',                           // Map only audio stream
      '-c:v', 'libx264',                       // Transcode video to H.264
      '-preset', 'ultrafast',                  // Ultrafast preset to prevent CPU choke on loops
      '-vf', "scale=w='if(gt(ih,iw),if(gte(ih/iw,1280/720),-2,720),if(gte(ih/iw,720/1280),-2,1280))':h='if(gt(ih,iw),if(gte(ih/iw,1280/720),1280,-2),if(gte(ih/iw,720/1280),720,-2))',pad=w='if(gt(ih,iw),720,1280)':h='if(gt(ih,iw),1280,720)':x='(ow-iw)/2':y='(oh-ih)/2':color=black", // Auto-detect orientation: output 1280x720 for landscape or 720x1280 for portrait to avoid windowboxing on mobile viewports
      '-threads', '0',                         // Let FFmpeg automatically choose the optimal number of threads based on CPU cores
      '-r', '30',                              // Force output frame rate of 30 FPS
      '-fps_mode', 'cfr',                      // Force Constant Frame Rate (CFR) to prevent mobile video timestamp drift
      '-g', '60',                              // Force keyframe every 60 frames (exactly 2 seconds)
      '-keyint_min', '60',                     // Lock minimum keyframe interval
      '-sc_threshold', '0',                    // Disable scene cut keyframe triggers
      '-b:v', '3000k',                         // Target video bitrate (3 Mbps - Sweet spot for home connections)
      '-minrate', '3000k',                     // Min video bitrate (forces constant bitrate control)
      '-maxrate', '3000k',                     // Max video bitrate
      '-bufsize', '6000k',                     // Buffer size (2x bitrate)
      '-pix_fmt', 'yuv420p',                   // Force YUV 4:2:0 pixel format
      '-c:a', 'aac',                           // Transcode audio to AAC
      '-b:a', '128k',                          // Audio bitrate
      '-ac', '2',                              // Force stereo
      '-ar', '44100',                          // Audio sample rate (44.1 kHz)
      '-max_muxing_queue_size', '1024',        // Allow larger muxing queues to prevent bottleneck on network write delays
      '-f', 'flv',                             // FLV container for RTMP push
      rtmpUrl                                  // Target RTMP URL
    ];

    const ffmpegProcess = spawn(config.FFMPEG_PATH, args);

    this.processes.set(sessionId, ffmpegProcess);

    ffmpegProcess.stderr.on('data', (data) => {
      logger.info(`FFmpeg (${sessionId}): ${data.toString().trim()}`);
    });

    ffmpegProcess.on('close', (code) => {
      logger.info(`FFmpeg file process for session ${sessionId} exited with code ${code}`);
      this.processes.delete(sessionId);
    });

    ffmpegProcess.on('error', (err) => {
      logger.error(`FFmpeg file process error for session ${sessionId}: ${err.message}`);
    });

    return ffmpegProcess;
  }

  writeData(sessionId, data) {
    const process = this.processes.get(sessionId);
    if (process && process.stdin.writable) {
      return process.stdin.write(data);
    }
    return false;
  }

  stopStream(sessionId) {
    const process = this.processes.get(sessionId);
    if (process) {
      logger.info(`Stopping stream for session ${sessionId}`);
      process.stdin.end();
      process.kill('SIGTERM');
      
      setTimeout(() => {
        if (this.processes.has(sessionId)) {
          logger.warn(`Force killing FFmpeg for session ${sessionId}`);
          const p = this.processes.get(sessionId);
          if (p) p.kill('SIGKILL');
        }
      }, 5000);
      
      this.processes.delete(sessionId);
    }
  }

  stopAll() {
    logger.info('Stopping all active FFmpeg streams');
    for (const sessionId of this.processes.keys()) {
      this.stopStream(sessionId);
    }
  }

  getActiveStreams() {
    return Array.from(this.processes.keys());
  }

  isStreaming(sessionId) {
    return this.processes.has(sessionId);
  }
}

module.exports = new FFmpegService();
