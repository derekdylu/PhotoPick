import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import JsonLd from "@/components/JsonLd";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://photopick.vercel.app";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "PhotoPick — RAW + JPG pairing for macOS",
    template: "%s · PhotoPick",
  },
  description:
    "A lightweight macOS app for photographers who shoot RAW + JPG. Remove orphans, batch-move picks into Lightroom — in seconds.",
  applicationName: "PhotoPick",
  authors: [{ name: "Derek Lu", url: "https://derekdylu.com" }],
  creator: "Derek Lu",
  publisher: "Derek Lu",
  keywords: [
    "PhotoPick",
    "RAW JPG pairing",
    "macOS photo app",
    "Lightroom workflow",
    "photography tools",
    "orphan files",
    "Derek Lu",
  ],
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url: "/",
    siteName: "PhotoPick",
    title: "PhotoPick — RAW + JPG pairing for macOS",
    description:
      "Remove orphaned RAW/JPG files and batch-move your picks into Lightroom. Built for dual-format photographers.",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "PhotoPick — RAW + JPG pairing for macOS",
    description:
      "Remove orphaned RAW/JPG files and batch-move your picks into Lightroom. Built for dual-format photographers.",
    creator: "@derekdylu",
  },
  icons: {
    icon: [{ url: "/PhotoPick.png", type: "image/png" }],
    apple: [{ url: "/PhotoPick.png", type: "image/png" }],
  },
  category: "technology",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#07090f" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans antialiased">
        <JsonLd />
        {children}
      </body>
    </html>
  );
}
