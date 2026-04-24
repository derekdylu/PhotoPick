import type { Metadata } from "next";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import Screenshots from "@/components/Screenshots";
import SupportedCameras from "@/components/SupportedCameras";
import FAQ from "@/components/FAQ";
import DownloadCTA from "@/components/DownloadCTA";
import Footer from "@/components/Footer";
import JsonLd from "@/components/JsonLd";

const title = "PhotoPick — macOS 上的 RAW + JPG 配對工具";
const description =
  "免費開放原始碼的 macOS 應用程式，為同時拍攝 RAW + JPG 的攝影師設計。移除孤兒檔、批次把精選的 RAW 搬進 Lightroom，幾秒鐘搞定。";

export const metadata: Metadata = {
  title,
  description,
  alternates: {
    canonical: "/zh",
    languages: {
      en: "/",
      "zh-Hant": "/zh",
      "x-default": "/",
    },
  },
  openGraph: {
    type: "website",
    url: "/zh",
    siteName: "PhotoPick",
    title,
    description,
    locale: "zh_TW",
    alternateLocale: ["en_US"],
  },
  twitter: {
    card: "summary_large_image",
    title,
    description,
    creator: "@derekdylu",
  },
};

export default function HomeZh() {
  return (
    <main className="min-h-screen">
      <JsonLd lang="zh" />
      <Hero lang="zh" />
      <Features lang="zh" />
      <Screenshots lang="zh" />
      <SupportedCameras lang="zh" />
      <FAQ lang="zh" />
      <DownloadCTA lang="zh" />
      <Footer lang="zh" />
    </main>
  );
}
