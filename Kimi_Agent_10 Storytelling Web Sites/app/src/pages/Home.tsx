import { useEffect, useRef, useState, useCallback } from 'react';
import { Link } from 'react-router';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import {
  ArrowRight,
  Code2,
  Briefcase,
  Users,
  ListChecks,
  Landmark,
  CheckCircle,
  Download,
} from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

/* ─────────────────────────────────────────────
   Section 1: Two-Path Gateway (Hero)
   ───────────────────────────────────────────── */
function HeroGateway() {
  const containerRef = useRef<HTMLDivElement>(null);
  const leftPanelRef = useRef<HTMLDivElement>(null);
  const rightPanelRef = useRef<HTMLDivElement>(null);
  const leftTextRef = useRef<HTMLDivElement>(null);
  const rightTextRef = useRef<HTMLDivElement>(null);
  const emblemRef = useRef<HTMLDivElement>(null);
  const [hoveredPanel, setHoveredPanel] = useState<'left' | 'right' | null>(null);

  useGSAP(
    () => {
      const tl = gsap.timeline({ delay: 0.3 });

      tl.fromTo(
        leftPanelRef.current,
        { x: '-100%' },
        { x: '0%', duration: 1, ease: 'expo.out' },
        0,
      );
      tl.fromTo(
        rightPanelRef.current,
        { x: '100%' },
        { x: '0%', duration: 1, ease: 'expo.out' },
        0,
      );
      tl.fromTo(
        emblemRef.current,
        { scale: 0, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.6, ease: 'back.out(1.7)' },
        0.5,
      );
      tl.fromTo(
        leftTextRef.current?.children || [],
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.12, ease: 'expo.out' },
        0.8,
      );
      tl.fromTo(
        rightTextRef.current?.children || [],
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.12, ease: 'expo.out' },
        0.9,
      );
    },
    { scope: containerRef },
  );

  const scrollToMyth = useCallback(() => {
    const el = document.getElementById('myth');
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }, []);

  return (
    <section
      ref={containerRef}
      className="relative flex min-h-[100dvh] flex-col md:flex-row overflow-hidden"
    >
      {/* Left Panel */}
      <div
        ref={leftPanelRef}
        className="relative flex flex-1 items-center justify-center overflow-hidden transition-all duration-500"
        style={{
          backgroundColor: 'var(--marble-white)',
          flex: hoveredPanel === 'left' ? '1.22' : hoveredPanel === 'right' ? '0.82' : '1',
          transitionTimingFunction: 'var(--ease-out-expo)',
        }}
        onMouseEnter={() => setHoveredPanel('left')}
        onMouseLeave={() => setHoveredPanel(null)}
      >
        {/* Subtle bg overlay */}
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.08]"
          style={{
            backgroundImage: 'url(/hero-parthenon-bg.jpg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        />
        <div ref={leftTextRef} className="relative z-10 px-8 text-center max-w-md">
          <span
            className="mb-4 inline-block font-inter text-xs font-semibold tracking-[0.16em]"
            style={{ color: 'var(--stripe-indigo)' }}
          >
            HACKATHON 2025
          </span>
          <h1
            className="font-cinzel mb-4"
            style={{
              fontSize: 'clamp(2.5rem, 6vw, 5rem)',
              letterSpacing: '0.08em',
              lineHeight: 1.05,
              color: 'var(--deep-stone)',
            }}
          >
            THE
            <br />
            PARTENON
          </h1>
          <p
            className="mb-8 font-inter text-base leading-relaxed"
            style={{ color: 'var(--text-secondary)', maxWidth: '360px', margin: '0 auto 2rem' }}
          >
            Where heroes assemble for every enterprise. A complete AI agent system
            built for entrepreneurs.
          </p>
          <button
            onClick={scrollToMyth}
            className="inline-flex items-center gap-2 rounded-pill px-8 py-3.5 font-inter text-sm font-semibold tracking-[0.04em] text-white transition-all duration-200 hover:scale-[1.02] hover:shadow-glow-indigo"
            style={{
              backgroundColor: 'var(--stripe-indigo)',
              borderRadius: 'var(--radius-pill)',
            }}
          >
            ENTER THE TEMPLE
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Center Divider + Emblem */}
      <div className="absolute left-1/2 top-0 bottom-0 z-20 hidden md:flex -translate-x-1/2 flex-col items-center justify-center pointer-events-none">
        <div
          className="h-full w-px"
          style={{
            background:
              'linear-gradient(to bottom, transparent, var(--myth-gold), transparent)',
            opacity: 0.4,
          }}
        />
        <div
          ref={emblemRef}
          className="absolute flex h-12 w-12 items-center justify-center rounded-full border-2"
          style={{ borderColor: 'var(--myth-gold)', background: 'var(--marble-white)' }}
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            className="h-5 w-5"
            stroke="var(--myth-gold)"
            strokeWidth="1.5"
          >
            <path d="M2 20h20M4 20V10h2v10M10 20V6h2v14M16 20V6h2v14M20 20V10h2v10M2 10l10-6 10 6" />
          </svg>
        </div>
      </div>

      {/* Right Panel */}
      <div
        ref={rightPanelRef}
        className="relative flex flex-1 items-center justify-center overflow-hidden transition-all duration-500"
        style={{
          backgroundColor: 'var(--midnight)',
          flex: hoveredPanel === 'right' ? '1.22' : hoveredPanel === 'left' ? '0.82' : '1',
          transitionTimingFunction: 'var(--ease-out-expo)',
        }}
        onMouseEnter={() => setHoveredPanel('right')}
        onMouseLeave={() => setHoveredPanel(null)}
      >
        {/* Grid pattern */}
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            backgroundImage:
              'linear-gradient(rgba(247,245,240,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(247,245,240,0.03) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />
        <div ref={rightTextRef} className="relative z-10 px-8 text-center max-w-md">
          <span
            className="mb-4 inline-block font-inter text-xs font-semibold tracking-[0.16em]"
            style={{ color: 'var(--envidia-green)' }}
          >
            TECHNICAL DOCUMENTATION
          </span>
          <h1
            className="font-cinzel mb-4"
            style={{
              fontSize: 'clamp(2.5rem, 6vw, 5rem)',
              letterSpacing: '0.08em',
              lineHeight: 1.05,
            }}
          >
            <span style={{ color: 'var(--marble-white)' }}>FOR</span>
            <br />
            <span style={{ color: 'var(--stripe-indigo)' }}>DEVELOPERS</span>
          </h1>
          <p
            className="mb-8 font-inter text-base leading-relaxed"
            style={{
              color: 'rgba(247,245,240,0.6)',
              maxWidth: '360px',
              margin: '0 auto 2rem',
            }}
          >
            Architecture, MCP connections, workshop structure, and technical
            specifications.
          </p>
          <Link
            to="/developers"
            className="inline-flex items-center gap-2 rounded-pill px-8 py-3.5 font-inter text-sm font-semibold tracking-[0.04em] transition-all duration-200 hover:scale-[1.02]"
            style={{
              border: '2px solid var(--stripe-indigo)',
              color: 'var(--stripe-indigo)',
              borderRadius: 'var(--radius-pill)',
            }}
          >
            <Code2 className="h-4 w-4" />
            VIEW THE SCHEMATICS
          </Link>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   Section 2: The Myth (Brand Story)
   ───────────────────────────────────────────── */
function TheMyth() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 80%',
          end: 'top 20%',
          toggleActions: 'play none none none',
        },
      });

      tl.fromTo(
        '.myth-eyebrow',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
      );
      tl.fromTo(
        '.myth-headline span',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.08, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.myth-divider',
        { scaleX: 0 },
        { scaleX: 1, duration: 0.5, ease: 'expo.out' },
        '-=0.3',
      );
      tl.fromTo(
        '.myth-desc',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.myth-left-col > *',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.12, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.myth-hermes',
        { scale: 0.9, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.8, ease: 'expo.out' },
        '-=0.5',
      );
      tl.fromTo(
        '.myth-archetype-icon',
        { scale: 0, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.4, stagger: 0.1, ease: 'back.out(1.7)' },
        '-=0.3',
      );
    },
    { scope: sectionRef },
  );

  const archetypes = [
    { name: 'THE SCRIBE', color: '#4A90A4' },
    { name: 'THE HERALD', color: '#9B59B6' },
    { name: 'THE COLLECTOR', color: '#635BFF' },
    { name: 'THE GUARDIAN', color: '#76B900' },
    { name: 'THE STRATEGIST', color: '#FFB800' },
    { name: 'THE DIPLOMAT', color: '#E74C3C' },
    { name: 'THE BRAIN', color: '#D4A853' },
  ];

  return (
    <section
      id="myth"
      ref={sectionRef}
      className="relative w-full overflow-hidden"
      style={{
        backgroundColor: 'var(--parchment)',
        padding: 'var(--section-pad-y) 0',
      }}
    >
      {/* Marble texture overlay */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.05]"
        style={{ backgroundImage: 'url(/marble-texture.jpg)' }}
      />

      <div className="relative z-10 mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
        {/* Section Header */}
        <div className="mb-16 text-center" style={{ maxWidth: 'var(--container-narrow)', margin: '0 auto 4rem' }}>
          <span
            className="myth-eyebrow mb-3 inline-block font-inter text-xs font-semibold tracking-[0.12em]"
            style={{ color: 'var(--myth-gold)' }}
          >
            THE FOUNDATION
          </span>
          <h2
            className="myth-headline font-cinzel mb-4"
            style={{
              fontSize: 'clamp(1.75rem, 4vw, 3rem)',
              letterSpacing: '0.06em',
              lineHeight: 1.1,
              color: 'var(--deep-stone)',
            }}
          >
            {'EVERY ENTERPRISE NEEDS ITS HEROES'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">{word}</span>
            ))}
          </h2>
          <div
            className="myth-divider mx-auto mb-4 h-0.5 w-12"
            style={{ backgroundColor: 'var(--myth-gold)' }}
          />
          <p className="myth-desc font-inter text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
            For millennia, the Parthenon stood as a monument to collective excellence —
            where individual mastery served a greater purpose. Today, The Partenon brings
            that archetype to your business.
          </p>
        </div>

        {/* Two-column content */}
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-16 items-center mb-16">
          {/* Left Column */}
          <div className="myth-left-col space-y-6">
            <h3
              className="font-cinzel text-xl tracking-[0.04em]"
              style={{ color: 'var(--deep-stone)' }}
            >
              ARCHETYPES, NOT ALGORITHMS
            </h3>
            <p className="font-inter text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
              We don&apos;t believe in faceless automation. The Partenon is built on the
              understanding that every business function has an archetypal essence — the
              meticulous record-keeper, the persuasive communicator, the vigilant guardian,
              the strategic coordinator.
            </p>
            <p className="font-inter text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
              Each hero in The Partenon embodies an archetype that resonates across all human
              enterprise. They don&apos;t just process tasks — they bring a perspective, a
              personality, a way of approaching problems that feels intuitively right.
            </p>
            <p className="font-inter text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
              This isn&apos;t Greek mythology cosplay. It&apos;s using timeless patterns of
              human excellence to build AI agents that entrepreneurs actually want to work with.
            </p>
            <button
              onClick={() => document.getElementById('heroes')?.scrollIntoView({ behavior: 'smooth' })}
              className="inline-flex items-center gap-2 font-inter text-sm font-semibold transition-colors duration-200 hover:opacity-70"
              style={{ color: 'var(--stripe-indigo)' }}
            >
              MEET THE HEROES <ArrowRight className="h-4 w-4" />
            </button>
          </div>

          {/* Right Column — Hermes */}
          <div className="flex flex-col items-center">
            <div
              className="myth-hermes relative mb-4"
              style={{ maxWidth: '400px', width: '80%' }}
            >
              <div
                className="absolute inset-0 rounded-2xl"
                style={{
                  background: 'var(--shadow-glow-gold)',
                  filter: 'blur(40px)',
                  opacity: 0.4,
                }}
              />
              <img
                src="/hermes-centerpiece.png"
                alt="Hermes — the enterprise hub"
                className="relative w-full h-auto"
                loading="lazy"
              />
            </div>
            <p className="text-center font-inter text-xs tracking-[0.08em]" style={{ color: 'var(--text-secondary)' }}>
              Hermes: The enterprise. The central hub. The reason heroes assemble.
            </p>
          </div>
        </div>

        {/* Bottom Archetype Band */}
        <div className="flex items-center justify-center gap-4 md:gap-8 flex-wrap">
          {archetypes.map((a, i) => (
            <div key={a.name} className="myth-archetype-icon flex flex-col items-center gap-2">
              <div
                className="flex h-12 w-12 md:h-16 md:w-16 items-center justify-center rounded-full"
                style={{ backgroundColor: a.color }}
              >
                <span className="font-cinzel text-xs font-bold text-white">{i + 1}</span>
              </div>
              <span
                className="font-inter text-[10px] font-medium tracking-[0.08em]"
                style={{ color: 'var(--text-secondary)' }}
              >
                {a.name}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   Section 3: The Heroes — Agent Profiles
   ───────────────────────────────────────────── */

interface HeroData {
  name: string;
  archetype: string;
  color: string;
  description: string;
  skills: string[];
  icon: string;
  link: string;
  isBrain?: boolean;
}

const heroesData: HeroData[] = [
  {
    name: 'THE SCRIBE',
    archetype: 'FINANCIAL ARCHITECT',
    color: '#4A90A4',
    description:
      'Master of numbers and structures. The Scribe transforms chaotic business data into crystal-clear dashboards, financial models, and strategic insights using Google Sheets.',
    skills: ['Google Sheets', 'Financial Modeling', 'Dashboards', 'Data Analysis', '.finance files'],
    icon: '/hero-scribe-icon.png',
    link: '/heroes#scribe',
  },
  {
    name: 'THE HERALD',
    archetype: 'VOICE OF THE BRAND',
    color: '#9B59B6',
    description:
      'The communicator who gives your brand a voice. The Herald crafts campaigns, manages social presence, builds SEO strategies, and ensures your message reaches the right people.',
    skills: ['Social Media', 'SEO/GEO', 'Brand Strategy', 'Content Calendar', '.design files'],
    icon: '/hero-herald-icon.png',
    link: '/heroes#herald',
  },
  {
    name: 'THE COLLECTOR',
    archetype: 'PAYMENT GUARDIAN',
    color: '#635BFF',
    description:
      'The financial gatekeeper. The Collector manages all Stripe operations — subscriptions, invoices, payment processing, and revenue tracking — ensuring every transaction flows smoothly.',
    skills: ['Stripe API', 'Payment Processing', 'Invoicing', 'Revenue Tracking', 'Subscriptions'],
    icon: '/hero-collector-icon.png',
    link: '/heroes#collector',
  },
  {
    name: 'THE GUARDIAN',
    archetype: 'SENTINEL OF SYSTEMS',
    color: '#76B900',
    description:
      'The protector of your digital realm. The Guardian manages API keys, Envidia integrations, model access, and security protocols — ensuring The Partenon remains fortress-strong.',
    skills: ['Envidia Security', 'API Management', 'Model Administration', 'Access Control', 'MCP Protocols'],
    icon: '/hero-guardian-icon.png',
    link: '/heroes#guardian',
  },
  {
    name: 'THE STRATEGIST',
    archetype: 'MASTER OF OPERATIONS',
    color: '#FFB800',
    description:
      'The operational mind that keeps everything moving. The Strategist manages projects, calendars, deadlines, and internal coordination — ensuring no detail is ever lost.',
    skills: ['Google Calendar', 'Project Management', 'Task Orchestration', 'Email Management', 'Operations'],
    icon: '/hero-strategist-icon.png',
    link: '/heroes#strategist',
  },
  {
    name: 'THE DIPLOMAT',
    archetype: 'BRIDGE BETWEEN WORLDS',
    color: '#E74C3C',
    description:
      'The two-sided guardian of relationships. The Diplomat manages client communications, vendor coordination, and external partnerships — keeping both internal teams and external stakeholders aligned.',
    skills: ['CRM Management', 'Client Communication', 'Vendor Relations', 'Negotiation', 'Follow-ups'],
    icon: '/hero-diplomat-icon.png',
    link: '/heroes#diplomat',
  },
  {
    name: 'THE BRAIN',
    archetype: 'G-BRAIN OF GARITAN',
    color: '#D4A853',
    description:
      'The central intelligence that connects everything. The Brain analyzes cross-hero data, identifies patterns, suggests optimizations, and ensures The Partenon operates as a unified organism through MCP.',
    skills: ['MCP Protocol', 'Cross-Agent Analysis', 'Pattern Recognition', 'Strategic Insights', 'Data Synthesis'],
    icon: '/hero-brain-icon.png',
    link: '/heroes#brain',
    isBrain: true,
  },
];

function HeroCard({ hero }: { hero: HeroData }) {
  return (
    <div
      className={`hero-card group relative overflow-hidden rounded-2xl transition-all duration-300 hover:-translate-y-2 hover:shadow-lg-token ${
        hero.isBrain ? 'md:col-start-2 md:scale-105' : ''
      }`}
      style={{
        backgroundColor: 'var(--marble-white)',
        boxShadow: hero.isBrain ? 'var(--shadow-glow-gold)' : 'var(--shadow-md)',
      }}
    >
      {/* Color accent bar */}
      <div
        className="h-1 w-full transition-all duration-300 group-hover:h-1.5"
        style={{ backgroundColor: hero.color }}
      />

      <div className="p-6">
        {/* Icon */}
        <div
          className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full transition-transform duration-300 group-hover:rotate-[15deg]"
          style={{ backgroundColor: `${hero.color}15` }}
        >
          <img
            src={hero.icon}
            alt={hero.name}
            className="h-16 w-16 object-contain"
            loading="lazy"
          />
        </div>

        {/* Name */}
        <h3
          className="mb-2 text-center font-cinzel text-lg tracking-[0.04em]"
          style={{ color: 'var(--deep-stone)' }}
        >
          {hero.name}
        </h3>

        {/* Archetype pill */}
        <div className="mb-3 flex justify-center">
          <span
            className="rounded-full px-3 py-1 font-inter text-[10px] font-semibold tracking-[0.08em] text-white"
            style={{ backgroundColor: hero.color }}
          >
            {hero.archetype}
          </span>
        </div>

        {/* Description */}
        <p
          className="mb-4 text-center font-inter text-sm leading-relaxed"
          style={{ color: 'var(--text-secondary)' }}
        >
          {hero.description}
        </p>

        {/* Skills */}
        <div className="mb-4 flex flex-wrap justify-center gap-1.5">
          {hero.skills.map((skill) => (
            <span
              key={skill}
              className="rounded px-2 py-0.5 font-mono text-[10px] tracking-wide"
              style={{
                backgroundColor: 'rgba(42,42,46,0.06)',
                color: 'var(--text-secondary)',
              }}
            >
              {skill}
            </span>
          ))}
        </div>

        {/* View Profile link */}
        <Link
          to={hero.link}
          className="flex items-center justify-center gap-1 font-inter text-xs font-medium transition-colors duration-200"
          style={{ color: hero.color }}
        >
          VIEW PROFILE <ArrowRight className="h-3 w-3" />
        </Link>
      </div>
    </div>
  );
}

function TheHeroes() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 80%',
          toggleActions: 'play none none none',
        },
      });

      tl.fromTo(
        '.heroes-eyebrow',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
      );
      tl.fromTo(
        '.heroes-headline span',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.08, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.heroes-divider',
        { scaleX: 0 },
        { scaleX: 1, duration: 0.5, ease: 'expo.out' },
        '-=0.3',
      );
      tl.fromTo(
        '.heroes-desc',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.hero-card',
        { y: 80, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.heroes-diagram',
        { scale: 0.95, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.7, ease: 'expo.out' },
        '-=0.3',
      );
    },
    { scope: sectionRef },
  );

  return (
    <section
      id="heroes"
      ref={sectionRef}
      className="relative w-full"
      style={{
        backgroundColor: 'var(--marble-white)',
        padding: 'var(--section-pad-y) 0',
      }}
    >
      <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
        {/* Section Header */}
        <div className="mb-16 text-center" style={{ maxWidth: 'var(--container-narrow)', margin: '0 auto 4rem' }}>
          <span
            className="heroes-eyebrow mb-3 inline-block font-inter text-xs font-semibold tracking-[0.12em]"
            style={{ color: 'var(--stripe-indigo)' }}
          >
            THE ASSEMBLY
          </span>
          <h2
            className="heroes-headline font-cinzel mb-4"
            style={{
              fontSize: 'clamp(1.75rem, 4vw, 3rem)',
              letterSpacing: '0.06em',
              lineHeight: 1.1,
              color: 'var(--deep-stone)',
            }}
          >
            {'SEVEN HEROES. ONE MISSION.'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">{word}</span>
            ))}
          </h2>
          <div
            className="heroes-divider mx-auto mb-4 h-0.5 w-12 origin-center"
            style={{ backgroundColor: 'var(--stripe-indigo)' }}
          />
          <p className="heroes-desc font-inter text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
            Each hero brings a specialization, a personality, and a set of powerful tools.
            Together, they form The Partenon — a complete operational system for any enterprise.
          </p>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-16">
          {heroesData.map((hero) => (
            <HeroCard key={hero.name} hero={hero} />
          ))}
        </div>

        {/* Central Diagram */}
        <div className="heroes-diagram text-center">
          <img
            src="/parthenon-diagram.png"
            alt="The Partenon structure diagram"
            className="mx-auto mb-4 w-full"
            style={{ maxWidth: '800px' }}
            loading="lazy"
          />
          <p className="font-inter text-xs tracking-[0.08em]" style={{ color: 'var(--text-secondary)' }}>
            The Partenon structure: Hermes at the center, heroes connected in a circle of shared knowledge and tools.
          </p>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   Section 4: How It Works — Process Flow
   ───────────────────────────────────────────── */
const processSteps = [
  {
    num: '01',
    title: 'THE ENTREPRENEUR ARRIVES',
    body: 'You come with your business — a construction company, a cafe, a consultancy. Hermes asks the right questions: What do you sell? What are your costs? What keeps you up at night?',
    Icon: Briefcase,
  },
  {
    num: '02',
    title: 'HEROES ASSEMBLE',
    body: 'Based on your needs, Hermes activates the right heroes. The Scribe sets up your financial tracking. The Herald begins brand discovery. The Strategist creates your operational calendar. Each hero starts their mission.',
    Icon: Users,
  },
  {
    num: '03',
    title: 'MISSIONS IN MOTION',
    body: 'Heroes work collaboratively — The Herald requests budget data from The Scribe. The Collector sets up Stripe for your products. The Diplomat schedules client follow-ups. All progress tracked in shared Google Workspace.',
    Icon: ListChecks,
  },
  {
    num: '04',
    title: 'THE PARTENON THRIVES',
    body: 'Your business now has a complete operational system. Dashboards show real-time numbers. Campaigns run on schedule. Payments flow automatically. And The Brain continuously optimizes everything through cross-agent intelligence.',
    Icon: Landmark,
  },
];

function HowItWorks() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 70%',
          toggleActions: 'play none none none',
        },
      });

      tl.fromTo(
        '.process-eyebrow',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
      );
      tl.fromTo(
        '.process-headline span',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.08, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.process-line',
        { scaleX: 0 },
        { scaleX: 1, duration: 1.2, ease: 'expo.out' },
        '-=0.3',
      );
      tl.fromTo(
        '.process-step',
        { y: 50, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.15, ease: 'expo.out' },
        '-=0.8',
      );
      tl.fromTo(
        '.process-cta-bottom',
        { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' },
        '-=0.3',
      );
    },
    { scope: sectionRef },
  );

  return (
    <section
      id="how-it-works"
      ref={sectionRef}
      data-dark-section
      className="relative w-full overflow-hidden"
      style={{
        backgroundColor: 'var(--deep-stone)',
        padding: 'var(--section-pad-y) 0',
      }}
    >
      <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
        {/* Section Header */}
        <div className="mb-16 text-center" style={{ maxWidth: 'var(--container-narrow)', margin: '0 auto 4rem' }}>
          <span
            className="process-eyebrow mb-3 inline-block font-inter text-xs font-semibold tracking-[0.12em]"
            style={{ color: 'var(--glow-amber)' }}
          >
            THE PROCESS
          </span>
          <h2
            className="process-headline font-cinzel mb-4"
            style={{
              fontSize: 'clamp(1.75rem, 4vw, 3rem)',
              letterSpacing: '0.06em',
              lineHeight: 1.1,
              color: 'var(--marble-white)',
            }}
          >
            {'FROM CHAOS TO CLARITY'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">{word}</span>
            ))}
          </h2>
          <div
            className="process-divider mx-auto mb-4 h-0.5 w-12"
            style={{ backgroundColor: 'var(--glow-amber)' }}
          />
          <p className="process-desc font-inter text-base leading-relaxed" style={{ color: 'rgba(247,245,240,0.6)' }}>
            Hermes doesn&apos;t just automate — it understands your business, assembles the
            right heroes, and guides you through a collaborative journey of transformation.
          </p>
        </div>

        {/* Steps */}
        <div className="relative mb-16">
          {/* Connecting line (desktop) */}
          <div
            className="process-line absolute top-24 left-0 right-0 hidden lg:block h-px origin-left"
            style={{
              background:
                'linear-gradient(to right, var(--glow-amber), var(--stripe-indigo))',
            }}
          />

          <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4 relative z-10">
            {processSteps.map((step) => (
              <div key={step.num} className="process-step text-center">
                <span
                  className="mb-2 block font-cinzel text-5xl"
                  style={{ color: 'var(--glow-amber)', opacity: 0.3 }}
                >
                  {step.num}
                </span>
                <div className="mb-4 flex justify-center">
                  <div
                    className="flex h-12 w-12 items-center justify-center rounded-full"
                    style={{ backgroundColor: 'rgba(255,184,0,0.15)' }}
                  >
                    <step.Icon className="h-6 w-6" style={{ color: 'var(--glow-amber)' }} />
                  </div>
                </div>
                <h4
                  className="mb-3 font-inter text-base font-semibold tracking-wide"
                  style={{ color: 'var(--marble-white)' }}
                >
                  {step.title}
                </h4>
                <p
                  className="font-inter text-sm leading-relaxed"
                  style={{ color: 'rgba(247,245,240,0.6)' }}
                >
                  {step.body}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom CTA */}
        <div className="process-cta-bottom text-center">
          <h3
            className="font-cinzel text-xl mb-6"
            style={{ color: 'var(--marble-white)', letterSpacing: '0.04em' }}
          >
            Ready to assemble your heroes?
          </h3>
          <Link
            to="/developers"
            className="inline-flex items-center gap-2 rounded-pill px-8 py-3.5 font-inter text-sm font-semibold tracking-[0.04em] text-white transition-all duration-200 hover:scale-[1.02] hover:shadow-glow-indigo"
            style={{
              backgroundColor: 'var(--stripe-indigo)',
              borderRadius: 'var(--radius-pill)',
            }}
          >
            INSTALL HERMES NOW
          </Link>
          <p
            className="mt-4 font-inter text-xs tracking-[0.08em]"
            style={{ color: 'rgba(247,245,240,0.4)' }}
          >
            Open source. Free to install. Built for entrepreneurs.
          </p>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   Section 5: Impact Counter
   ───────────────────────────────────────────── */

interface CounterData {
  target: number;
  suffix: string;
  label: string;
  context: string;
  color: string;
}

const countersData: CounterData[] = [
  {
    target: 1000000,
    suffix: '',
    label: 'ENTREPRENEURS EMPOWERED',
    context: 'From 10 to 1,000,000 — every one with a complete operational system',
    color: '#635BFF',
  },
  {
    target: 40,
    suffix: '',
    label: 'HOURS SAVED MONTHLY',
    context: 'Average time entrepreneurs reclaim by automating operations',
    color: '#76B900',
  },
  {
    target: 95,
    suffix: '%',
    label: 'FINANCIAL CLARITY ACHIEVED',
    context: 'Percentage of users who report understanding their business numbers for the first time',
    color: '#4A90A4',
  },
  {
    target: 32,
    suffix: '%',
    label: 'AVERAGE REVENUE UPLIFT',
    context: 'Revenue increase within 6 months of implementing The Partenon',
    color: '#FFB800',
  },
  {
    target: 50000000,
    suffix: '',
    label: 'MISSIONS COMPLETED',
    context: 'Tasks, campaigns, analyses, and operations executed by heroes',
    color: '#9B59B6',
  },
  {
    target: 50,
    suffix: '',
    label: 'COUNTRIES REACHED',
    context: 'Global expansion through workshops, universities, and partnerships',
    color: '#E74C3C',
  },
];

function formatNumber(num: number): string {
  if (num >= 1000000) return (num / 1000000).toFixed(0) + ',000,000';
  if (num >= 1000) return num.toLocaleString();
  return num.toString();
}

function CounterBlock({ data, index }: { data: CounterData; index: number }) {
  const [count, setCount] = useState(0);
  const [hasAnimated, setHasAnimated] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasAnimated) {
            setHasAnimated(true);
            const duration = 2500;
            const start = performance.now();

            const animate = (now: number) => {
              const elapsed = now - start;
              const progress = Math.min(elapsed / duration, 1);
              // Spring-like easing
              const eased =
                progress === 1
                  ? 1
                  : 1 - Math.pow(2, -10 * progress) * Math.cos((progress * 10 - 0.75) * ((2 * Math.PI) / 3));
              setCount(Math.floor(eased * data.target));
              if (progress < 1) requestAnimationFrame(animate);
            };

            setTimeout(() => requestAnimationFrame(animate), index * 300);
          }
        });
      },
      { threshold: 0.5 },
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [hasAnimated, data.target, index]);

  return (
    <div ref={ref} className="text-center" style={{ maxWidth: '320px', margin: '0 auto' }}>
      <div
        className="font-cinzel mb-2 tabular-nums"
        style={{
          fontSize: 'clamp(2.5rem, 6vw, 4.5rem)',
          letterSpacing: '0.04em',
          lineHeight: 1,
          color: data.color,
          textShadow: `0 0 30px ${data.color}40`,
        }}
      >
        {formatNumber(count)}{data.suffix}
      </div>
      <div
        className="mb-2 font-inter text-xs font-semibold tracking-[0.12em]"
        style={{ color: 'var(--text-secondary)' }}
      >
        {data.label}
      </div>
      <p className="font-inter text-sm leading-relaxed" style={{ color: 'var(--text-secondary)', opacity: 0.7 }}>
        {data.context}
      </p>
    </div>
  );
}

function ImpactCounter() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 80%',
          toggleActions: 'play none none none',
        },
      });

      tl.fromTo(
        '.counter-eyebrow',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
      );
      tl.fromTo(
        '.counter-headline span',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.08, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.counter-divider',
        { scaleX: 0 },
        { scaleX: 1, duration: 0.5, ease: 'expo.out' },
        '-=0.3',
      );
    },
    { scope: sectionRef },
  );

  const milestones = [
    { num: 10, label: 'First 10 founders' },
    { num: 100, label: 'Early adopters' },
    { num: 1000, label: 'University partnerships begin' },
    { num: 10000, label: 'Regional expansion' },
    { num: 100000, label: 'Global network' },
    { num: 1000000, label: 'Worldwide impact' },
  ];

  return (
    <section
      id="vision"
      ref={sectionRef}
      className="relative w-full"
      style={{
        backgroundColor: 'var(--parchment)',
        padding: 'var(--section-pad-y) 0',
      }}
    >
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.08]"
        style={{ backgroundImage: 'url(/marble-texture.jpg)' }}
      />
      <div className="relative z-10 mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
        {/* Section Header */}
        <div className="mb-16 text-center" style={{ maxWidth: 'var(--container-narrow)', margin: '0 auto 4rem' }}>
          <span
            className="counter-eyebrow mb-3 inline-block font-inter text-xs font-semibold tracking-[0.12em]"
            style={{ color: 'var(--stripe-indigo)' }}
          >
            THE VISION
          </span>
          <h2
            className="counter-headline font-cinzel mb-4"
            style={{
              fontSize: 'clamp(1.75rem, 4vw, 3rem)',
              letterSpacing: '0.06em',
              lineHeight: 1.1,
              color: 'var(--deep-stone)',
            }}
          >
            {'SCALING FROM TEN TO ONE MILLION'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">{word}</span>
            ))}
          </h2>
          <div
            className="counter-divider mx-auto mb-4 h-0.5 w-12 origin-center"
            style={{ backgroundColor: 'var(--stripe-indigo)' }}
          />
          <p className="counter-desc font-inter text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
            Every entrepreneur we empower creates ripples. Here&apos;s what The Partenon can
            achieve as we grow — and the real impact on real businesses.
          </p>
        </div>

        {/* Counters Grid */}
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3 mb-20">
          {countersData.map((c, i) => (
            <CounterBlock key={c.label} data={c} index={i} />
          ))}
        </div>

        {/* Milestone Bar */}
        <div className="relative">
          <div
            className="hidden lg:block absolute left-0 right-0 top-5 h-0.5"
            style={{
              background:
                'linear-gradient(to right, var(--stripe-indigo), var(--envidia-green))',
            }}
          />
          <div className="grid grid-cols-2 gap-6 lg:grid-cols-6 lg:gap-4">
            {milestones.map((m, i) => (
              <div key={m.num} className="flex flex-col items-center text-center">
                <div
                  className="mb-2 flex h-10 w-10 items-center justify-center rounded-full border-2"
                  style={{
                    borderColor: i < 3 ? 'var(--stripe-indigo)' : 'rgba(42,42,46,0.2)',
                    backgroundColor: i < 3 ? 'var(--stripe-indigo)' : 'transparent',
                  }}
                >
                  <span
                    className="font-cinzel text-xs font-bold"
                    style={{ color: i < 3 ? 'white' : 'var(--text-secondary)' }}
                  >
                    {m.num >= 1000000 ? '1M' : m.num >= 1000 ? `${(m.num / 1000).toFixed(0)}K` : m.num}
                  </span>
                </div>
                <span
                  className="font-inter text-[10px] tracking-wide"
                  style={{ color: 'var(--text-secondary)' }}
                >
                  {m.label}
                </span>
                {i >= 3 && (
                  <span
                    className="mt-1 font-inter text-[9px] tracking-wide"
                    style={{ color: 'var(--text-secondary)', opacity: 0.5 }}
                  >
                    Coming soon
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   Section 6: The Growth Plan
   ───────────────────────────────────────────── */
const growthChannels = [
  {
    tag: 'GLOBAL REACH',
    tagColor: '#9B59B6',
    title: 'BIWEEKLY WEBINARS',
    body: 'Every 15 days, a live session for pre-registered entrepreneurs worldwide. We install Hermes together, configure heroes for each business, and leave everyone with a working operational system. 2 hours, zero cost, infinite value.',
    metrics: 'Target: 500 participants per session',
    cta: 'REGISTER FOR NEXT SESSION',
    image: null,
  },
  {
    tag: 'NEXT GENERATION',
    tagColor: '#4A90A4',
    title: 'UNIVERSITY PARTNERSHIPS',
    body: 'Collaborating with innovation departments, business accelerators, and extracurricular programs. Students from any discipline can adapt The Partenon to a business in their field — learning entrepreneurship by building real operational systems.',
    metrics: 'Target: 50 universities in Year 1',
    cta: 'PARTNER WITH US',
    image: '/growth-universities.jpg',
  },
  {
    tag: 'COMMUNITY',
    tagColor: '#E74C3C',
    title: 'BUSINESS ORGANIZATIONS',
    body: 'Workshops with BNI chapters, Rotary clubs, chambers of commerce, and Waypio networks. Members bring their businesses; we bring The Partenon. Every participant leaves with Hermes installed and heroes activated.',
    metrics: 'Target: 200 organizations per year',
    cta: 'JOIN THE NETWORK',
    image: null,
  },
  {
    tag: 'STARTUP ECOSYSTEM',
    tagColor: '#FFB800',
    title: 'COWORKING & ACCELERATORS',
    body: 'Partnerships with coworking spaces and business accelerators to make Hermes the default operational backbone for every startup in their portfolio. Custom agent configurations for accelerator cohorts.',
    metrics: 'Target: 100 spaces, 20 accelerators in Year 1',
    cta: 'BECOME A PARTNER',
    image: '/growth-coworking.jpg',
  },
];

function GrowthPlan() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 75%',
          toggleActions: 'play none none none',
        },
      });

      tl.fromTo(
        '.growth-eyebrow',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
      );
      tl.fromTo(
        '.growth-headline span',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.08, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.growth-divider',
        { scaleX: 0 },
        { scaleX: 1, duration: 0.5, ease: 'expo.out' },
        '-=0.3',
      );
      tl.fromTo(
        '.growth-card',
        { y: 60, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.15, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.growth-banner',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, ease: 'expo.out' },
        '-=0.3',
      );
    },
    { scope: sectionRef },
  );

  return (
    <section
      ref={sectionRef}
      className="relative w-full"
      style={{
        backgroundColor: 'var(--marble-white)',
        padding: 'var(--section-pad-y) 0',
      }}
    >
      <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
        {/* Section Header */}
        <div className="mb-16 text-center" style={{ maxWidth: 'var(--container-narrow)', margin: '0 auto 4rem' }}>
          <span
            className="growth-eyebrow mb-3 inline-block font-inter text-xs font-semibold tracking-[0.12em]"
            style={{ color: 'var(--envidia-green)' }}
          >
            THE PATH FORWARD
          </span>
          <h2
            className="growth-headline font-cinzel mb-4"
            style={{
              fontSize: 'clamp(1.75rem, 4vw, 3rem)',
              letterSpacing: '0.06em',
              lineHeight: 1.1,
              color: 'var(--deep-stone)',
            }}
          >
            {'HOW WE REACH THE WORLD'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">{word}</span>
            ))}
          </h2>
          <div
            className="growth-divider mx-auto mb-4 h-0.5 w-12 origin-center"
            style={{ backgroundColor: 'var(--envidia-green)' }}
          />
          <p className="growth-desc font-inter text-base leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
            A multi-channel strategy to bring The Partenon to entrepreneurs everywhere —
            from university auditoriums to coworking workshops.
          </p>
        </div>

        {/* Growth Cards Grid */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 mb-12">
          {growthChannels.map((channel) => (
            <div
              key={channel.title}
              className="growth-card group overflow-hidden rounded-2xl transition-all duration-300 hover:-translate-y-1 hover:shadow-lg-token"
              style={{ backgroundColor: 'var(--marble-white)', boxShadow: 'var(--shadow-md)' }}
            >
              {channel.image && (
                <div className="overflow-hidden">
                  <img
                    src={channel.image}
                    alt={channel.title}
                    className="h-48 w-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
                    loading="lazy"
                  />
                </div>
              )}
              <div className="p-6">
                <span
                  className="mb-3 inline-block rounded-full px-3 py-1 font-inter text-[10px] font-semibold tracking-[0.08em] text-white"
                  style={{ backgroundColor: channel.tagColor }}
                >
                  {channel.tag}
                </span>
                <h3
                  className="mb-3 font-cinzel text-lg tracking-[0.04em]"
                  style={{ color: 'var(--deep-stone)' }}
                >
                  {channel.title}
                </h3>
                <p
                  className="mb-4 font-inter text-sm leading-relaxed"
                  style={{ color: 'var(--text-secondary)' }}
                >
                  {channel.body}
                </p>
                <p
                  className="mb-4 font-inter text-xs tracking-wide"
                  style={{ color: 'var(--text-secondary)', opacity: 0.7 }}
                >
                  {channel.metrics}
                </p>
                <button
                  className="inline-flex items-center gap-1 font-inter text-xs font-semibold transition-colors duration-200 hover:opacity-70"
                  style={{ color: channel.tagColor }}
                >
                  {channel.cta} <ArrowRight className="h-3 w-3" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom Banner */}
        <div
          className="growth-banner flex flex-col md:flex-row items-center justify-between gap-6 rounded-2xl p-8"
          style={{ backgroundColor: 'var(--deep-stone)' }}
        >
          <h3
            className="font-cinzel text-lg tracking-[0.04em]"
            style={{ color: 'var(--glow-amber)' }}
          >
            THE ULTIMATE GOAL
          </h3>
          <p className="flex-1 text-center font-inter text-sm leading-relaxed" style={{ color: 'var(--marble-white)' }}>
            Make The Partenon the default operational intelligence system for every small
            business in the world — powered by Stripe, Envidia, and Nose Research.
          </p>
          <Link
            to="/developers"
            className="inline-flex items-center gap-2 rounded-pill px-6 py-2.5 font-inter text-sm font-semibold text-white transition-all duration-200 hover:scale-[1.02] hover:shadow-glow-indigo"
            style={{
              backgroundColor: 'var(--stripe-indigo)',
              borderRadius: 'var(--radius-pill)',
            }}
          >
            START WITH HERMES
          </Link>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   Section 7: Partners
   ───────────────────────────────────────────── */
function Partners() {
  const sectionRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      gsap.fromTo(
        '.partner-logo',
        { y: 20, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.2,
          ease: 'expo.out',
          scrollTrigger: {
            trigger: sectionRef.current,
            start: 'top 85%',
            toggleActions: 'play none none none',
          },
        },
      );
    },
    { scope: sectionRef },
  );

  const partners = [
    { name: 'Nose Research', hoverColor: '#F7F5F0' },
    { name: 'Envidia', hoverColor: '#76B900' },
    { name: 'Stripe', hoverColor: '#635BFF' },
  ];

  return (
    <section
      ref={sectionRef}
      data-dark-section
      className="relative w-full"
      style={{
        backgroundColor: 'var(--deep-stone)',
        padding: '4rem 0',
      }}
    >
      <div className="mx-auto px-6 text-center" style={{ maxWidth: 'var(--container-max)' }}>
        <span
          className="mb-8 inline-block font-inter text-xs font-semibold tracking-[0.12em]"
          style={{ color: 'rgba(247,245,240,0.4)' }}
        >
          POWERED BY
        </span>

        <div className="flex flex-col md:flex-row items-center justify-center gap-12 md:gap-20 mb-8">
          {partners.map((p) => (
            <div
              key={p.name}
              className="partner-logo group cursor-pointer transition-all duration-300"
            >
              <span
                className="font-inter text-xl font-semibold tracking-wide transition-colors duration-300"
                style={{ color: 'rgba(247,245,240,0.6)' }}
                onMouseEnter={(e) => {
                  (e.target as HTMLElement).style.color = p.hoverColor;
                }}
                onMouseLeave={(e) => {
                  (e.target as HTMLElement).style.color = 'rgba(247,245,240,0.6)';
                }}
              >
                {p.name}
              </span>
            </div>
          ))}
        </div>

        <p
          className="mx-auto max-w-xl font-inter text-sm leading-relaxed"
          style={{ color: 'rgba(247,245,240,0.5)' }}
        >
          The Partenon is built for the Nose Research &times; Envidia &times; Stripe
          Hackathon — and designed to become the operational backbone of every small enterprise.
        </p>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   Section 8: CTA / Install
   ───────────────────────────────────────────── */
function CTASection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const [typedText, setTypedText] = useState('');
  const fullText = 'npx create-hermes@latest';
  const hasTyped = useRef(false);

  useGSAP(
    () => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: 'top 75%',
          toggleActions: 'play none none none',
          onEnter: () => {
            if (hasTyped.current) return;
            hasTyped.current = true;
            let i = 0;
            const typeInterval = setInterval(() => {
              i++;
              setTypedText(fullText.slice(0, i));
              if (i >= fullText.length) clearInterval(typeInterval);
            }, 60);
          },
        },
      });

      tl.fromTo(
        '.cta-headline span',
        { y: 40, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.08, ease: 'expo.out' },
      );
      tl.fromTo(
        '.cta-code-block',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, ease: 'expo.out' },
        '-=0.3',
      );
      tl.fromTo(
        '.cta-buttons > *',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.4, stagger: 0.1, ease: 'expo.out' },
        '-=0.2',
      );
      tl.fromTo(
        '.cta-badge',
        { scale: 0, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.3, stagger: 0.08, ease: 'back.out(1.7)' },
        '-=0.2',
      );
    },
    { scope: sectionRef },
  );

  const badges = [
    'Open Source',
    'Free Forever',
    'MCP Ready',
    'Google Workspace Integrated',
  ];

  return (
    <section
      id="cta"
      ref={sectionRef}
      className="relative w-full"
      style={{
        background: 'linear-gradient(to bottom, var(--marble-white), var(--parchment))',
        padding: 'var(--section-pad-y) 0',
      }}
    >
      <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-narrow)' }}>
        {/* Greek key border top */}
        <div
          className="mb-12 h-4 w-full opacity-20"
          style={{
            backgroundImage: `repeating-linear-gradient(
              90deg,
              var(--deep-stone) 0px,
              var(--deep-stone) 8px,
              transparent 8px,
              transparent 16px
            )`,
            maskImage: 'repeating-linear-gradient(90deg, black 0px, black 8px, transparent 8px, transparent 16px)',
            WebkitMaskImage: 'repeating-linear-gradient(90deg, black 0px, black 8px, transparent 8px, transparent 16px)',
          }}
        />

        <div className="text-center">
          <h2
            className="cta-headline font-cinzel mb-4"
            style={{
              fontSize: 'clamp(2rem, 4vw, 3.5rem)',
              letterSpacing: '0.06em',
              lineHeight: 1.1,
              color: 'var(--deep-stone)',
            }}
          >
            {'YOUR PARTENON AWAITS'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">{word}</span>
            ))}
          </h2>
          <p
            className="mb-8 font-inter text-base leading-relaxed"
            style={{ color: 'var(--text-secondary)' }}
          >
            Hermes is open source and free to install. One command sets up your entire
            operational system. Your heroes are ready — all they need is a mission.
          </p>

          {/* Code Block */}
          <div
            className="cta-code-block mx-auto mb-8 flex items-center gap-3 rounded-lg px-6 py-4 text-left"
            style={{
              backgroundColor: 'var(--midnight)',
              maxWidth: '480px',
            }}
          >
            <span style={{ color: 'var(--envidia-green)' }}>$</span>
            <code className="font-mono text-sm" style={{ color: 'var(--marble-white)' }}>
              {typedText}
            </code>
            <span
              className="inline-block h-4 w-0.5 animate-pulse"
              style={{ backgroundColor: 'var(--envidia-green)' }}
            />
          </div>

          {/* CTAs */}
          <div className="cta-buttons mb-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/developers"
              className="inline-flex items-center gap-2 rounded-pill px-8 py-3.5 font-inter text-sm font-semibold tracking-[0.04em] text-white transition-all duration-200 hover:scale-[1.02] hover:shadow-glow-indigo"
              style={{
                backgroundColor: 'var(--stripe-indigo)',
                borderRadius: 'var(--radius-pill)',
              }}
            >
              <Download className="h-4 w-4" />
              INSTALL HERMES
            </Link>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-pill px-8 py-3.5 font-inter text-sm font-semibold tracking-[0.04em] transition-all duration-200 hover:scale-[1.02]"
              style={{
                border: '2px solid var(--deep-stone)',
                color: 'var(--deep-stone)',
                borderRadius: 'var(--radius-pill)',
              }}
            >
              View on GitHub
            </a>
          </div>

          <Link
            to="/developers"
            className="mb-8 inline-flex items-center gap-1 font-inter text-sm font-medium transition-colors duration-200 hover:opacity-70"
            style={{ color: 'var(--stripe-indigo)' }}
          >
            Read the Technical Documentation <ArrowRight className="h-4 w-4" />
          </Link>

          {/* Trust Badges */}
          <div className="flex flex-wrap items-center justify-center gap-3">
            {badges.map((badge) => (
              <span
                key={badge}
                className="cta-badge inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 font-inter text-xs font-medium"
                style={{
                  backgroundColor: 'rgba(118,185,0,0.1)',
                  color: 'var(--envidia-green)',
                }}
              >
                <CheckCircle className="h-3 w-3" />
                {badge}
              </span>
            ))}
          </div>
        </div>

        {/* Greek key border bottom */}
        <div
          className="mt-12 h-4 w-full opacity-20"
          style={{
            backgroundImage: `repeating-linear-gradient(
              90deg,
              var(--deep-stone) 0px,
              var(--deep-stone) 8px,
              transparent 8px,
              transparent 16px
            )`,
          }}
        />
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════
   HOME PAGE — Compose all sections
   ═══════════════════════════════════════════ */
export default function Home() {
  return (
    <div>
      <HeroGateway />
      <TheMyth />
      <TheHeroes />
      <HowItWorks />
      <ImpactCounter />
      <GrowthPlan />
      <Partners />
      <CTASection />
    </div>
  );
}
