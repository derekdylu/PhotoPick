import Link from "next/link";
import type { Locale } from "@/lib/i18n";

const dict = {
  en: {
    builtByPrefix: "Built by",
    builtBySuffix: "",
    github: "GitHub",
    license: "MIT License",
  },
  zh: {
    builtByPrefix: "Built by",
    builtBySuffix: "",
    github: "GitHub",
    license: "MIT License",
  },
} as const;

export default function Footer({ lang = "en" }: { lang?: Locale }) {
  const t = dict[lang];
  return (
    <footer className="border-t border-slate-200 px-6 py-10 dark:border-slate-800">
      <div className="mx-auto flex max-w-5xl flex-col items-center justify-between gap-4 text-sm text-slate-600 dark:text-slate-400 sm:flex-row">
        <p>
          {t.builtByPrefix}{" "}
          <Link
            href="https://derekdylu.com"
            className="font-medium text-brand-fg underline-offset-4 hover:underline dark:text-white"
            rel="author"
          >
            Derek Lu
          </Link>
          {t.builtBySuffix}. &copy; {new Date().getFullYear()}
        </p>
        <div className="flex items-center gap-5">
          <Link
            href="https://github.com/derekdylu/PhotoPick"
            className="hover:text-brand-fg dark:hover:text-white"
          >
            {t.github}
          </Link>
          <Link
            href="https://github.com/derekdylu/PhotoPick/blob/main/LICENSE"
            className="hover:text-brand-fg dark:hover:text-white"
          >
            {t.license}
          </Link>
          <Link
            href="https://derekdylu.com"
            className="hover:text-brand-fg dark:hover:text-white"
          >
            derekdylu.com
          </Link>
        </div>
      </div>
    </footer>
  );
}
