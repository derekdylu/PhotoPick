import Hero from "@/components/Hero";
import Features from "@/components/Features";
import Screenshots from "@/components/Screenshots";
import SupportedCameras from "@/components/SupportedCameras";
import FAQ from "@/components/FAQ";
import DownloadCTA from "@/components/DownloadCTA";
import Footer from "@/components/Footer";
import JsonLd from "@/components/JsonLd";

export default function Home() {
  return (
    <main className="min-h-screen">
      <JsonLd lang="en" />
      <Hero lang="en" />
      <Features lang="en" />
      <Screenshots lang="en" />
      <SupportedCameras lang="en" />
      <FAQ lang="en" />
      <DownloadCTA lang="en" />
      <Footer lang="en" />
    </main>
  );
}
