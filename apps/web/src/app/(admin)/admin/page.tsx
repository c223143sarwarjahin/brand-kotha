import { DollarSign, Users, Megaphone, ToggleLeft } from "lucide-react";

export default function AdminDashboardPage() {
  return (
    <div className="space-y-8">
      {/* Platform Switch Banner */}
      <div className="p-6 bg-slate-800/80 rounded-xl border border-slate-700 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider block">
            Monetization Governance
          </span>
          <h2 className="text-xl font-bold text-white mt-1">Platform Charge Switch: <span className="text-emerald-400">FREE_TRIAL (charge_enabled = False)</span></h2>
          <p className="text-xs text-slate-400 mt-1">
            Running 100% free during closed &amp; open trials to bootstrap liquidity in Dhaka &amp; Chattogram.
          </p>
        </div>
        <button className="px-4 py-2 bg-slate-700 hover:bg-slate-600 border border-slate-600 rounded-lg text-xs font-semibold text-white transition flex items-center gap-2">
          <ToggleLeft className="w-4 h-4 text-slate-400" /> Toggle Production Paywall
        </button>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="p-5 bg-slate-800/50 rounded-xl border border-slate-700/80 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs uppercase font-medium">Active Creators</span>
            <Users className="w-4 h-4" />
          </div>
          <div className="text-2xl font-bold text-white">54</div>
          <span className="text-xs text-emerald-400">+12 this week (Pre-onboarding)</span>
        </div>

        <div className="p-5 bg-slate-800/50 rounded-xl border border-slate-700/80 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs uppercase font-medium">Published Campaigns</span>
            <Megaphone className="w-4 h-4" />
          </div>
          <div className="text-2xl font-bold text-white">18</div>
          <span className="text-xs text-slate-400">Dhaka Beauty &amp; Fashion</span>
        </div>

        <div className="p-5 bg-slate-800/50 rounded-xl border border-slate-700/80 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs uppercase font-medium">Transactions Settled</span>
            <DollarSign className="w-4 h-4" />
          </div>
          <div className="text-2xl font-bold text-white">৳ 0.00</div>
          <span className="text-xs text-slate-400">0% Commission during trial</span>
        </div>
      </div>
    </div>
  );
}
