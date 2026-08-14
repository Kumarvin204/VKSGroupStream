import { useCallback, useEffect } from 'react';
import useStudioStore from '../store/useStudioStore';

const useScreenShare = () => {
  const {
    screenStream,
    setScreenStream,
    setScreenSharing
  } = useStudioStore();

  const stopScreenShare = useCallback(() => {
    if (screenStream) {
      screenStream.getTracks().forEach(track => track.stop());
      setScreenStream(null);
      setScreenSharing(false);
    }
  }, [screenStream, setScreenStream, setScreenSharing]);

  const startScreenShare = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: true
      });
      
      stream.getVideoTracks()[0].onended = () => {
        stopScreenShare();
      };
      
      setScreenStream(stream);
      setScreenSharing(true);
    } catch (err) {
      console.error('Error starting screen share:', err);
      setScreenSharing(false);
    }
  }, [setScreenStream, setScreenSharing, stopScreenShare]);

  useEffect(() => {
    return () => {
      if (screenStream) {
        screenStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [screenStream]);

  return { startScreenShare, stopScreenShare };
};

export default useScreenShare;
