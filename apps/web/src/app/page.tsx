import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Sparkles, ShieldCheck, ArrowRight, DollarSign } from "lucide-react";

export default function HomePage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 md:py-16">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <Badge variant="match" className="py-1 px-3">
          <Sparkles className="w-3.5 h-3.5 mr-1 text-indigo-600 inline" />
          50/25/25 Deterministic Compatibility Matching
        </Badge>
        <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-slate-900">
          Bangladesh&apos;s Frictionless PR & Creator Marketplace
        </h1>
        <p className="text-base md:text-lg text-slate-600 max-w-2xl mx-auto">
          Connect local micro & mid-tier creators (10K–150K followers) with authentic Bangladeshi brands.
          Transparent BDT (৳) budgets, verified collaboration ratings, and zero DM ghosting.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
          <a href="/campaigns" className="w-full sm:w-auto">
            <Button size="lg" className="w-full sm:w-auto gap-2">
              Explore Active Campaigns <ArrowRight className="w-4 h-4" />
            </Button>
          </a>
          <a href="/creators" className="w-full sm:w-auto">
            <Button variant="outline" size="lg" className="w-full sm:w-auto">
              Find Vetted Creators
            </Button>
          </a>
        </div>
      </div>

      {/* Feature Value Props */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
        <div className="p-6 bg-white rounded-xl border border-slate-200 shadow-sm space-y-2">
          <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center text-blue-600">
            <DollarSign className="w-5 h-5" />
          </div>
          <h3 className="font-semibold text-slate-900 text-lg">Upfront BDT (৳) Pricing</h3>
          <p className="text-sm text-slate-600">
            Clear campaign budgets and creator deliverable rates with local bKash, SSLCommerz, and aamarPay readiness.
          </p>
        </div>

        <div className="p-6 bg-white rounded-xl border border-slate-200 shadow-sm space-y-2">
          <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center text-emerald-600">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="font-semibold text-slate-900 text-lg">Verified Mutual Reviews</h3>
          <p className="text-sm text-slate-600">
            1-to-5 star ratings strictly gated behind an accepted pitch. Build authentic reputation without fake screenshots.
          </p>
        </div>

        <div className="p-6 bg-white rounded-xl border border-slate-200 shadow-sm space-y-2">
          <div className="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center text-indigo-600">
            <Sparkles className="w-5 h-5" />
          </div>
          <h3 className="font-semibold text-slate-900 text-lg">100-Point Match Score</h3>
          <p className="text-sm text-slate-600">
            Transparent scoring calculated from 50% Niche, 25% Platform, and 25% Budget compatibility.
          </p>
        </div>
      </div>
    </div>
  );
}

