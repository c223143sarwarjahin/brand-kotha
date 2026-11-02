import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Star, ShieldCheck } from "lucide-react";

export default function CreatorsPage() {
  const sampleCreators = [
    {
      id: "1",
      name: "Tanzina Karim",
      handle: "@tanzina_beauty",
      niche: "Beauty & Skincare",
      platform: "INSTAGRAM",
      followers: "68K",
      rate: 10000,
      rating: 4.9,
      reviewCount: 14,
      verified: true,
    },
    {
      id: "2",
      name: "Rafid Zaman",
      handle: "@techwithrafid",
      niche: "Tech & Gadgets",
      platform: "YOUTUBE",
      followers: "125K",
      rate: 22000,
      rating: 4.8,
      reviewCount: 29,
      verified: true,
    },
    {
      id: "3",
      name: "Nabila Hossain",
      handle: "@nabilastyle",
      niche: "Fashion",
      platform: "TIKTOK",
      followers: "42K",
      rate: 8000,
      rating: 5.0,
      reviewCount: 8,
      verified: false,
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Vetted Bangladeshi Creators</h1>
          <p className="text-sm text-slate-600">Discover authentic micro and mid-tier influencers for your campaigns</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {sampleCreators.map((creator) => (
          <div
            key={creator.id}
            className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Badge variant="default">{creator.platform}</Badge>
                {creator.verified && (
                  <span className="text-xs text-blue-600 flex items-center gap-0.5 font-medium">
                    <ShieldCheck className="w-4 h-4" /> Verified
                  </span>
                )}
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 text-base">{creator.name}</h3>
                <p className="text-xs text-slate-500">{creator.handle}</p>
              </div>
              <p className="text-xs font-medium text-slate-700 bg-slate-50 px-2.5 py-1 rounded-md inline-block">
                {creator.niche}
              </p>
              <div className="flex items-center justify-between text-xs text-slate-600 pt-2 border-t border-slate-100">
                <span>{creator.followers} followers</span>
                <span className="flex items-center gap-1 font-semibold text-amber-600">
                  <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
                  {creator.rating} ({creator.reviewCount})
                </span>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <div>
                <span className="text-xs text-slate-500 block">Rate / reel</span>
                <span className="text-sm font-bold text-slate-900">৳{creator.rate.toLocaleString()}</span>
              </div>
              <Button size="sm">Invite to Brief</Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

