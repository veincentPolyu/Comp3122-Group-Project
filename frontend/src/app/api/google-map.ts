// pages/api/google-maps.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const { query } = req; // Or req.body depending on your needs

    // Construct the Google Maps API URL with the key on the server-side
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

    if (!apiKey) {
      throw new Error("Google Maps API key is missing");
    }
    const baseUrl = 'https://maps.googleapis.com/maps/api/js';
    const url = `${baseUrl}?key=${apiKey}&libraries=places,marker&v=beta`;

    // Fetch the Google Maps API script (or data)
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Google Maps API request failed with status: ${response.status}`);
    }
      const data = await response.text();
      res.setHeader('Content-Type', 'application/javascript'); // Important: Set the correct content type
      res.status(200).send(data);


  } catch (error: any) {
    console.error("Error fetching Google Maps API:", error);
    res.status(500).json({ error: error.message || "Failed to fetch Google Maps API" });
  }
}
