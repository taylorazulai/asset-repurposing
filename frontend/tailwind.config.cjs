/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cream:    '#FBF6E9',
        heading:  '#065F46',
        muted:    '#6B7280',
        warnText: '#B91C1C',
        warnBg:   '#FEE2E2',
      },
    },
  },
  plugins: [],
};
