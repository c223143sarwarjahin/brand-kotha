import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BrandKotha — Creator & Brand Freelancing Marketplace",
  description:
    "Bangladesh's dedicated two-sided marketplace connecting content creators with authentic local brands.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5" />
      </head>
      <body className="bg-slate-50 text-slate-900 antialiased font-sans">
        <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                BrandKotha
              </span>
              <span className="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded-full">
                🇧🇩 BD
              </span>
            </div>
            <nav className="flex items-center gap-4 text-sm font-medium">
              <a href="/campaigns" className="text-slate-600 hover:text-blue-600 transition">
                Campaigns
              </a>
              <a href="/creators" className="text-slate-600 hover:text-blue-600 transition">
                Creators
              </a>
              <a href="/admin" className="text-slate-500 hover:text-slate-900 text-xs px-2 py-1 bg-slate-100 rounded">
                Admin
              </a>
            </nav>
          </div>
        </header>

        <main className="min-h-[calc(100vh-4rem)]">
          {children}
        </main>

        <footer className="bg-white border-t border-slate-200 py-6 text-center text-xs text-slate-500">
          <p>© 2026 BrandKotha (Team A: Kalpona Koly, Mahir Tajuar Akash, Rawfun Shovon, Sarwar Jahin). All rights reserved.</p>
        </footer>
      </body>
    </html>
  );
}
