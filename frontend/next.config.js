/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    GOOGLE_MAPS_API_KEY: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY,
    API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL
  }
}

module.exports = nextConfig
