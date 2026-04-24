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

const website = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": `${siteUrl}#website`,
  url: siteUrl,
  name: "PhotoPick",
  description:
    "Free macOS app for photographers shooting RAW + JPG. Remove orphaned files and batch-move your picks into Lightroom.",
  inLanguage: "en",
  publisher: person,
};

const faq = {
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
};

export default function JsonLd() {
  const graph = {
    "@context": "https://schema.org",
    "@graph": [softwareApplication, website, faq],
  };
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(graph) }}
    />
  );
}
