// Footer component

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

export default function Footer() {
  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer className="w-full bg-midnight text-[#F7F5F0]" style={{ padding: '6rem 0 3rem' }}>
      <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
        {/* Top Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          {/* Col 1: Logo + Tagline */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <ParthenonLogo className="h-8 w-8 text-[#F7F5F0]" />
              <span className="font-cinzel text-sm tracking-[0.12em]">
                THE PARTENON
              </span>
            </div>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              Where Heroes Assemble for Every Enterprise
            </p>
          </div>

          {/* Col 2: Navigation */}
          <div>
            <h4 className="font-inter text-xs font-semibold tracking-[0.12em] mb-4 text-[#6B6B73]">
              NAVIGATION
            </h4>
            <ul className="space-y-2">
              {[
                { label: 'The Myth', id: 'myth' },
                { label: 'The Heroes', id: 'heroes' },
                { label: 'The Vision', id: 'vision' },
                { label: 'GitHub', id: '' },
                { label: 'Documentation', id: '' },
              ].map((item) => (
                <li key={item.label}>
                  {item.id ? (
                    <button
                      onClick={() => scrollToSection(item.id)}
                      className="text-sm transition-colors duration-200 hover:text-[#635BFF]"
                      style={{ color: 'rgba(247,245,240,0.6)' }}
                    >
                      {item.label}
                    </button>
                  ) : (
                    <span
                      className="text-sm"
                      style={{ color: 'rgba(247,245,240,0.6)' }}
                    >
                      {item.label}
                    </span>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Col 3: Partner Logos */}
          <div>
            <h4 className="font-inter text-xs font-semibold tracking-[0.12em] mb-4 text-[#6B6B73]">
              PARTNERS
            </h4>
            <div className="flex items-center gap-6">
              {/* Nose Research */}
              <div className="group relative flex items-center justify-center h-10 px-3 rounded-md transition-all duration-300 hover:bg-white/5 cursor-pointer">
                <span className="font-inter text-sm font-medium tracking-wide text-[#F7F5F0]/60 group-hover:text-[#F7F5F0] transition-colors">
                  Nose Research
                </span>
              </div>
              {/* Envidia */}
              <div className="group relative flex items-center justify-center h-10 px-3 rounded-md transition-all duration-300 hover:bg-[#76B900]/10 cursor-pointer">
                <span className="font-inter text-sm font-medium tracking-wide text-[#F7F5F0]/60 group-hover:text-[#76B900] transition-colors">
                  Envidia
                </span>
              </div>
              {/* Stripe */}
              <div className="group relative flex items-center justify-center h-10 px-3 rounded-md transition-all duration-300 hover:bg-[#635BFF]/10 cursor-pointer">
                <span className="font-inter text-sm font-medium tracking-wide text-[#F7F5F0]/60 group-hover:text-[#635BFF] transition-colors">
                  Stripe
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Decorative Divider */}
        <div
          className="h-px w-full mb-8"
          style={{
            background:
              'linear-gradient(to right, transparent, var(--myth-gold), transparent)',
          }}
        />

        {/* Bottom Row */}
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs" style={{ color: 'rgba(247,245,240,0.4)' }}>
            &copy; 2025 The Partenon. Built for the Nose Research &times; Envidia
            &times; Stripe Hackathon.
          </p>
          <span
            className="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium"
            style={{
              background: 'rgba(118,185,0,0.15)',
              color: 'var(--envidia-green)',
            }}
          >
            Open Source
          </span>
        </div>
      </div>
    </footer>
  );
}
