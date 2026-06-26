import { useEffect } from 'react';
import { ReactLenis } from 'lenis/react';
import type { ReactNode } from 'react';
import Navbar from './Navbar';
import Footer from './Footer';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  // Sync lenis with GSAP ScrollTrigger if needed
  useEffect(() => {
    // Any global scroll sync can go here
  }, []);

  return (
    <ReactLenis root options={{ lerp: 0.08, smoothWheel: true }}>
      <div className="flex flex-col min-h-[100dvh]">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </div>
    </ReactLenis>
  );
}
