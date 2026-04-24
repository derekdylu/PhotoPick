"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function LangToggle() {
  const pathname = usePathname() ?? "/";
  const isZh = pathname === "/zh" || pathname.startsWith("/zh/");
  const href = isZh ? "/" : "/zh";
  const label = isZh ? "EN" : "中";
  const aria = isZh ? "Switch to English" : "切換成中文";

  return (
    <Link
      href={href}
      aria-label={aria}
      title={aria}
      prefetch={false}
      className="fixed left-4 top-4 z-50 inline-flex h-10 min-w-10 items-center justify-center rounded-full border border-slate-200 bg-white/80 px-3 text-sm font-semibold text-slate-700 shadow-sm backdrop-blur transition hover:bg-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-200 dark:hover:bg-slate-900 sm:left-6 sm:top-6"
    >
      {label}
    </Link>
  );
}
