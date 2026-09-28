// Central API base configuration for local dev, Vercel edge proxy, and Hugging Face static space
export const API_BASE = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/+$/, '');
