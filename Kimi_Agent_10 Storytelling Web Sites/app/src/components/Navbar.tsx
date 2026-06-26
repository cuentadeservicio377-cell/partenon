import { useEffect, useState, useCallback } from 'react';
import { Link, useLocation } from 'react-router';
import { useLenis } from 'lenis/react';

const navLinks = [
  { label: 'THE MYTH', href: '#myth' },
  { label: 'THE HEROES', href: '#heroes' },
  { label: 'THE VISION', href: '#vision' },
  { label: 'FOR DEVELOPERS', href: '/developers' },
];

function ParthenonLogo({ className = '' }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <path
        d="M2 28h28M4 28V12h3v16M12 28V8h3v20M20 28V8h3v20M25 28V12h3v16M2 12l14-8 14 8"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
    </svg>
  );
}

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [isDark, setIsDark] = useState(false);
  const [activeSection, setActiveSection] = useState('');
  const [wordmarkVisible, setWordmarkVisible] = useState(true);
  const location = useLocation();
  const lenis = useLenis();
  const isHome = location.pathname === '/';

  const handleNavClick = useCallback(
    (e: React.MouseEvent, href: string) => {
      if (href.startsWith('#') && isHome) {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target && lenis) {
          lenis.scrollTo(target as HTMLElement, { offset: -60 });
        }
      }
    },
    [isHome, lenis],
  );

  useEffect(() => {
    const handleScroll = () => {
      const y = window.scrollY;
      setScrolled(y > 50);
      setWordmarkVisible(y < 200);

      // Detect dark sections
      const darkSections = document.querySelectorAll('[data-dark-section]');
      let inDark = false;
      darkSections.forEach((section) => {
        const rect = section.getBoundingClientRect();
        if (rect.top < 72 && rect.bottom > 72) {
          inDark = true;
        }
      });
      setIsDark(inDark);

      // Detect active section
      if (isHome) {
        const sections = ['myth', 'heroes', 'vision', 'how-it-works', 'cta'];
        for (const id of sections) {
          const el = document.getElementById(id);
          if (el) {
            const rect = el.getBoundingClientRect();
            if (rect.top < 200 && rect.bottom > 200) {
              setActiveSection(`#${id}`);
              break;
            }
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isHome]);

  const bgClass = isDark
    ? 'bg-[rgba(26,26,30,0.9)] text-[#F7F5F0]'
    : 'bg-[rgba(247,245,240,0.9)] text-[#2A2A2E]';

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 backdrop-blur-[12px] ${bgClass}`}
      style={{
        height: scrolled ? '60px' : '72px',
        transitionTimingFunction: 'var(--ease-out-expo)',
      }}
    >
      <div className="mx-auto flex h-full items-center justify-between px-6" style={{ maxWidth: 'var(--container-max)' }}>
        {/* Logo */}
        <Link to="/" className="flex items-center gap-3">
          <ParthenonLogo className="h-8 w-8" />
          <span
            className="font-cinzel text-sm tracking-[0.12em] transition-opacity duration-300"
            style={{
              opacity: wordmarkVisible ? 1 : 0,
              width: wordmarkVisible ? 'auto' : 0,
              overflow: 'hidden',
            }}
          >
            THE PARTENON
          </span>
        </Link>

        {/* Center Nav Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => {
            const isActive =
              link.href.startsWith('#') && activeSection === link.href;
            const isExternal = link.href.startsWith('/');
            return isExternal ? (
              <Link
                key={link.label}
                to={link.href}
                className={`relative text-xs font-medium tracking-[0.08em] transition-colors duration-200 hover:text-[#635BFF] ${
                  isActive ? 'text-[#635BFF]' : ''
                }`}
              >
                {link.label}
                {isActive && (
                  <span className="absolute -bottom-1 left-0 right-0 h-0.5 bg-[#635BFF]" />
                )}
              </Link>
            ) : (
              <a
                key={link.label}
                href={link.href}
                onClick={(e) => handleNavClick(e, link.href)}
                className={`relative text-xs font-medium tracking-[0.08em] transition-colors duration-200 hover:text-[#635BFF] ${
                  isActive ? 'text-[#635BFF]' : ''
                }`}
              >
                {link.label}
                {isActive && (
                  <span className="absolute -bottom-1 left-0 right-0 h-0.5 bg-[#635BFF]" />
                )}
              </a>
            );
          })}
        </div>

        {/* CTA Button */}
        <Link
          to="/developers"
          className={`hidden md:inline-flex items-center rounded-pill px-6 py-2.5 text-sm font-semibold tracking-[0.04em] transition-all duration-200 hover:scale-[1.02] ${
            isDark
              ? 'border-2 border-[#635BFF] text-[#635BFF] hover:bg-[#635BFF] hover:text-white'
              : 'bg-[#635BFF] text-[#F7F5F0] hover:shadow-glow-indigo'
          }`}
          style={{ borderRadius: 'var(--radius-pill)' }}
        >
          INSTALL HERMES
        </Link>

        {/* Mobile hamburger placeholder */}
        <button className="md:hidden flex flex-col gap-1.5">
          <span className="block h-0.5 w-6 bg-current" />
          <span className="block h-0.5 w-6 bg-current" />
          <span className="block h-0.5 w-6 bg-current" />
        </button>
      </div>
    </nav>
  );
}
