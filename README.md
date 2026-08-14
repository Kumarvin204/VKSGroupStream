# 🎬 YouTubeLiveStreamAdda

A custom cloud-based live streaming web application that allows users to broadcast webcam, screen share, and pre-recorded videos directly to **YouTube Live** via RTMP.

> **Built with:** Next.js · Tailwind CSS v3 · Zustand · Node.js · Express · WebSocket · FFmpeg

---

## 🏗️ Architecture

```
Browser (Next.js)                    Node.js Server                    YouTube
┌──────────────────┐     WebSocket    ┌──────────────────┐    RTMP     ┌──────────┐
│ Camera + Mic     │ ──────────────▶ │ WebSocket Server │ ─────────▶ │ YouTube  │
│ Screen Share     │  Binary Blobs   │ FFmpeg Process   │  FLV/H264  │ Live     │
│ Canvas Compositor│                 │ Stream Manager   │            │ 🔴 LIVE  │
└──────────────────┘                 └──────────────────┘            └──────────┘
```

---

## ⚡ Prerequisites

### 1. Node.js (v18+)
```bash
node --version  # Should be >= 18.0.0
```

### 2. FFmpeg (REQUIRED)

FFmpeg is used to transcode browser video (WebM) into RTMP format for YouTube.

**Windows Installation:**
```powershell
# Option 1: Using winget (recommended)
winget install Gyan.FFmpeg

# Option 2: Using Chocolatey
choco install ffmpeg

# Option 3: Manual Download
# Download from https://ffmpeg.org/download.html
# Extract and add the bin/ folder to your system PATH
```

**Verify installation:**
```bash
ffmpeg -version
```
You should see version info. If you get "command not found", FFmpeg is not in your PATH.

### 3. Google Cloud Console Setup

You need real Google OAuth credentials for YouTube integration:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable these APIs:
   - **YouTube Data API v3**
   - **YouTube Live Streaming API** (usually included with Data API)
4. Go to **APIs & Services → Credentials**
5. Create **OAuth 2.0 Client ID** (Web application type)
   - Authorized redirect URIs: `http://localhost:3000/api/auth/callback/google`
6. Copy the **Client ID** and **Client Secret**

---

## 🚀 Quick Start

### 1. Clone & Setup Backend
```bash
cd backend
cp .env.example .env
# Edit .env with your REAL Google OAuth credentials
npm install
npm run dev
```

Backend starts on **http://localhost:4000**

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend starts on **http://localhost:3000**

### 3. Verify Backend
```bash
# Health check
curl http://localhost:4000/api/health

# Expected response:
# { "status": "ok", "timestamp": "...", "activeStreams": 0, "uptime": "..." }
```

---

## 📁 Project Structure

```
Youttubelivestreamadda/
├── frontend/                # Next.js App (UI)
│   ├── src/
│   │   ├── app/            # Pages (App Router)
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks (media, streaming)
│   │   ├── store/          # Zustand stores
│   │   └── lib/            # Utilities & configs
│   └── package.json
│
├── backend/                 # Node.js Server
│   ├── src/
│   │   ├── server.js       # Express + WebSocket entry
│   │   ├── services/       # FFmpeg, Stream, YouTube services
│   │   ├── routes/         # REST API routes
│   │   ├── middleware/     # CORS, Auth
│   │   └── utils/          # Config, Logger
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## 🔧 Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in **real** values:

| Variable | Description | Required |
|----------|-------------|----------|
| `PORT` | Backend server port | Default: 4000 |
| `CORS_ORIGIN` | Frontend URL | Default: http://localhost:3000 |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | ✅ Yes |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Secret | ✅ Yes |
| `NEXTAUTH_SECRET` | Random 32-char string | ✅ Yes |
| `YOUTUBE_API_KEY` | YouTube Data API key | ✅ Yes |
| `FFMPEG_PATH` | Path to FFmpeg binary | Default: ffmpeg |

---

## 🔴 How Streaming Works

1. **Browser** captures camera/mic/screen → composites on `<canvas>`
2. **MediaRecorder** encodes canvas as WebM blobs
3. **WebSocket** sends binary blobs to Node.js server
4. **FFmpeg** receives blobs via stdin pipe, transcodes to H.264+AAC
5. **FFmpeg** pushes FLV to `rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}`
6. **YouTube** receives RTMP feed → channel goes **LIVE 🔴**

---

## 📜 License

MIT
