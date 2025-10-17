/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../modules/**/templates/**/*.html", // <-- subiu um nível
    "../modules/**/*.js",                // <-- idem
    "./static/js/**/*.js",
    "!./node_modules/**",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#AC50D3",
        secondary: "#2F3A27",
        background: "#ffffff",
        foreground: "#292826",
        muted: "#F8F8F8",
        "foreground-secondary": "#666666",
      },
    },
  },
  safelist: [
    "btn","btn-primary","btn-outline","btn-ghost",
    "bg-primary","text-foreground","border-primary",
    "px-3","py-2","text-sm","rounded-lg","p-2"
  ],
  plugins: [],
};
