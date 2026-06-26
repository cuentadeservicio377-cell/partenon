/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive) / <alpha-value>)",
          foreground: "hsl(var(--destructive-foreground) / <alpha-value>)",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // Partenon design tokens
        'marble-white': '#F7F5F0',
        'parchment': '#EDE8DF',
        'deep-stone': '#2A2A2E',
        'midnight': '#1A1A1E',
        'stripe-indigo': '#635BFF',
        'envidia-green': '#76B900',
        'glow-amber': '#FFB800',
        'myth-gold': '#D4A853',
        'hero-scribe': '#4A90A4',
        'hero-herald': '#9B59B6',
        'hero-collector': '#635BFF',
        'hero-guardian': '#76B900',
        'hero-strategist': '#FFB800',
        'hero-diplomat': '#E74C3C',
        'hero-brain': '#D4A853',
        'text-primary': '#2A2A2E',
        'text-secondary': '#6B6B73',
        'text-light': '#F7F5F0',
      },
      fontFamily: {
        'cinzel': ['Cinzel', 'Georgia', 'serif'],
        'inter': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
        'cinzel-decorative': ['Cinzel Decorative', 'Georgia', 'serif'],
      },
      spacing: {
        'xs': '0.5rem',
        'sm': '1rem',
        'md': '2rem',
        'lg': '4rem',
        'xl': '8rem',
        '2xl': '12rem',
      },
      borderRadius: {
        xl: "calc(var(--radius) + 4px)",
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
        xs: "calc(var(--radius) - 6px)",
        'sm-token': '4px',
        'md-token': '8px',
        'lg-token': '16px',
        'xl-token': '24px',
        'pill': '9999px',
      },
      boxShadow: {
        xs: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        'sm-token': '0 1px 3px rgba(42,42,46,0.06)',
        'md-token': '0 4px 16px rgba(42,42,46,0.08)',
        'lg-token': '0 12px 40px rgba(42,42,46,0.12)',
        'glow-indigo': '0 0 30px rgba(99,91,255,0.3)',
        'glow-green': '0 0 30px rgba(118,185,0,0.3)',
        'glow-gold': '0 0 40px rgba(212,168,83,0.25)',
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "caret-blink": {
          "0%,70%,100%": { opacity: "1" },
          "20%,50%": { opacity: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "caret-blink": "caret-blink 1.25s ease-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
