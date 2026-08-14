import { useEffect, useCallback } from 'react';
import useStudioStore from '../store/useStudioStore';

const useMediaDevices = () => {
  const {
    localStream,
    setLocalStream,
    setDevices,
    selectedCamera,
    setSelectedCamera,
    selectedMic,
    setSelectedMic,
    isMicMuted,
    isCamOff
  } = useStudioStore();

  const getDevices = useCallback(async () => {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      setDevices(devices);
      
      const cameras = devices.filter(d => d.kind === 'videoinput');
      const mics = devices.filter(d => d.kind === 'audioinput');
      
      if (!selectedCamera && cameras.length > 0) {
        setSelectedCamera(cameras[0].deviceId);
      }
      if (!selectedMic && mics.length > 0) {
        setSelectedMic(mics[0].deviceId);
      }
    } catch (err) {
      console.error('Error enumerating devices:', err);
    }
  }, [setDevices, selectedCamera, setSelectedCamera, selectedMic, setSelectedMic]);

  const requestPermissions = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      stream.getTracks().forEach(track => track.stop());
      await getDevices();
    } catch (err) {
      console.error('Error requesting permissions:', err);
    }
  }, [getDevices]);

  const startPreview = useCallback(async () => {
    try {
      if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
      }
      
      const constraints = {
        video: selectedCamera ? { deviceId: { exact: selectedCamera } } : true,
        audio: selectedMic ? { deviceId: { exact: selectedMic } } : true
      };
      
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      
      // Apply initial mute states
      stream.getAudioTracks().forEach(track => { track.enabled = !isMicMuted; });
      stream.getVideoTracks().forEach(track => { track.enabled = !isCamOff; });
      
      setLocalStream(stream);
      await getDevices();
    } catch (err) {
      console.error('Error starting preview:', err);
    }
  }, [localStream, selectedCamera, selectedMic, isMicMuted, isCamOff, setLocalStream, getDevices]);

  const stopPreview = useCallback(() => {
    if (localStream) {
      localStream.getTracks().forEach(track => track.stop());
      setLocalStream(null);
    }
  }, [localStream, setLocalStream]);

  const changeCamera = useCallback(async (deviceId) => {
    setSelectedCamera(deviceId);
    if (!localStream) return;
    
    try {
      const videoConstraints = { video: { deviceId: { exact: deviceId } } };
      const newStream = await navigator.mediaDevices.getUserMedia(videoConstraints);
      
      const oldVideoTracks = localStream.getVideoTracks();
      oldVideoTracks.forEach(track => {
        track.stop();
        localStream.removeTrack(track);
      });
      
      const newVideoTrack = newStream.getVideoTracks()[0];
      newVideoTrack.enabled = !isCamOff;
      localStream.addTrack(newVideoTrack);
    } catch (err) {
      console.error('Error changing camera:', err);
    }
  }, [localStream, setSelectedCamera, isCamOff]);

  const changeMic = useCallback(async (deviceId) => {
    setSelectedMic(deviceId);
    if (!localStream) return;
    
    try {
      const audioConstraints = { audio: { deviceId: { exact: deviceId } } };
      const newStream = await navigator.mediaDevices.getUserMedia(audioConstraints);
      
      const oldAudioTracks = localStream.getAudioTracks();
      oldAudioTracks.forEach(track => {
        track.stop();
        localStream.removeTrack(track);
      });
      
      const newAudioTrack = newStream.getAudioTracks()[0];
      newAudioTrack.enabled = !isMicMuted;
      localStream.addTrack(newAudioTrack);
    } catch (err) {
      console.error('Error changing mic:', err);
    }
  }, [localStream, setSelectedMic, isMicMuted]);

  useEffect(() => {
    navigator.mediaDevices.addEventListener('devicechange', getDevices);
    return () => {
      navigator.mediaDevices.removeEventListener('devicechange', getDevices);
      stopPreview();
    };
  }, [getDevices, stopPreview]);

  return { requestPermissions, startPreview, stopPreview, changeCamera, changeMic };
};

export default useMediaDevices;
