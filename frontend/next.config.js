/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [
      'lh3.googleusercontent.com',  // Google profile images
      'yt3.ggpht.com',              // YouTube channel avatars
      'i.ytimg.com',                // YouTube thumbnails
    ],
  },
  // Proxy API calls to backend during development
  async rewrites() {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:4000';
    return [
      {
        source: '/api/stream/:path*',
        destination: `${backendUrl}/api/stream/:path*`,
      },
      {
        source: '/api/youtube/:path*',
        destination: `${backendUrl}/api/youtube/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
