import { Button } from "@/components/ui/button";

export default function LoginPage() {
  return (
    <div className="max-w-md mx-auto px-4 py-12">
      <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm space-y-6">
        <div className="text-center space-y-1">
          <h1 className="text-2xl font-bold text-slate-900">Sign in to BrandKotha</h1>
          <p className="text-sm text-slate-600">Access your Creator or Brand dashboard</p>
        </div>

        <form className="space-y-4">
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
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <Button type="button" className="w-full">
            Sign In
          </Button>
        </form>

        <p className="text-center text-xs text-slate-500">
          Don&apos;t have an account?{" "}
          <a href="/register" className="text-blue-600 font-medium hover:underline">
            Register here
          </a>
        </p>
      </div>
    </div>
  );
}
