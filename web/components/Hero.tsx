import Image from "next/image";
import Link from "next/link";

export default function Hero() {
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
          RAW + JPG, paired.
          <br />
          Orphans, gone.
        </h1>
        <p className="mt-6 max-w-2xl text-pretty text-lg text-slate-600 dark:text-slate-300 sm:text-xl">
          A lightweight macOS app for photographers who shoot dual-format.
          Clean up unpaired files and batch-move your picks into Lightroom in
          seconds.
        </p>
        <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:gap-4">
          <Link
            href="https://github.com/derekdylu/PhotoPick/releases"
            className="inline-flex items-center justify-center rounded-full bg-brand px-7 py-3 text-base font-semibold text-white shadow-lg shadow-brand/30 transition hover:bg-brand/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand hover:translate-y-[-2px]"
          >
            Download for macOS
          </Link>
          <Link
            href="https://github.com/derekdylu/PhotoPick"
            className="inline-flex items-center justify-center rounded-full border border-slate-300 px-7 py-3 text-base font-semibold text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            View on GitHub
          </Link>
        </div>
        <p className="mt-6 text-sm text-slate-500 dark:text-slate-400">
          Free &middot; Open source &middot; macOS 12+ &middot; Apple Silicon &amp; Intel
        </p>
      </div>
    </section>
  );
}
