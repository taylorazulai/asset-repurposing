# Decision: Frontend Dependency Versions

**Date:** 2026-09-07
**Decision:** Pin the Next.js frontend to `next@16.3.4`, `react@18.3.1`, `react-dom@18.3.1`, and `postcss@8.5.28`.
**Status:** Accepted

## Context

The project spec calls for a Next.js 14+ (App Router) frontend with React 18, TypeScript ≥5, and Tailwind CSS 3+. The initial dependency selection was `next@14.2.5`, `react@18.3.1`, `react-dom@18.3.1`, and `postcss@8.4.39`. After installing, `npm audit` reported multiple high-severity vulnerabilities in Next.js and PostCSS, so we needed to choose a pinned set that satisfies both the spec and a clean security audit.

## Options Considered

1. **Stay on Next.js 14.x (latest patch)**
   - Upgraded to `next@14.2.35`, the latest available 14.x release at the time.
   - `npm audit` still reported multiple high-severity advisories (DoS, SSRF, cache poisoning, middleware bypass) and a transitive PostCSS vulnerability.
   - Rejected because leaving known high-severity vulnerabilities in a portfolio project is unacceptable.

2. **Upgrade to Next.js 15.5.21**
   - Satisfies the "14+" constraint and is React-18 compatible.
   - `npm audit` still reported three high-severity issues (Next.js via PostCSS and Sharp).
   - Rejected because the audit was not clean.

3. **Upgrade to Next.js 16.3.4**
   - Satisfies the "14+" constraint and keeps React 18.3.1 compatibility.
   - Resolved all Next.js-related advisories.
   - Required bumping the direct `postcss` devDependency from `8.4.39` to `8.5.28` to clear the remaining PostCSS audit finding.
   - Selected because it produced a clean `npm audit` while preserving the requested stack (React 18, App Router, TypeScript, Tailwind CSS).

## Decision

Adopt the following pinned frontend versions:

| Package | Version | Reason |
|---------|---------|--------|
| `next` | `16.3.4` | Latest stable that clears all `npm audit` findings while staying within the "Next.js 14+" requirement. |
| `react` | `18.3.1` | Explicitly requested in the spec; compatible with Next.js 16. |
| `react-dom` | `18.3.1` | Matches React version. |
| `typescript` | `5.5.3` | Satisfies "TypeScript ≥5". |
| `tailwindcss` | `3.4.6` | Satisfies "Tailwind CSS 3+". |
| `postcss` | `8.5.28` | Direct devDependency bumped to clear CVEs related to source-map loading and CSS stringification. |
| `autoprefixer` | `10.4.19` | Standard Tailwind peer. |
| `@types/node` | `20.14.10` | Node 20 LTS types. |
| `@types/react` / `@types/react-dom` | `18.3.3` / `18.3.0` | Match React 18. |

## Consequences

- The frontend now runs Next.js 16 instead of 14. All code remains in the App Router and uses React 18 hooks, so no framework-level migration was needed.
- `next.config.js` uses `output: 'standalone'` for Cloud Run compatibility, which is supported unchanged in Next.js 16.
- The Dockerfile and multi-stage build do not require changes beyond the version pins.
- Pinning exact versions improves reproducibility and avoids future surprise audit failures from semver auto-upgrades.

## Verification

- `npm install` completed successfully.
- `npm audit` returned **0 vulnerabilities**.
- `npm run build` completed with no TypeScript errors and prerendered the `/` route as static content.

## References

- `frontend/package.json`
- `docs/running-doc.md` — Stages 5 & 6 recap
