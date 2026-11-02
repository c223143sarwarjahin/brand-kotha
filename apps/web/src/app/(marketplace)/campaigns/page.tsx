import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Sparkles, Calendar, Tag } from "lucide-react";

export default function CampaignsPage() {
  const sampleCampaigns = [
    {
      id: "1",
      title: "Eid Special PR Package & Reels Promotion",
      brand: "Aura Skincare BD",
      category: "Beauty",
      platform: "INSTAGRAM",
      budget: 15000,
      matchScore: 95,
      type: "PAID_PROMO",
    },
    {
      id: "2",
      title: "Winter Fusion Streetwear Review Series",
      brand: "Urban Threadz Dhaka",
      category: "Fashion",
      platform: "TIKTOK",
      budget: 12000,
      matchScore: 82,
      type: "PAID_PROMO",
    },
    {
      id: "3",
      title: "Tech Gadget Unboxing & Long-term Impressions",
      brand: "ByteCraft Bangladesh",
      category: "Tech",
      platform: "YOUTUBE",
      budget: 25000,
      matchScore: 78,
      type: "PAID_PROMO",
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Active Brand Campaigns</h1>
          <p className="text-sm text-slate-600">Browse verified campaigns tailored to your creator profile</p>
        </div>
        <div className="flex gap-2">
          <select className="px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none">
            <option>All Niches</option>
            <option>Beauty</option>
            <option>Fashion</option>
            <option>Food</option>
            <option>Tech</option>
          </select>
          <select className="px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none">
            <option>All Platforms</option>
            <option>Instagram</option>
            <option>Facebook</option>
            <option>YouTube</option>
            <option>TikTok</option>
          </select>
        </div>
      </div>

      <div className="space-y-4">
        {sampleCampaigns.map((camp) => (
          <div
            key={camp.id}
            className="p-5 bg-white rounded-xl border border-slate-200 shadow-sm hover:border-slate-300 transition flex flex-col sm:flex-row sm:items-center justify-between gap-4"
          >
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="match">
                  <Sparkles className="w-3 h-3 mr-1 inline" />
                  {camp.matchScore}% Match
                </Badge>
                <Badge variant="default">{camp.platform}</Badge>
                <span className="text-xs text-slate-500 flex items-center gap-1">
                  <Tag className="w-3 h-3" /> {camp.category}
                </span>
              </div>
              <h2 className="text-lg font-semibold text-slate-900">{camp.title}</h2>
              <p className="text-xs text-slate-500">Posted by {camp.brand}</p>
            </div>

            <div className="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center border-t sm:border-t-0 pt-3 sm:pt-0">
              <div className="text-lg font-bold text-slate-900">৳{camp.budget.toLocaleString()}</div>
              <Button size="sm" className="mt-2">
                Submit Pitch
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

