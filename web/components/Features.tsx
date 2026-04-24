import type { Locale } from "@/lib/i18n";

const dict = {
  en: {
    heading: "Two tools. One clean workflow.",
    subheading: "PhotoPick speeds up your photo cleanup process.",
    items: [
      {
        title: "Remove Orphans",
        description:
          "Scan any folder and safely trash RAW or JPG files that have lost their pair — so your catalog stays consistent and clean.",
      },
      {
        title: "Inbox Tray",
        description:
          "Drag the JPG keepers you like into the tray, then move their matched RAWs into Lightroom or any folder — all in one click.",
      },
    ],
  },
  zh: {
    heading: "兩個工具，一套乾淨流程。",
    subheading: "PhotoPick 加速你的照片整理流程。",
    items: [
      {
        title: "移除孤兒檔",
        description:
          "掃描任何資料夾，安全地把失去配對的 RAW 或 JPG 丟進垃圾桶，讓你的照片庫保持一致、乾淨。",
      },
      {
        title: "托盤暫存區",
        description:
          "把你喜歡的 JPG 拖進托盤暫存區，一鍵把對應的 RAW 搬進 Lightroom 或任何資料夾。",
      },
    ],
  },
} as const;

const icons = [
  <svg
    key="orphans"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="h-6 w-6"
  >
    <path d="M3 6h18" />
    <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
    <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
    <path d="M10 11v6" />
    <path d="M14 11v6" />
  </svg>,
  <svg
    key="inbox"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.8"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="h-6 w-6"
  >
    <path d="M3 13h4l2 3h6l2-3h4" />
    <path d="M5 13l2-7h10l2 7" />
    <path d="M3 13v6a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-6" />
  </svg>,
];

export default function Features({ lang = "en" }: { lang?: Locale }) {
  const t = dict[lang];
  return (
    <section
      id="features"
      aria-labelledby="features-heading"
      className="mx-auto max-w-5xl px-6 py-20"
    >
      <h2
        id="features-heading"
        className="text-center text-3xl font-bold tracking-tight text-brand-fg dark:text-white sm:text-4xl"
      >
        {t.heading}
      </h2>
      <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-slate-600 dark:text-slate-300">
        {t.subheading}
      </p>
      <div className="mt-14 grid gap-8 sm:grid-cols-2">
        {t.items.map((f, i) => (
          <div
            key={f.title}
            className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900/50"
          >
            <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-muted text-brand dark:bg-brand/15">
              {icons[i]}
            </div>
            <h3 className="mt-5 text-xl font-semibold text-brand-fg dark:text-white">
              {f.title}
            </h3>
            <p className="mt-3 text-slate-600 dark:text-slate-300">
              {f.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
