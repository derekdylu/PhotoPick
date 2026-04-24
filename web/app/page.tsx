import Hero from "@/components/Hero";
import Features from "@/components/Features";
import Screenshots from "@/components/Screenshots";
import SupportedCameras from "@/components/SupportedCameras";
import FAQ from "@/components/FAQ";
import DownloadCTA from "@/components/DownloadCTA";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Features />
      <Screenshots />
      <SupportedCameras />
      <FAQ />
      <DownloadCTA />
      <Footer />
    </main>
  );
}
