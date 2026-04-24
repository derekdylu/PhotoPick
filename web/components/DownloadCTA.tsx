import Link from "next/link";

export default function DownloadCTA() {
  return (
    <section id="download" className="px-6 py-20">
      <div className="mx-auto max-w-4xl overflow-hidden rounded-3xl bg-brand-fg px-8 py-16 text-center shadow-xl sm:px-16">
        <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
          Ready to clean up your catalog?
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-pretty text-lg text-white/80">
          PhotoPick is free and open source. Grab the latest build or build it
          yourself from source.
        </p>
        <div className="mt-10 flex flex-col items-center gap-3 sm:flex-row sm:justify-center sm:gap-4">
          <Link
            href="https://github.com/derekdylu/PhotoPick/releases"
            className="inline-flex items-center justify-center rounded-full bg-white px-7 py-3 text-base font-semibold text-brand-fg shadow-lg transition hover:bg-slate-100"
          >
            Download latest release
          </Link>
          <Link
            href="https://github.com/derekdylu/PhotoPick#readme"
            className="inline-flex items-center justify-center rounded-full border border-white/30 px-7 py-3 text-base font-semibold text-white transition hover:bg-white/10"
          >
            Build from source
          </Link>
        </div>
        <p className="mt-6 text-sm text-white/60">
          macOS 12 Monterey or later &middot; Apple Silicon &amp; Intel
        </p>
      </div>
    </section>
  );
}
