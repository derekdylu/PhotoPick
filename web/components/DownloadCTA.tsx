import Link from "next/link";
import type { Locale } from "@/lib/i18n";

const dict = {
  en: {
    heading: "Ready to clean up your catalog?",
    subheading:
      "PhotoPick is free and open source. Grab the latest build or build it yourself from source.",
    ctaPrimary: "Download latest release",
    ctaSecondary: "Build from source",
    small: "macOS 12 Monterey or later · Apple Silicon & Intel",
  },
  zh: {
    heading: "準備整理你的照片庫了嗎？",
    subheading:
      "PhotoPick 免費且開放原始碼。",
    ctaPrimary: "下載最新版本",
    ctaSecondary: "檢視 GitHub",
    small: "macOS 12 Monterey 以上 · Apple Silicon & Intel",
  },
} as const;

export default function DownloadCTA({ lang = "en" }: { lang?: Locale }) {
  const t = dict[lang];
  return (
    <section id="download" className="px-6 py-20">
      <div className="mx-auto max-w-4xl overflow-hidden rounded-3xl bg-brand-fg px-8 py-16 text-center shadow-xl sm:px-16">
        <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
          {t.heading}
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-pretty text-lg text-white/80">
          {t.subheading}
        </p>
        <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:justify-center sm:gap-4">
          <Link
            href="https://github.com/derekdylu/PhotoPick/releases"
            className="inline-flex items-center justify-center rounded-full bg-white px-7 py-3 text-base font-semibold text-brand-fg shadow-lg transition hover:bg-slate-100"
          >
            {t.ctaPrimary}
          </Link>
          <Link
            href="https://github.com/derekdylu/PhotoPick#readme"
            className="inline-flex items-center justify-center rounded-full border border-white/30 px-7 py-3 text-base font-semibold text-white transition hover:bg-white/10"
          >
            {t.ctaSecondary}
          </Link>
        </div>
        <p className="mt-6 text-sm text-white/60">{t.small}</p>
      </div>
    </section>
  );
}
