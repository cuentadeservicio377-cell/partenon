import './globals.css';
import { Space_Grotesk, Geist_Mono } from 'next/font/google';

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
  display: 'swap',
});

const geistMono = Geist_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains-mono',
  display: 'swap',
});

export const metadata = {
  title: 'Partenon Mission Control',
  description: 'Dashboard de operaciones para agentes Hermes de Partenon.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={`${spaceGrotesk.variable} ${geistMono.variable}`}>
      <body className="min-h-screen bg-partenon-bg font-body antialiased">{children}</body>
    </html>
  );
}
