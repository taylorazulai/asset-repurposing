import "@/styles/globals.css";

export const metadata = {
  title: "Asset Repurposing Pipeline",
  description:
    "Decompose a source document into executive briefs, social snippets, and slide decks.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-cream text-[#1A1A1A] min-h-screen">{children}</body>
    </html>
  );
}
