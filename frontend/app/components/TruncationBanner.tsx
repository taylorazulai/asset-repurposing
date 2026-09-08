"use client";

interface TruncationBannerProps {
  visible: boolean;
}

export function TruncationBanner({ visible }: TruncationBannerProps) {
  if (!visible) return null;

  return (
    <div className="bg-warnBg border border-warnText rounded-lg p-4 flex items-start gap-3">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="w-5 h-5 text-warnText flex-shrink-0 mt-0.5"
        aria-hidden="true"
      >
        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
        <path d="M12 9v4" />
        <path d="M12 17h.01" />
      </svg>
      <div>
        <p className="text-warnText font-medium">Source was truncated</p>
        <p className="text-warnText text-sm mt-0.5">
          The input exceeded the maximum length and was shortened before
          analysis. The assets below were generated from the shortened excerpt.
        </p>
      </div>
    </div>
  );
}
