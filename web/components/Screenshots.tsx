import Image from "next/image";
import type { Locale } from "@/lib/i18n";

const dict = {
  en: {
    heading: "See it in motion.",
    shots: [
      {
        src: "/screenshots/orphans.jpg",
        alt: "PhotoPick — Remove Orphans view showing unpaired files ready to trash",
        caption: "Remove Orphans",
        subcaption:
          "Unpaired RAW or JPG files, flagged and one click from the trash.",
      },
      {
        src: "/screenshots/inbox.jpg",
        alt: "PhotoPick — Inbox Tray view with JPG picks ready to move",
        caption: "Inbox Tray",
        subcaption:
          "Drop your keepers in. Move their RAWs into Lightroom or any folder.",
      },
    ],
  },
  zh: {
    heading: "實際畫面。",
    shots: [
      {
        src: "/screenshots/orphans.jpg",
        alt: "PhotoPick — 移除孤兒檔畫面，列出準備丟垃圾桶的未配對檔案",
        caption: "移除孤兒檔",
        subcaption: "未配對的 RAW 或 JPG 檔案會被標記，一鍵丟進垃圾桶。",
      },
      {
        src: "/screenshots/inbox.jpg",
        alt: "PhotoPick — 收件匣托盤畫面，擺放準備搬運的 JPG 精選",
        caption: "收件匣托盤",
        subcaption: "把你要的 JPG 丟進來，它們的 RAW 會跟著進 Lightroom 或任何資料夾。",
      },
    ],
  },
} as const;

export default function Screenshots({ lang = "en" }: { lang?: Locale }) {
  const t = dict[lang];
  return (
    <section
      id="screenshots"
      aria-labelledby="screenshots-heading"
      className="mx-auto max-w-6xl px-6 py-20"
    >
      <h2
        id="screenshots-heading"
        className="text-center text-3xl font-bold tracking-tight text-brand-fg dark:text-white sm:text-4xl"
      >
        {t.heading}
      </h2>
      <div className="mt-14 grid gap-10 md:grid-cols-2">
        {t.shots.map((s) => (
          <figure key={s.src} className="flex flex-col">
            <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-slate-50 shadow-md dark:border-slate-800 dark:bg-slate-900">
              <Image
                src={s.src}
                alt={s.alt}
                width={1440}
                height={900}
                className="h-auto w-full"
                sizes="(min-width: 768px) 50vw, 100vw"
              />
            </div>
            <figcaption className="mt-5">
              <div className="text-lg font-semibold text-brand-fg dark:text-white">
                {s.caption}
              </div>
              <div className="mt-1 text-sm text-slate-600 dark:text-slate-400">
                {s.subcaption}
              </div>
            </figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
}
