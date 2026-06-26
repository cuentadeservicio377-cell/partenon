import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        partenon: {
          bg: '#050505',
          surface: '#08080C',
          card: '#0E0E14',
          border: '#1C1C24',
          text: '#E8E8ED',
          muted: '#7A7A85',
          cyan: '#00D4FF',
          amber: '#FFB800',
        },
      },
      fontFamily: {
        display: ['var(--font-space-grotesk)', 'system-ui', 'sans-serif'],
        body: ['var(--font-space-grotesk)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-jetbrains-mono)', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
