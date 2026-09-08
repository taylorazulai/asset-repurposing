"use client";

import { useState } from "react";
import { UploadForm } from "./components/UploadForm";
import { OutputCards } from "./components/OutputCards";
import { ErrorBanner } from "./components/ErrorBanner";
import { PipelineOutput } from "@/lib/types";
import { pipelineRequest, PipelineError } from "@/lib/api";

export default function HomePage() {
  const [result, setResult] = useState<PipelineOutput | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<PipelineError | Error | null>(null);

  const handleSubmit = async (text: string) => {
    setLoading(true);
    setError(null);

    try {
      const data = await pipelineRequest(text);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Asset Repurposing Pipeline
        </h1>
        <p className="text-gray-600 mt-2">
          Paste a source document and generate executive briefs, social snippets, and slide decks.
        </p>
      </header>

      <UploadForm onSubmit={handleSubmit} loading={loading} />

      {loading && (
        <div className="mt-6 flex items-center space-x-2 text-gray-600">
          <div className="animate-spin h-5 w-5 border-2 border-blue-600 border-t-transparent rounded-full" />
          <span>
            {result ? "Regenerating assets..." : "Analyzing and generating assets..."}
          </span>
        </div>
      )}

      {error && (
        <div className="mt-6">
          <ErrorBanner error={error} />
        </div>
      )}

      {result && (
        <div className="mt-8">
          {result.core_context.truncated && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800">
              Source text was truncated before analysis. Consider splitting very
              long documents for best results.
            </div>
          )}
          <OutputCards output={result} />
        </div>
      )}
    </main>
  );
}
