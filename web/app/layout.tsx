import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import JsonLd from "@/components/JsonLd";
import ThemeProvider from "@/components/ThemeProvider";
import ThemeToggle from "@/components/ThemeToggle";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://photopick.vercel.app";

const title = "PhotoPick — RAW + JPG pairing for macOS";
const description =
  "Free macOS app for photographers shooting RAW + JPG. Remove orphaned files and batch-move your picks into Lightroom in seconds.";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: title,
    template: "%s · PhotoPick",
  },
  description,
  applicationName: "PhotoPick",
  authors: [{ name: "Derek Lu", url: "https://derekdylu.com" }],
  creator: "Derek Lu",
  publisher: "Derek Lu",
  keywords: [
    "PhotoPick",
    "RAW JPG pairing",
    "RAW photo manager",
    "macOS photo app",
    "Lightroom workflow",
    "photo culling",
    "photography tools",
    "orphan files",
    "Canon CR3",
    "Nikon NEF",
    "Sony ARW",
    "Fuji RAF",
    "DNG",
    "Derek Lu",
  ],
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url: "/",
    siteName: "PhotoPick",
    title,
    description,
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title,
    description,
    creator: "@derekdylu",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
      "max-video-preview": -1,
    },
  },
  category: "technology",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
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
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <body className="font-sans antialiased">
        <JsonLd />
        <ThemeProvider>
          <ThemeToggle />
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
