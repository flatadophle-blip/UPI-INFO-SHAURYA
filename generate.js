export default async function handler(req, res) {
  const { prompt } = req.query;

  if (!prompt) {
    res.status(400).json({ error: "prompt parameter required" });
    return;
  }

  // 🔑 HARD-CODED KEY
  const SPLEXXO_KEY = "SPLEXXO";

  const apiUrl =
    "https://splexx-api-img.vercel.app/api/imggen" +
    `?text=${encodeURIComponent(prompt)}` +
    `&key=${SPLEXXO_KEY}`;

  try {
    const response = await fetch(apiUrl);

    if (!response.ok) {
      res.status(500).json({ error: "Failed to generate image" });
      return;
    }

    // 🔥 Direct image bytes
    const buffer = Buffer.from(await response.arrayBuffer());

    res.setHeader("Content-Type", "image/png");
    res.setHeader("Cache-Control", "no-store");

    res.status(200).send(buffer);
  } catch (err) {
    res.status(500).json({ error: "Server error" });
  }
}
