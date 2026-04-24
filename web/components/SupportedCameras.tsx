import type { Locale } from "@/lib/i18n";

const brands = [
  `.cr2`, `.cr3`, `.nef`, `.arw`, `.dng`, `.orf`, `.rw2`, `.pef`, `.srw`, `.x3f`,
];

const dict = {
  en: { heading: "Supported RAW formats" },
  zh: { heading: "支援的 RAW 格式" },
} as const;

export default function SupportedCameras({ lang = "en" }: { lang?: Locale }) {
  const t = dict[lang];
  return (
    <section
      aria-labelledby="cameras-heading"
      className="mx-auto max-w-5xl px-6 py-20"
    >
      <h2
        id="cameras-heading"
        className="text-center text-sm font-semibold uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400"
      >
        {t.heading}
      </h2>
      <div className="mt-8 flex flex-wrap justify-center gap-3">
        {brands.map((brand) => (
          <span
            key={brand}
            className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm dark:border-slate-800 dark:bg-slate-900/60 dark:text-slate-200"
          >
            {brand}
          </span>
        ))}
      </div>
    </section>
  );
}
