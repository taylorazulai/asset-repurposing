"use client";

import { useState, useCallback } from "react";

interface UploadFormProps {
  onSubmit: (text: string) => void;
  loading: boolean;
}

const MIN_SOURCE_LENGTH = 50;
const MAX_FILE_SIZE_BYTES = 1024 * 1024;

export function UploadForm({ onSubmit, loading }: UploadFormProps) {
  const [text, setText] = useState("");
  const [fileError, setFileError] = useState<string | null>(null);

  const isValid = text.trim().length >= MIN_SOURCE_LENGTH;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isValid && !loading) {
      onSubmit(text.trim());
    }
  };

  const handleFileChange = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file) return;

      setFileError(null);

      if (!file.name.endsWith(".txt") && !file.name.endsWith(".md")) {
        setFileError("Only .txt and .md files are supported.");
        return;
      }

      if (file.size > MAX_FILE_SIZE_BYTES) {
        setFileError("File size must be less than 1 MB.");
        return;
      }

      const content = await file.text();
      setText(content);
    },
    []
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={`Paste your source document here (minimum ${MIN_SOURCE_LENGTH} characters)...`}
          disabled={loading}
          className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-60"
        />
        <div className="flex justify-between text-sm text-gray-500 mt-1">
          <span>{text.length} characters</span>
          <span>Minimum {MIN_SOURCE_LENGTH} characters</span>
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Or upload a file (optional, .txt or .md)
        </label>
        <input
          type="file"
          accept=".txt,.md,text/plain,text/markdown"
          onChange={handleFileChange}
          disabled={loading}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 disabled:opacity-60"
        />
        {fileError && (
          <p className="mt-1 text-sm text-red-600">{fileError}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={loading || !isValid}
        className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? "Generating assets..." : "Generate Assets"}
      </button>
    </form>
  );
}
