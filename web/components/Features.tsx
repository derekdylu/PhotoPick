const features = [
  {
    title: "Remove Orphans",
    description:
      "Scan any folder and safely trash RAW or JPG files that have lost their pair — so your catalog stays consistent and clean.",
    icon: (
      <svg
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
      </svg>
    ),
  },
  {
    title: "Inbox Tray",
    description:
      "Drag the JPG keepers you like into the tray, then move their matched RAWs into Lightroom or any folder — all in one click.",
    icon: (
      <svg
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
      </svg>
    ),
  },
];

export default function Features() {
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
        Two tools. One clean workflow.
      </h2>
      <p className="mx-auto mt-4 max-w-2xl text-center text-lg text-slate-600 dark:text-slate-300">
        PhotoPick stays out of your way until you need it.
      </p>
      <div className="mt-14 grid gap-8 sm:grid-cols-2">
        {features.map((f) => (
          <div
            key={f.title}
            className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm transition hover:shadow-md dark:border-slate-800 dark:bg-slate-900/50"
          >
            <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-brand-muted text-brand dark:bg-brand/15">
              {f.icon}
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
