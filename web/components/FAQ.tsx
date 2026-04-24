import type { ReactNode } from "react";
import type { Locale } from "@/lib/i18n";

type FAQ = {
  q: string;
  a: ReactNode;
};

const dict: Record<Locale, { heading: string; faqs: FAQ[] }> = {
  en: {
    heading: "Frequently asked questions",
    faqs: [
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
              PhotoPick is ad-hoc signed and not notarised by Apple, so
              Gatekeeper blocks the first launch. The app isn&apos;t actually
              malicious — pick either fix below, you only need to do it once.
            </p>
            <p className="font-semibold text-brand-fg dark:text-white">
              Option A — Terminal (one command)
            </p>
            <pre className="overflow-x-auto rounded-lg bg-slate-900 p-4 text-sm text-slate-100">
              <code>
                sudo xattr -dr com.apple.quarantine
                /Applications/PhotoPick.app
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
                Scroll to the <strong>Security</strong> section. You&apos;ll
                see{" "}
                <em>
                  &ldquo;PhotoPick was blocked to protect your Mac.&rdquo;
                </em>
              </li>
              <li>
                Click <strong>Open Anyway</strong> and authenticate with Touch
                ID or your password.
              </li>
              <li>
                Launch PhotoPick again and confirm <strong>Open</strong> in the
                follow-up dialog.
              </li>
            </ol>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              On macOS Sequoia the older &ldquo;right-click → Open&rdquo; trick
              no longer works — the dialog only offers &ldquo;Move to
              Trash&rdquo;, so use Option A or Option B.
            </p>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              * Actual risks are at your own discretion.
            </p>
          </div>
        ),
      },
    ],
  },
  zh: {
    heading: "常見問題",
    faqs: [
      {
        q: "PhotoPick 是做什麼的？",
        a: "PhotoPick 是為同時拍攝 RAW + JPG 的 macOS 攝影師設計的工具。它會找出沒有配對的檔案讓你丟進垃圾桶，也能把你挑好的 JPG 拖進托盤暫存區，一次把對應的 RAW 批次搬到 Lightroom 或任何資料夾。",
      },
      {
        q: "PhotoPick 支援哪些 RAW 格式？",
        a: "Canon (.cr2, .cr3)、Nikon (.nef)、Sony (.arw)、Fuji (.raf)、Pentax (.pef)、Panasonic (.rw2)、Sigma (.x3f)、Olympus (.orf)、Adobe DNG —— 會和 .jpg / .jpeg 配對。",
      },
      {
        q: "PhotoPick 免費嗎？",
        a: "免費。PhotoPick 採 MIT 授權、開放原始碼，完整程式碼可在 GitHub 取得。",
      },
      {
        q: "PhotoPick 支援 Apple Silicon 嗎？",
        a: "支援。PhotoPick 原生支援 Apple Silicon 與 Intel Mac，需要 macOS 12 Monterey 以上。",
      },
      {
        q: "macOS 顯示 PhotoPick「已損毀」或「是惡意軟體」，要怎麼打開？",
        a: (
          <div className="space-y-3">
            <p>
              PhotoPick 目前是 ad-hoc
              簽章、沒有經過 Apple notarization，所以 Gatekeeper
              會在第一次啟動時擋下來。這**不是**因為 app 真的有惡意。下列兩種方法擇一使用，每台電腦只需要做一次。
            </p>
            <p className="font-semibold text-brand-fg dark:text-white">
              方法 A — 使用 Terminal（一行指令）
            </p>
            <pre className="overflow-x-auto rounded-lg bg-slate-900 p-4 text-sm text-slate-100">
              <code>
                sudo xattr -dr com.apple.quarantine
                /Applications/PhotoPick.app
              </code>
            </pre>
            <p>然後正常雙擊 PhotoPick 即可。</p>
            <p className="font-semibold text-brand-fg dark:text-white">
              方法 B — 使用系統設定（不用開 Terminal）
            </p>
            <ol className="list-decimal space-y-1 pl-5">
              <li>
                先雙擊 PhotoPick 讓警告視窗出現，然後點{" "}
                <strong>取消</strong>（千萬不要按「移到垃圾桶」）。
              </li>
              <li>
                打開 <strong>系統設定 → 隱私權與安全性</strong>。
              </li>
              <li>
                滑到 <strong>安全性</strong> 區塊，會看到一行{" "}
                <em>「PhotoPick 已被封鎖以保護 Mac。」</em>
              </li>
              <li>
                按右邊的 <strong>仍要打開</strong>，並用 Touch ID 或密碼驗證。
              </li>
              <li>
                再次打開 PhotoPick，在接下來的確認對話框按{" "}
                <strong>打開</strong>。
              </li>
            </ol>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              macOS Sequoia 提醒：舊版「右鍵 → 打開」的繞過法已經失效 ——
              該對話框現在只剩「移到垃圾桶」一個按鈕，請改用方法 A 或 B。
            </p>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              * 實際風險請自行評估。
            </p>
          </div>
        ),
      },
    ],
  },
};

export default function FAQ({ lang = "en" }: { lang?: Locale }) {
  const t = dict[lang];
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
        {t.heading}
      </h2>
      <dl className="mt-12 space-y-6">
        {t.faqs.map((f) => (
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
