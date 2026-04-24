import Image from "next/image";

const shots = [
  {
    src: "/screenshots/orphans.jpg",
    alt: "PhotoPick — Remove Orphans view showing unpaired files ready to trash",
    caption: "Remove Orphans",
    subcaption: "Unpaired RAW or JPG files, flagged and one click from the trash.",
  },
  {
    src: "/screenshots/inbox.jpg",
    alt: "PhotoPick — Inbox Tray view with JPG picks ready to move",
    caption: "Inbox Tray",
    subcaption: "Drop your keepers in. Move their RAWs into Lightroom or any folder.",
  },
];

export default function Screenshots() {
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
        See it in motion.
      </h2>
      <div className="mt-14 grid gap-10 md:grid-cols-2">
        {shots.map((s) => (
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
