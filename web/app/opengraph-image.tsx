import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "PhotoPick — RAW + JPG pairing for macOS";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          justifyContent: "center",
          padding: "80px",
          background:
            "linear-gradient(135deg, #0b2447 0%, #19376d 45%, #2f6feb 100%)",
          color: "#ffffff",
          fontFamily: "system-ui, sans-serif",
        }}
      >
        <div
          style={{
            fontSize: 28,
            letterSpacing: 4,
            textTransform: "uppercase",
            opacity: 0.8,
          }}
        >
          PhotoPick
        </div>
        <div
          style={{
            fontSize: 88,
            fontWeight: 800,
            lineHeight: 1.05,
            marginTop: 24,
            maxWidth: 1000,
          }}
        >
          RAW + JPG, paired. Orphans, gone.
        </div>
        <div
          style={{
            fontSize: 34,
            marginTop: 28,
            opacity: 0.85,
            maxWidth: 900,
          }}
        >
          A lightweight macOS app for photographers who shoot dual-format.
        </div>
        <div
          style={{
            marginTop: 56,
            fontSize: 24,
            opacity: 0.7,
          }}
        >
          by Derek Lu · derekdylu.com
        </div>
      </div>
    ),
    { ...size }
  );
}
