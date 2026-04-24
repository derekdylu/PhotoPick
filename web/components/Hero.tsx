import Image from "next/image";
import Link from "next/link";
import type { Locale } from "@/lib/i18n";

const dict = {
  en: {
    heading1: "RAW + JPG, paired.",
    heading2: "Orphans, gone.",
    subheading:
      "A lightweight macOS app for photographers who shoot dual-format. Clean up unpaired files and batch-move your picks into Lightroom in seconds.",
    ctaDownload: "Download for macOS",
    ctaGithub: "View on GitHub",
    small: "Free · Open source · macOS 12+ · Apple Silicon & Intel",
  },
  zh: {
    heading1: "RAW + JPG 自動配對。",
    heading2: "孤兒檔一鍵清空。",
    subheading:
      "專為同時拍攝 RAW + JPG 的攝影師設計的輕量 macOS 應用程式。清除未配對檔案、批次把選好的 RAW 丟進 Lightroom，只需要幾秒鐘。",
    ctaDownload: "下載 (macOS)",
    ctaGithub: "檢視 GitHub",
    small: "免費 · 開放原始碼 · macOS 12+ · Apple Silicon 與 Intel",
  },
} as const;

export default function Hero({ lang = "en" }: { lang?: Locale }) {
  const t = dict[lang];
  return (
    <section className="relative overflow-hidden">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10 bg-gradient-to-b from-brand-muted/70 via-white to-white dark:from-brand/10 dark:via-[#07090f] dark:to-[#07090f]"
      />
      <div className="mx-auto flex max-w-5xl flex-col items-center px-6 pb-16 pt-24 text-center sm:pt-32">
        <Image
          src="/PhotoPick.png"
          alt="PhotoPick app icon"
          width={144}
          height={144}
          priority
          className="mb-8 h-28 w-28 rounded-[28%] shadow-xl sm:h-36 sm:w-36"
        />
        <h1 className="text-balance text-4xl font-bold tracking-tight text-brand-fg dark:text-white sm:text-6xl">
          {t.heading1}
          <br />
          {t.heading2}
        </h1>
        <p className="mt-6 max-w-2xl text-pretty text-lg text-slate-600 dark:text-slate-300 sm:text-xl">
          {t.subheading}
        </p>
        <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:gap-4">
          <Link
            href="https://github.com/derekdylu/PhotoPick/releases"
            className="inline-flex items-center justify-center rounded-full bg-brand px-7 py-3 text-base font-semibold text-white shadow-lg shadow-brand/30 transition hover:bg-brand/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand hover:translate-y-[-2px]"
          >
            {t.ctaDownload}
          </Link>
          <Link
            href="https://github.com/derekdylu/PhotoPick"
            className="inline-flex items-center justify-center rounded-full border border-slate-300 px-7 py-3 text-base font-semibold text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            {t.ctaGithub}
          </Link>
        </div>
        <p className="mt-6 text-sm text-slate-500 dark:text-slate-400">
          {t.small}
        </p>
      </div>
    </section>
  );
}
