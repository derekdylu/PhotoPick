export default function JsonLd() {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://photopick.vercel.app";

  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "PhotoPick",
    applicationCategory: "PhotographyApplication",
    operatingSystem: "macOS",
    description:
      "A lightweight macOS app for photographers who shoot RAW + JPG. Remove orphans and batch-move picks into Lightroom.",
    url: siteUrl,
    image: `${siteUrl}/PhotoPick.png`,
    downloadUrl: "https://github.com/derekdylu/PhotoPick/releases",
    softwareVersion: "0.2.0",
    license: "https://opensource.org/licenses/MIT",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
    author: {
      "@type": "Person",
      name: "Derek Lu",
      url: "https://derekdylu.com",
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
