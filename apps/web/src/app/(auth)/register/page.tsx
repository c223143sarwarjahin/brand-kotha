import { Button } from "@/components/ui/button";

export default function RegisterPage() {
  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm space-y-6">
        <div className="text-center space-y-1">
          <h1 className="text-2xl font-bold text-slate-900">Create Account</h1>
          <p className="text-sm text-slate-600">Join BrandKotha as a Creator or Brand</p>
        </div>

        <form className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
              Select Your Role
            </label>
            <div className="grid grid-cols-2 gap-2">
              <label className="flex items-center justify-center p-3 border border-slate-300 rounded-lg cursor-pointer hover:border-blue-500 has-[:checked]:border-blue-600 has-[:checked]:bg-blue-50">
                <input type="radio" name="role" value="CREATOR" defaultChecked className="sr-only" />
                <span className="text-sm font-semibold text-slate-800">Creator</span>
              </label>
              <label className="flex items-center justify-center p-3 border border-slate-300 rounded-lg cursor-pointer hover:border-blue-500 has-[:checked]:border-blue-600 has-[:checked]:bg-blue-50">
                <input type="radio" name="role" value="BRAND" className="sr-only" />
                <span className="text-sm font-semibold text-slate-800">Brand</span>
              </label>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
              Full Name or Brand Name
            </label>
            <input
              type="text"
              placeholder="e.g. Shovon Ahmed / Glow Skin BD"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
              Email Address
            </label>
            <input
              type="email"
              placeholder="you@domain.com"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">
              Password (min. 8 characters)
            </label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <Button type="button" className="w-full">
            Complete Registration
          </Button>
        </form>

        <p className="text-center text-xs text-slate-500">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600 font-medium hover:underline">
            Sign in
          </a>
        </p>
      </div>
    </div>
  );
}

