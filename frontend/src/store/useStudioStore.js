import { create } from 'zustand';

const useStudioStore = create((set, get) => ({
  localStream: null,
  screenStream: null,
  isMicMuted: false,
  isCamOff: false,
  isScreenSharing: false,
  devices: [],
  selectedCamera: '',
  selectedMic: '',
  layout: 'grid', // 'grid', 'sidebar', 'presentation'
  isLive: false,
  sessionId: null,
  canvasStream: null,
  chatMessages: [],
  streamQuality: { width: 1280, height: 720, frameRate: 30 },

  setLocalStream: (stream) => set({ localStream: stream }),
  
  setScreenStream: (stream) => set({ screenStream: stream }),
  
  toggleMic: () => {
    const { localStream, isMicMuted } = get();
    if (localStream) {
      localStream.getAudioTracks().forEach(track => {
        track.enabled = isMicMuted;
      });
    }
    set({ isMicMuted: !isMicMuted });
  },

  toggleCam: () => {
    const { localStream, isCamOff } = get();
    if (localStream) {
      localStream.getVideoTracks().forEach(track => {
        track.enabled = isCamOff;
      });
    }
    set({ isCamOff: !isCamOff });
  },

  setScreenSharing: (sharing) => set({ isScreenSharing: sharing }),
  
  setDevices: (devices) => set({ devices }),
  
  setSelectedCamera: (deviceId) => set({ selectedCamera: deviceId }),
  
  setSelectedMic: (deviceId) => set({ selectedMic: deviceId }),
  
  setLayout: (layout) => set({ layout }),
  
  setIsLive: (isLive) => set({ isLive }),
  
  setSessionId: (sessionId) => set({ sessionId }),
  
  setCanvasStream: (stream) => set({ canvasStream: stream }),
  
  addChatMessage: (msg) => set((state) => ({ chatMessages: [...state.chatMessages, msg] })),
  
  setChatMessages: (messages) => set({ chatMessages: messages }),
  
  clearChat: () => set({ chatMessages: [] }),
  
  reset: () => {
    const { localStream, screenStream, canvasStream } = get();
    [localStream, screenStream, canvasStream].forEach(stream => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    });
    set({
      localStream: null,
      screenStream: null,
      isMicMuted: false,
      isCamOff: false,
      isScreenSharing: false,
      devices: [],
      selectedCamera: '',
      selectedMic: '',
      layout: 'grid',
      isLive: false,
      sessionId: null,
      canvasStream: null,
      chatMessages: []
    });
  }
}));

export default useStudioStore;
