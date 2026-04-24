"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

export default function HtmlLangSetter() {
  const pathname = usePathname() ?? "/";

  useEffect(() => {
    const isZh = pathname === "/zh" || pathname.startsWith("/zh/");
    document.documentElement.lang = isZh ? "zh-Hant" : "en";
  }, [pathname]);

  return null;
}
