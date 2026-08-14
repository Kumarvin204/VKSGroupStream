import { useRef, useCallback, useEffect } from 'react';
import useStudioStore from '@/store/useStudioStore';

export const useStreamSocket = () => {
  const canvasStream = useStudioStore((state) => state.canvasStream);
  const setIsLive = useStudioStore((state) => state.setIsLive);

  const wsRef = useRef(null);
  const mediaRecorderRef = useRef(null);

  const cleanup = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (wsRef.current && (wsRef.current.readyState === WebSocket.OPEN || wsRef.current.readyState === WebSocket.CONNECTING)) {
      wsRef.current.close();
    }
    mediaRecorderRef.current = null;
    wsRef.current = null;
    setIsLive(false);
  }, [setIsLive]);

  const startStreaming = useCallback(
    (streamKey) => {
      if (!canvasStream) {
        console.error('No canvas stream available to start streaming.');
        return;
      }

      if (!streamKey) {
        console.error('No stream key provided.');
        return;
      }

      const wsUrl = `ws://localhost:4000/ws/stream?streamKey=${streamKey}`;
      const socket = new WebSocket(wsUrl);
      socket.binaryType = 'arraybuffer';
      wsRef.current = socket;

      socket.onopen = () => {
        console.log('WebSocket connection opened');
        
        let mimeType = 'video/webm;codecs=vp8,opus';
        if (!MediaRecorder.isTypeSupported(mimeType)) {
          mimeType = 'video/webm;codecs=vp9,opus';
          if (!MediaRecorder.isTypeSupported(mimeType)) {
            mimeType = 'video/webm'; // fallback
          }
        }

        const mediaRecorder = new MediaRecorder(canvasStream, { mimeType });
        mediaRecorderRef.current = mediaRecorder;

        mediaRecorder.ondataavailable = async (event) => {
          if (event.data && event.data.size > 0 && socket.readyState === WebSocket.OPEN) {
            try {
              const arrayBuffer = await event.data.arrayBuffer();
              socket.send(arrayBuffer);
            } catch (error) {
              console.error('Error sending arraybuffer data to websocket:', error);
            }
          }
        };

        mediaRecorder.onstop = () => {
          console.log('MediaRecorder stopped');
        };

        // 250ms timeslice
        mediaRecorder.start(250);
        setIsLive(true);
      };

      socket.onclose = (event) => {
        console.log('WebSocket connection closed', event.code, event.reason);
        cleanup();
      };

      socket.onerror = (error) => {
        console.error('WebSocket encountered an error:', error);
        cleanup();
      };
    },
    [canvasStream, setIsLive, cleanup]
  );

  const stopStreaming = useCallback(() => {
    cleanup();
  }, [cleanup]);

  useEffect(() => {
    return () => {
      cleanup();
    };
  }, [cleanup]);

  return { startStreaming, stopStreaming };
};
