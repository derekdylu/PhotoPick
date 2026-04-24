const faqs = [
  {
    q: "What does PhotoPick do?",
    a: "PhotoPick helps macOS photographers who shoot dual-format (RAW + JPG). It finds unpaired files so you can trash them, and lets you drag JPG keepers into an Inbox Tray to batch-move their matching RAW files into Lightroom or any folder.",
  },
  {
    q: "Which RAW formats does PhotoPick support?",
    a: "Canon (.cr2, .cr3), Nikon (.nef), Sony (.arw), Fuji (.raf), Pentax (.pef), Panasonic (.rw2), Sigma (.x3f), Olympus (.orf), and Adobe DNG — paired against .jpg / .jpeg.",
  },
  {
    q: "Is PhotoPick free?",
    a: "Yes. PhotoPick is free and open source under the MIT license. Source code is available on GitHub.",
  },
  {
    q: "Does PhotoPick run on Apple Silicon?",
    a: "Yes. PhotoPick runs natively on both Apple Silicon and Intel Macs. macOS 12 Monterey or later is required.",
  },
];

export default function FAQ() {
  return (
    <section
      id="faq"
      aria-labelledby="faq-heading"
      className="mx-auto max-w-3xl px-6 py-20"
    >
      <h2
        id="faq-heading"
        className="text-center text-3xl font-bold tracking-tight text-brand-fg dark:text-white sm:text-4xl"
      >
        Frequently asked questions
      </h2>
      <dl className="mt-12 space-y-6">
        {faqs.map((f) => (
          <div
            key={f.q}
            className="rounded-2xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900/50"
          >
            <dt className="text-lg font-semibold text-brand-fg dark:text-white">
              {f.q}
            </dt>
            <dd className="mt-2 text-slate-600 dark:text-slate-300">{f.a}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
