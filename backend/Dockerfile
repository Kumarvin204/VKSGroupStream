# Base image with Node.js 18
FROM node:18-slim

# Install system dependencies, specifically FFmpeg and FFprobe
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install application dependencies (omit devDependencies for production)
RUN npm ci --only=production

# Copy application source code
COPY . .

# Create uploads directory and grant write permissions for Hugging Face non-root user
RUN mkdir -p uploads && chmod -R 777 uploads

# Expose port (Hugging Face Spaces requires port 7860)
EXPOSE 7860

# Set environment variables defaults
ENV PORT=7860
ENV NODE_ENV=production
ENV FFMPEG_PATH=ffmpeg

# Start command
CMD ["npm", "start"]
