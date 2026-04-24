import type { ReactNode } from "react";

type FAQ = {
  q: string;
  a: ReactNode;
};

const faqs: FAQ[] = [
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
  {
    q: 'macOS says PhotoPick "is damaged" or "is malware". How do I open it?',
    a: (
      <div className="space-y-3">
        <p>
          PhotoPick is ad-hoc signed and not notarised by Apple, so Gatekeeper
          blocks the first launch. The app isn&apos;t actually malicious — pick
          either fix below, you only need to do it once.
        </p>
        <p className="font-semibold text-brand-fg dark:text-white">
          Option A — Terminal (one command)
        </p>
        <pre className="overflow-x-auto rounded-lg bg-slate-900 p-4 text-sm text-slate-100">
          <code>
            sudo xattr -dr com.apple.quarantine /Applications/PhotoPick.app
          </code>
        </pre>
        <p>Then double-click PhotoPick normally.</p>
        <p className="font-semibold text-brand-fg dark:text-white">
          Option B — GUI (no Terminal)
        </p>
        <ol className="list-decimal space-y-1 pl-5">
          <li>
            Double-click PhotoPick so the warning appears, then click{" "}
            <strong>Cancel</strong> (not &ldquo;Move to Trash&rdquo;).
          </li>
          <li>
            Open <strong>System Settings → Privacy &amp; Security</strong>.
          </li>
          <li>
            Scroll to the <strong>Security</strong> section. You&apos;ll see{" "}
            <em>&ldquo;PhotoPick was blocked to protect your Mac.&rdquo;</em>
          </li>
          <li>
            Click <strong>Open Anyway</strong> and authenticate with Touch ID
            or your password.
          </li>
          <li>
            Launch PhotoPick again and confirm <strong>Open</strong> in the
            follow-up dialog.
          </li>
        </ol>
        <p className="text-sm text-slate-500 dark:text-slate-400">
          On macOS Sequoia the older &ldquo;right-click → Open&rdquo; trick no
          longer works — the dialog only offers &ldquo;Move to Trash&rdquo;, so
          use Option A or Option B.
        </p>
      </div>
    ),
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
