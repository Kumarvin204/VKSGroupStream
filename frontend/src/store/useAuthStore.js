import { create } from 'zustand';

const useAuthStore = create((set) => ({
  // Channel data from YouTube API
  channel: null,
  isLoadingChannel: false,
  channelError: null,

  // Active broadcast data
  activeBroadcast: null,
  activeStream: null,
  streamKey: null,
  rtmpUrl: null,

  setChannel: (channel) => set({ channel, channelError: null }),
  setLoadingChannel: (loading) => set({ isLoadingChannel: loading }),
  setChannelError: (error) => set({ channelError: error }),

  setActiveBroadcast: (broadcast) => set({ activeBroadcast: broadcast }),
  setActiveStream: (stream) => set({
    activeStream: stream,
    streamKey: stream?.cdn?.ingestionInfo?.streamName || null,
    rtmpUrl: stream?.cdn?.ingestionInfo?.ingestionAddress || null,
  }),
  setStreamData: ({ broadcast, streamKey }) => set({
    activeBroadcast: broadcast,
    streamKey: streamKey
  }),

  clearBroadcast: () => set({
    activeBroadcast: null,
    activeStream: null,
    streamKey: null,
    rtmpUrl: null,
  }),

  reset: () => set({
    channel: null,
    isLoadingChannel: false,
    channelError: null,
    activeBroadcast: null,
    activeStream: null,
    streamKey: null,
    rtmpUrl: null,
  }),
}));

export default useAuthStore;
