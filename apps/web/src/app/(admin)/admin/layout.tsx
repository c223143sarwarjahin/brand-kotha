import { Shield } from "lucide-react";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="bg-slate-900 text-slate-100 min-h-screen">
      <div className="border-b border-slate-800 bg-slate-950 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-600/20 text-blue-400 rounded-lg">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <span className="font-bold text-white text-base">BrandKotha Administration</span>
            <span className="block text-xs text-slate-400">Owner Screen &amp; Platform Controls</span>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className="px-2.5 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 font-mono">
            ROLE_ADMIN
          </span>
          <a href="/" className="text-slate-400 hover:text-white transition">
            Exit to Marketplace &rarr;
          </a>
        </div>
      </div>
      <div className="max-w-6xl mx-auto px-6 py-8">
        {children}
      </div>
    </div>
  );
}
