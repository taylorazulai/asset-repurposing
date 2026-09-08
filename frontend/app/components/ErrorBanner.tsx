"use client";

import { PipelineError } from "@/lib/api";

interface ErrorBannerProps {
  error: PipelineError | Error | string;
}

export function ErrorBanner({ error }: ErrorBannerProps) {
  const message = typeof error === "string" ? error : error.message;

  if (error instanceof PipelineError) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="font-semibold text-red-800">
          {error.status ? `Error ${error.status}` : "Something went wrong"}
        </h3>
        <p className="text-red-700 mt-1">{message}</p>
        {error.kind === "all_generators_failed" && error.errors && (
          <div className="mt-3 text-sm">
            <p className="font-medium text-red-800">Per-asset errors:</p>
            <ul className="list-disc list-inside mt-1 text-red-700">
              {Object.entries(error.errors).map(([key, value]) => (
                <li key={key}>
                  {key}: {value}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
      <h3 className="font-semibold text-red-800">Something went wrong</h3>
      <p className="text-red-700 mt-1">{message}</p>
    </div>
  );
}
