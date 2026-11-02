export * from "./types";

export interface ApiClientConfig {
  baseUrl: string;
  getAuthToken?: () => string | null;
}

export class BrandKothaClient {
  private baseUrl: string;
  private getAuthToken?: () => string | null;

  constructor(config: ApiClientConfig) {
    this.baseUrl = config.baseUrl.replace(/\/$/, "");
    this.getAuthToken = config.getAuthToken;
  }

  private async fetchWithAuth(endpoint: string, options: RequestInit = {}): Promise<Response> {
    const url = `${this.baseUrl}${endpoint.startsWith("/") ? endpoint : `/${endpoint}`}`;
    const headers = new Headers(options.headers || {});
    headers.set("Content-Type", "application/json");

    if (this.getAuthToken) {
      const token = this.getAuthToken();
      if (token) {
        headers.set("Authorization", `Bearer ${token}`);
      }
    }

    return fetch(url, {
      ...options,
      headers,
    });
  }

  async checkHealth(): Promise<{ status: string; service: string }> {
    const res = await this.fetchWithAuth("/health/live");
    if (!res.ok) throw new Error("Health check failed");
    return res.json();
  }
}

