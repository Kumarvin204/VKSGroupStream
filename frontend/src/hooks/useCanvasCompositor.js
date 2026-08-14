import { useEffect, useRef } from 'react';
import useStudioStore from '../store/useStudioStore';

const drawRoundedRect = (ctx, x, y, width, height, radius) => {
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
};

const drawVideoElement = (ctx, videoEl, x, y, width, height, radius = 0) => {
  if (videoEl.readyState >= 2) {
    ctx.save();
    if (radius > 0) {
      drawRoundedRect(ctx, x, y, width, height, radius);
      ctx.clip();
    }
    
    // Fit to cover
    const videoRatio = videoEl.videoWidth / videoEl.videoHeight;
    const boxRatio = width / height;
    let drawWidth = width;
    let drawHeight = height;
    let drawX = x;
    let drawY = y;
    
    if (videoRatio > boxRatio) {
      drawWidth = height * videoRatio;
      drawX = x - (drawWidth - width) / 2;
    } else {
      drawHeight = width / videoRatio;
      drawY = y - (drawHeight - height) / 2;
    }
    
    ctx.drawImage(videoEl, drawX, drawY, drawWidth, drawHeight);
    ctx.restore();
  } else {
    ctx.fillStyle = '#222';
    if (radius > 0) {
      drawRoundedRect(ctx, x, y, width, height, radius);
      ctx.fill();
    } else {
      ctx.fillRect(x, y, width, height);
    }
  }
};

const useCanvasCompositor = (canvasRef) => {
  const { localStream, screenStream, layout, setCanvasStream } = useStudioStore();
  const requestRef = useRef();
  const localVideoRef = useRef(document.createElement('video'));
  const screenVideoRef = useRef(document.createElement('video'));

  // Setup video elements
  useEffect(() => {
    const localVideo = localVideoRef.current;
    localVideo.muted = true;
    localVideo.autoplay = true;
    localVideo.playsInline = true;
    
    if (localStream) {
      localVideo.srcObject = localStream;
      localVideo.play().catch(console.error);
    } else {
      localVideo.srcObject = null;
    }
  }, [localStream]);

  useEffect(() => {
    const screenVideo = screenVideoRef.current;
    screenVideo.muted = true;
    screenVideo.autoplay = true;
    screenVideo.playsInline = true;
    
    if (screenStream) {
      screenVideo.srcObject = screenStream;
      screenVideo.play().catch(console.error);
    } else {
      screenVideo.srcObject = null;
    }
  }, [screenStream]);

  // Main render loop
  useEffect(() => {
    if (!canvasRef || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d', { alpha: false });
    
    // Set internal resolution
    const width = 1280;
    const height = 720;
    canvas.width = width;
    canvas.height = height;

    const render = () => {
      // Clear background
      ctx.fillStyle = '#0f172a'; // slate-900
      ctx.fillRect(0, 0, width, height);

      const hasLocal = !!localStream;
      const hasScreen = !!screenStream;
      const localVideo = localVideoRef.current;
      const screenVideo = screenVideoRef.current;

      if (hasLocal && !hasScreen) {
        drawVideoElement(ctx, localVideo, 0, 0, width, height);
      } else if (!hasLocal && hasScreen) {
        drawVideoElement(ctx, screenVideo, 0, 0, width, height);
      } else if (hasLocal && hasScreen) {
        if (layout === 'grid') {
          // Side-by-side
          const margin = 20;
          const boxWidth = (width - margin * 3) / 2;
          const boxHeight = height - margin * 2;
          
          // Screen left, Camera right
          drawVideoElement(ctx, screenVideo, margin, margin, boxWidth, boxHeight, 16);
          drawVideoElement(ctx, localVideo, margin * 2 + boxWidth, margin, boxWidth, boxHeight, 16);
          
        } else if (layout === 'sidebar') {
          // Screen big on left, cam smaller on right
          const margin = 20;
          const rightColWidth = 300;
          const leftColWidth = width - margin * 3 - rightColWidth;
          
          drawVideoElement(ctx, screenVideo, margin, margin, leftColWidth, height - margin * 2, 16);
          
          const camHeight = rightColWidth * (9/16);
          drawVideoElement(ctx, localVideo, margin * 2 + leftColWidth, margin, rightColWidth, camHeight, 16);
          
        } else if (layout === 'presentation') {
          // Screen full, cam bottom right PIP
          drawVideoElement(ctx, screenVideo, 0, 0, width, height);
          
          const pipWidth = 280;
          const pipHeight = pipWidth * (9/16);
          const margin = 20;
          
          drawVideoElement(ctx, localVideo, width - pipWidth - margin, height - pipHeight - margin, pipWidth, pipHeight, 12);
        }
      }

      // Draw Logo
      ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
      ctx.font = 'bold 24px Arial, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('VKSGroupStream', width - 20, 40);
      
      // Draw User Name if local is active
      if (hasLocal) {
        let nameX = 0;
        let nameY = 0;
        
        if (!hasScreen) {
          nameX = 30;
          nameY = height - 30;
        } else if (layout === 'grid') {
          const margin = 20;
          const boxWidth = (width - margin * 3) / 2;
          nameX = margin * 2 + boxWidth + 15;
          nameY = height - margin - 15;
        } else if (layout === 'sidebar') {
          const margin = 20;
          const rightColWidth = 300;
          const leftColWidth = width - margin * 3 - rightColWidth;
          nameX = margin * 2 + leftColWidth + 15;
          const camHeight = rightColWidth * (9/16);
          nameY = margin + camHeight - 15;
        } else if (layout === 'presentation') {
          const pipWidth = 280;
          const margin = 20;
          nameX = width - pipWidth - margin + 10;
          nameY = height - margin - 10;
        }
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(nameX - 5, nameY - 25, 120, 32);
        ctx.fillStyle = '#fff';
        ctx.font = '16px Arial, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('Host', nameX, nameY - 3);
      }

      requestRef.current = requestAnimationFrame(render);
    };

    requestRef.current = requestAnimationFrame(render);

    // Create Canvas stream
    const canvasStreamObj = canvas.captureStream(30);
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const destination = audioContext.createMediaStreamDestination();
    
    let hasAudio = false;

    if (localStream && localStream.getAudioTracks().length > 0) {
      const localAudioSource = audioContext.createMediaStreamSource(
        new MediaStream([localStream.getAudioTracks()[0]])
      );
      localAudioSource.connect(destination);
      hasAudio = true;
    }

    if (screenStream && screenStream.getAudioTracks().length > 0) {
      const screenAudioSource = audioContext.createMediaStreamSource(
        new MediaStream([screenStream.getAudioTracks()[0]])
      );
      screenAudioSource.connect(destination);
      hasAudio = true;
    }

    if (hasAudio) {
      destination.stream.getAudioTracks().forEach(track => {
        canvasStreamObj.addTrack(track);
      });
    }

    setCanvasStream(canvasStreamObj);

    return () => {
      cancelAnimationFrame(requestRef.current);
      if (canvasStreamObj) {
        canvasStreamObj.getTracks().forEach(track => track.stop());
      }
      if (audioContext.state !== 'closed') {
        audioContext.close();
      }
    };
  }, [canvasRef, localStream, screenStream, layout, setCanvasStream]);

};

export default useCanvasCompositor;
