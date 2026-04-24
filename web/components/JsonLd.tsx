import type { Locale } from "@/lib/i18n";

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://photopick.vercel.app";

const person = {
  "@type": "Person",
  "@id": "https://derekdylu.com#person",
  name: "Derek Lu",
  url: "https://derekdylu.com",
};

const softwareApplication = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": `${siteUrl}#software`,
  name: "PhotoPick",
  applicationCategory: "PhotographyApplication",
  operatingSystem: "macOS 12 or later",
  description:
    "A lightweight macOS app for photographers who shoot RAW + JPG. Remove orphans and batch-move picks into Lightroom.",
  url: siteUrl,
  image: `${siteUrl}/icon-512.png`,
  downloadUrl: "https://github.com/derekdylu/PhotoPick/releases",
  softwareVersion: "0.2.0",
  license: "https://opensource.org/licenses/MIT",
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "USD",
  },
  author: person,
  publisher: person,
  featureList: [
    "Detect and remove orphaned RAW or JPG files",
    "Drag-and-drop Inbox Tray for JPG picks",
    "Batch move matched RAW files into Lightroom or any folder",
    "Supports Canon, Nikon, Sony, Fuji, Pentax, Panasonic, Sigma, Olympus, Adobe DNG",
  ],
};

const websiteByLocale: Record<Locale, object> = {
  en: {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": `${siteUrl}#website`,
    url: siteUrl,
    name: "PhotoPick",
    description:
      "Free macOS app for photographers shooting RAW + JPG. Remove orphaned files and batch-move your picks into Lightroom.",
    inLanguage: "en",
    publisher: person,
  },
  zh: {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": `${siteUrl}/zh#website`,
    url: `${siteUrl}/zh`,
    name: "PhotoPick",
    description:
      "為 RAW + JPG 雙格式拍攝者設計的免費 macOS 應用程式。移除孤兒檔並批次搬運精選 RAW 到 Lightroom。",
    inLanguage: "zh-Hant",
    publisher: person,
  },
};

const faqByLocale: Record<Locale, object> = {
  en: {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: [
      {
        "@type": "Question",
        name: "What does PhotoPick do?",
        acceptedAnswer: {
          "@type": "Answer",
          text: "PhotoPick helps macOS photographers who shoot dual-format (RAW + JPG). It finds unpaired files so you can trash them, and lets you drag JPG keepers into an Inbox Tray to batch-move their matching RAW files into Lightroom or any folder.",
        },
      },
      {
        "@type": "Question",
        name: "Which RAW formats does PhotoPick support?",
        acceptedAnswer: {
          "@type": "Answer",
          text: "Canon (.cr2, .cr3), Nikon (.nef), Sony (.arw), Fuji (.raf), Pentax (.pef), Panasonic (.rw2), Sigma (.x3f), Olympus (.orf), and Adobe DNG (.dng). Paired against .jpg / .jpeg.",
        },
      },
      {
        "@type": "Question",
        name: "Is PhotoPick free?",
        acceptedAnswer: {
          "@type": "Answer",
          text: "Yes. PhotoPick is free and open source under the MIT license. Source code is available on GitHub.",
        },
      },
      {
        "@type": "Question",
        name: "Does PhotoPick run on Apple Silicon?",
        acceptedAnswer: {
          "@type": "Answer",
          text: "Yes. PhotoPick runs natively on both Apple Silicon and Intel Macs. macOS 12 Monterey or later is required.",
        },
      },
      {
        "@type": "Question",
        name: 'macOS says PhotoPick "is damaged" or "is malware". How do I open it?',
        acceptedAnswer: {
          "@type": "Answer",
          text: 'PhotoPick is ad-hoc signed and not notarised by Apple, so Gatekeeper blocks the first launch. Option A (Terminal): run "sudo xattr -dr com.apple.quarantine /Applications/PhotoPick.app" then double-click the app. Option B (GUI): after the warning appears, click Cancel, open System Settings → Privacy & Security, scroll to the Security section, click "Open Anyway" next to the PhotoPick notice, authenticate, then launch the app and confirm Open. On macOS Sequoia the old "right-click → Open" trick no longer works.',
        },
      },
    ],
  },
  zh: {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: [
      {
        "@type": "Question",
        name: "PhotoPick 是做什麼的？",
        acceptedAnswer: {
          "@type": "Answer",
          text: "PhotoPick 是為同時拍攝 RAW + JPG 的 macOS 攝影師設計的工具。它會找出沒有配對的檔案讓你丟進垃圾桶，也能把你挑好的 JPG 拖進收件匣托盤，一次把對應的 RAW 批次搬到 Lightroom 或任何資料夾。",
        },
      },
      {
        "@type": "Question",
        name: "PhotoPick 支援哪些 RAW 格式？",
        acceptedAnswer: {
          "@type": "Answer",
          text: "Canon (.cr2, .cr3)、Nikon (.nef)、Sony (.arw)、Fuji (.raf)、Pentax (.pef)、Panasonic (.rw2)、Sigma (.x3f)、Olympus (.orf)、Adobe DNG (.dng)。與 .jpg / .jpeg 配對。",
        },
      },
      {
        "@type": "Question",
        name: "PhotoPick 免費嗎？",
        acceptedAnswer: {
          "@type": "Answer",
          text: "免費。PhotoPick 採 MIT 授權、開放原始碼，完整程式碼可在 GitHub 取得。",
        },
      },
      {
        "@type": "Question",
        name: "PhotoPick 支援 Apple Silicon 嗎？",
        acceptedAnswer: {
          "@type": "Answer",
          text: "支援。PhotoPick 原生支援 Apple Silicon 與 Intel Mac，需要 macOS 12 Monterey 以上。",
        },
      },
      {
        "@type": "Question",
        name: "macOS 顯示 PhotoPick「已損毀」或「是惡意軟體」，要怎麼打開？",
        acceptedAnswer: {
          "@type": "Answer",
          text: "PhotoPick 是 ad-hoc 簽章、沒有經過 Apple notarization，所以 Gatekeeper 會擋下第一次啟動。方法 A（Terminal）：執行 sudo xattr -dr com.apple.quarantine /Applications/PhotoPick.app，然後正常雙擊打開。方法 B（GUI）：先雙擊 PhotoPick 讓警告出現並按取消，打開系統設定 → 隱私權與安全性，滑到安全性區塊按 PhotoPick 旁的「仍要打開」，驗證後再次啟動並在對話框按「打開」。macOS Sequoia 上舊版「右鍵 → 打開」的繞過法已失效。",
        },
      },
    ],
  },
};

export default function JsonLd({ lang = "en" }: { lang?: Locale }) {
  const graph = {
    "@context": "https://schema.org",
    "@graph": [softwareApplication, websiteByLocale[lang], faqByLocale[lang]],
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(graph) }}
    />
  );
}
