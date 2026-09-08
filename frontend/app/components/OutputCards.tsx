"use client";

import { useState } from "react";
import { PipelineOutput, SocialSnippet, Slide } from "@/lib/types";

interface OutputCardsProps {
  output: PipelineOutput;
}

interface CopyButtonProps {
  text: string;
  label: string;
}

function CopyButton({ text, label }: CopyButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      alert("Failed to copy to clipboard.");
    }
  };

  return (
    <button
      onClick={handleCopy}
      className="text-sm text-blue-600 hover:text-blue-800 underline"
    >
      {copied ? "Copied!" : `Copy ${label}`}
    </button>
  );
}

function ErrorBadge({ message }: { message: string }) {
  return (
    <span className="px-2 py-1 bg-red-100 text-red-700 text-xs font-medium rounded">
      Failed
    </span>
  );
}

function InlineError({ assetKey, message }: { assetKey: string; message: string }) {
  return (
    <div className="mb-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-800">
      <span className="font-semibold">Error generating {assetKey.replace("_", " ")}:</span>{" "}
      {message}
    </div>
  );
}

interface AssetCardProps {
  title: string;
  errorKey: "executive_brief" | "social_snippets" | "slide_deck";
  error?: string;
  children: React.ReactNode;
}

function AssetCard({ title, errorKey, error, children }: AssetCardProps) {
  return (
    <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        {error && <ErrorBadge message={error} />}
      </div>
      {error && <InlineError assetKey={errorKey} message={error} />}
      {children}
    </section>
  );
}

interface ErrorOnlyCardProps {
  title: string;
  errorKey: "executive_brief" | "social_snippets" | "slide_deck";
  error: string;
}

function ErrorOnlyCard({ title, errorKey, error }: ErrorOnlyCardProps) {
  return (
    <section className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900">{title}</h2>
        <ErrorBadge message={error} />
      </div>
      <InlineError assetKey={errorKey} message={error} />
    </section>
  );
}

export function OutputCards({ output }: OutputCardsProps) {
  return (
    <div className="space-y-6 mt-8">
      {output.executive_brief ? (
        <AssetCard
          title="Executive Brief"
          errorKey="executive_brief"
          error={output.errors.executive_brief}
        >
          <div className="space-y-3">
            <h3 className="text-lg font-semibold">{output.executive_brief.headline}</h3>
            <p className="text-gray-700">{output.executive_brief.summary}</p>
            <ul className="list-disc list-inside space-y-1">
              {output.executive_brief.key_points.map((point, i) => (
                <li key={i} className="text-gray-700">
                  {point}
                </li>
              ))}
            </ul>
            <p className="font-medium text-blue-700">
              {output.executive_brief.call_to_action}
            </p>
            <CopyButton
              text={[
                output.executive_brief.headline,
                "",
                output.executive_brief.summary,
                "",
                ...output.executive_brief.key_points,
                "",
                output.executive_brief.call_to_action,
              ].join("\n")}
              label="Executive Brief"
            />
          </div>
        </AssetCard>
      ) : output.errors.executive_brief ? (
        <ErrorOnlyCard
          title="Executive Brief"
          errorKey="executive_brief"
          error={output.errors.executive_brief}
        />
      ) : null}

      {output.social_snippets ? (
        <AssetCard
          title="Social Snippets"
          errorKey="social_snippets"
          error={output.errors.social_snippets}
        >
          <div className="space-y-4">
            {output.social_snippets.map((snippet, i) => (
              <SocialSnippetCard key={i} snippet={snippet} />
            ))}
          </div>
        </AssetCard>
      ) : output.errors.social_snippets ? (
        <ErrorOnlyCard
          title="Social Snippets"
          errorKey="social_snippets"
          error={output.errors.social_snippets}
        />
      ) : null}

      {output.slide_deck ? (
        <AssetCard
          title="Slide Deck"
          errorKey="slide_deck"
          error={output.errors.slide_deck}
        >
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">{output.slide_deck.title}</h3>
            {output.slide_deck.slides.map((slide, i) => (
              <SlideCard key={i} index={i} slide={slide} />
            ))}
          </div>
        </AssetCard>
      ) : output.errors.slide_deck ? (
        <ErrorOnlyCard
          title="Slide Deck"
          errorKey="slide_deck"
          error={output.errors.slide_deck}
        />
      ) : null}
    </div>
  );
}

function SocialSnippetCard({ snippet }: { snippet: SocialSnippet }) {
  return (
    <div className="p-4 border border-gray-200 rounded-lg">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-semibold text-gray-500 uppercase">
          {snippet.platform}
        </span>
        <CopyButton text={snippet.text} label={snippet.platform} />
      </div>
      <p className="text-gray-800 whitespace-pre-wrap">{snippet.text}</p>
      {snippet.hashtags.length > 0 && (
        <p className="mt-2 text-sm text-blue-600">{snippet.hashtags.join(" ")}</p>
      )}
    </div>
  );
}

function SlideCard({ index, slide }: { index: number; slide: Slide }) {
  const copyText = [
    slide.title,
    ...slide.bullets,
    "",
    `Speaker notes: ${slide.speaker_notes}`,
  ].join("\n");

  return (
    <div className="p-4 border border-gray-200 rounded-lg">
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-semibold">
          Slide {index + 1}: {slide.title}
        </h4>
        <CopyButton text={copyText} label={`Slide ${index + 1}`} />
      </div>
      <ul className="list-disc list-inside space-y-1 mb-2">
        {slide.bullets.map((bullet, j) => (
          <li key={j} className="text-gray-700">
            {bullet}
          </li>
        ))}
      </ul>
      <p className="text-sm text-gray-500 italic">{slide.speaker_notes}</p>
    </div>
  );
}
