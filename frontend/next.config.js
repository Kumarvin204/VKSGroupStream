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
    return [
      {
        source: '/api/stream/:path*',
        destination: 'http://localhost:4000/api/stream/:path*',
      },
      {
        source: '/api/youtube/:path*',
        destination: 'http://localhost:4000/api/youtube/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
