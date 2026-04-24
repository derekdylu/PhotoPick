import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "PhotoPick",
    short_name: "PhotoPick",
    description:
      "A lightweight macOS app for photographers who shoot RAW + JPG. Remove orphans and batch-move picks into Lightroom.",
    start_url: "/",
    display: "standalone",
    background_color: "#ffffff",
    theme_color: "#2F6FEB",
    categories: ["photo", "productivity", "utilities"],
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/icon-512.png", sizes: "512x512", type: "image/png" },
      {
        src: "/icon-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
  };
}
