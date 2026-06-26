import { useRef, useCallback } from 'react';
import { Link } from 'react-router';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import {
  Feather,
  Megaphone,
  CreditCard,
  Shield,
  Target,
  Handshake,
  Brain,
  ChevronRight,
  ExternalLink,
  Github,
  BookOpen,
  ArrowRight,
  Zap,
  CheckCircle2,
} from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

/* ------------------------------------------------------------------ */
/*  DATA                                                               */
/* ------------------------------------------------------------------ */

interface HeroData {
  id: string;
  title: string;
  archetype: string;
  color: string;
  icon: string;
  lucideIcon: React.ElementType;
  description: string;
  archetypeDesc: string;
  skills: string[];
  tools: string[];
  connections: { name: string; icon: string; color: string }[];
  mcpConnections: string;
  missionExample: string;
  capabilities: { title: string; desc: string }[];
}

const heroes: HeroData[] = [
  {
    id: 'scribe',
    title: 'THE SCRIBE',
    archetype: 'Guardian of the Ledger',
    color: '#4A90A4',
    icon: '/hero-scribe-icon.png',
    lucideIcon: Feather,
    description:
      'Master of spreadsheets and financial clarity. The Scribe transforms chaos into structured insight, building dashboards that reveal the true financial health of your enterprise.',
    archetypeDesc:
      'The Scribe embodies the archetype of the meticulous record-keeper — the one who sees order in chaos and transforms raw data into strategic clarity. Every number tells a story, and The Scribe is the storyteller.',
    skills: [
      'Google Sheets',
      'Excel',
      'Dashboards',
      'Financial Analysis',
      'Cost Tracking',
      'Revenue Optimization',
    ],
    tools: [
      'Google Sheets',
      'Google Drive',
      '.finance Files',
      'Pivot Tables',
      'Query Functions',
      'Data Visualization',
      'Forecasting',
    ],
    connections: [
      { name: 'The Herald', icon: '/hero-herald-icon.png', color: '#9B59B6' },
      { name: 'The Collector', icon: '/hero-collector-icon.png', color: '#635BFF' },
      { name: 'The Brain', icon: '/hero-brain-icon.png', color: '#D4A853' },
    ],
    mcpConnections: 'Google Workspace MCP',
    missionExample:
      'A cafe owner needs to understand their true profitability. The Scribe receives their expense data, creates a .finance file categorizing all costs (rent, supplies, labor, marketing), builds a dashboard showing daily break-even point, and alerts when margins drop below target.',
    capabilities: [
      {
        title: 'Financial Modeling',
        desc: 'Builds complete financial models from scratch. Tracks fixed costs, variable costs, margins, and projections. Creates .finance files — standardized financial blueprints for any business type.',
      },
      {
        title: 'Dashboard Creation',
        desc: 'Designs real-time dashboards in Google Sheets that update automatically. Visual charts, KPI trackers, and executive summaries that evolve as your business grows.',
      },
      {
        title: 'Data Analysis',
        desc: 'Analyzes business data to identify trends, anomalies, and opportunities. From sales patterns to cost inefficiencies — The Scribe finds what others miss.',
      },
    ],
  },
  {
    id: 'herald',
    title: 'THE HERALD',
    archetype: 'Voice of the Brand',
    color: '#9B59B6',
    icon: '/hero-herald-icon.png',
    lucideIcon: Megaphone,
    description:
      'Expert in communication and brand strategy. The Herald crafts your message, manages your presence across all channels, and ensures your brand resonates with the right audience.',
    archetypeDesc:
      'The Herald is the voice of your brand — the communicator who ensures your message reaches the right people at the right time. Persuasive, creative, and relentlessly focused on growth.',
    skills: [
      'Social Media',
      'SEO',
      'Content Strategy',
      'Brand Identity',
      'Email Marketing',
      'Campaign Management',
    ],
    tools: [
      'Instagram',
      'Twitter',
      'LinkedIn',
      'Mailchimp',
      '.design Files',
      'SEO Tools',
      'Content Calendar',
    ],
    connections: [
      { name: 'The Scribe', icon: '/hero-scribe-icon.png', color: '#4A90A4' },
      { name: 'The Diplomat', icon: '/hero-diplomat-icon.png', color: '#E74C3C' },
      { name: 'The Brain', icon: '/hero-brain-icon.png', color: '#D4A853' },
    ],
    mcpConnections: 'Social Media APIs, Open Design',
    missionExample:
      'A construction company wants to attract more residential clients. The Herald interviews the founder to understand their unique value, creates a .design file capturing the brand essence, builds a 6-month content strategy with weekly social posts, and launches a targeted local SEO campaign.',
    capabilities: [
      {
        title: 'Brand Strategy',
        desc: 'Develops complete brand identities — voice, tone, visual guidelines, messaging frameworks. Creates .design files that serve as the brand bible for all other heroes.',
      },
      {
        title: 'Social Media Management',
        desc: 'Plans, creates, and schedules content across all platforms. Monitors engagement, responds to trends, and builds community — all aligned with your brand strategy.',
      },
      {
        title: 'SEO & GEO',
        desc: 'Optimizes for both traditional search (SEO) and generative engine optimization (GEO). Ensures your business is found whether customers search on Google or ask AI assistants.',
      },
      {
        title: 'Campaign Management',
        desc: 'Designs and executes marketing campaigns — from product launches to seasonal promotions. Tracks ROI, A/B tests messaging, and scales what works.',
      },
      {
        title: 'Content Calendar',
        desc: 'Maintains a living content calendar that coordinates all marketing activities. Ensures no opportunity is missed and no message conflicts.',
      },
      {
        title: 'Client Presentations',
        desc: 'Creates pitch decks, proposals, and presentations that win business. Professional, on-brand, and persuasive.',
      },
    ],
  },
  {
    id: 'collector',
    title: 'THE COLLECTOR',
    archetype: 'Keeper of Payments',
    color: '#635BFF',
    icon: '/hero-collector-icon.png',
    lucideIcon: CreditCard,
    description:
      'Payment processing expert with deep Stripe integration. The Collector ensures every transaction flows smoothly, from subscription management to invoice processing.',
    archetypeDesc:
      'The Collector is the financial gatekeeper — ensuring every transaction is processed, every invoice is sent, and every dollar is accounted for. Built on Stripe, trusted by businesses worldwide.',
    skills: [
      'Stripe Integration',
      'Payment Processing',
      'Invoicing',
      'Subscription Management',
      'Financial APIs',
    ],
    tools: [
      'Stripe API',
      'Stripe Dashboard',
      'Payment Links',
      'Checkout',
      'Billing',
      'Invoicing',
      'Connect',
    ],
    connections: [
      { name: 'The Scribe', icon: '/hero-scribe-icon.png', color: '#4A90A4' },
      { name: 'The Strategist', icon: '/hero-strategist-icon.png', color: '#FFB800' },
      { name: 'The Brain', icon: '/hero-brain-icon.png', color: '#D4A853' },
    ],
    mcpConnections: 'Stripe MCP',
    missionExample:
      'A coworking space sells day passes, monthly memberships, and meeting room bookings. The Collector sets up Stripe Checkout for each product type, configures subscription billing for memberships, creates an automated invoicing system for corporate clients, and builds a revenue dashboard.',
    capabilities: [
      {
        title: 'Payment Processing',
        desc: 'Handles all Stripe payment flows — one-time purchases, subscriptions, installments. Configures payment methods, currencies, and checkout experiences.',
      },
      {
        title: 'Invoicing',
        desc: 'Generates and sends professional invoices automatically. Tracks payment status, sends reminders, and reconciles received payments.',
      },
      {
        title: 'Subscription Management',
        desc: 'Manages recurring billing, plan changes, prorations, and cancellations. Handles free trials, upgrades, and downgrades seamlessly.',
      },
      {
        title: 'Revenue Tracking',
        desc: 'Real-time revenue dashboards connected to your Stripe account. MRR, ARR, churn rate, LTV — all tracked and reported.',
      },
      {
        title: 'Financial Reconciliation',
        desc: 'Reconciles Stripe transactions with your accounting system. Catches discrepancies and ensures your books are always accurate.',
      },
      {
        title: 'Fraud Monitoring',
        desc: 'Monitors transactions for suspicious patterns. Alerts on unusual activity and implements Stripe fraud prevention tools.',
      },
    ],
  },
  {
    id: 'guardian',
    title: 'THE GUARDIAN',
    archetype: 'Protector of the Realm',
    color: '#76B900',
    icon: '/hero-guardian-icon.png',
    lucideIcon: Shield,
    description:
      'Security specialist powered by Envidia. The Guardian manages API keys, model access, and security protocols — ensuring your AI infrastructure remains protected and compliant.',
    archetypeDesc:
      'The Guardian protects your digital realm. From API keys to model access, from security protocols to system integrity — nothing enters or leaves The Partenon without The Guardian watch.',
    skills: [
      'API Key Management',
      'Model Administration',
      'Security Protocols',
      'Access Control',
      'Envidia Integration',
    ],
    tools: [
      'Envidia Platform',
      'API Key Manager',
      'Security Dashboard',
      'Encryption',
      'Access Control',
      'MCP Security',
      'Audit Logs',
    ],
    connections: [
      { name: 'All Heroes', icon: '', color: '#76B900' },
      { name: 'The Brain', icon: '/hero-brain-icon.png', color: '#D4A853' },
    ],
    mcpConnections: 'Envidia MCP',
    missionExample:
      'A marketing agency uses multiple AI models and has API keys for five different platforms. The Guardian creates a secure vault for all credentials, sets up role-based access so each hero only sees what it needs, configures Envidia for optimal inference costs, and establishes audit logging.',
    capabilities: [
      {
        title: 'API Key Management',
        desc: 'Securely stores and manages all API keys — Envidia, OpenAI, social platforms, and custom integrations. Rotates keys, monitors usage, and prevents exposure.',
      },
      {
        title: 'Model Administration',
        desc: 'Manages access to AI models across the system. Configures which heroes use which models, optimizes for cost and performance, and tracks token usage.',
      },
      {
        title: 'Security Protocols',
        desc: 'Implements security best practices — encryption, access control, audit logging. Ensures The Partenon meets enterprise security standards.',
      },
      {
        title: 'Envidia Integration',
        desc: 'Manages Envidia API connections, GPU allocation for model inference, and security configurations specific to Envidia services.',
      },
      {
        title: 'Access Control',
        desc: 'Defines permissions for each hero and user. Role-based access ensures heroes can only reach the data and tools they need.',
      },
      {
        title: 'Audit & Compliance',
        desc: 'Maintains logs of all actions across The Partenon. Generates compliance reports and identifies security anomalies.',
      },
    ],
  },
  {
    id: 'strategist',
    title: 'THE STRATEGIST',
    archetype: 'Master of Operations',
    color: '#FFB800',
    icon: '/hero-strategist-icon.png',
    lucideIcon: Target,
    description:
      'Operational genius and project management expert. The Strategist keeps everything organized, manages calendars, tracks details, and ensures nothing falls through the cracks.',
    archetypeDesc:
      'The Strategist is the operational mind — the one who sees the big picture while tracking every detail. Project manager, calendar wizard, and the hero who ensures nothing falls through the cracks.',
    skills: [
      'Project Management',
      'Calendar Optimization',
      'Task Delegation',
      'Detail Tracking',
      'Process Optimization',
    ],
    tools: [
      'Google Calendar',
      'Google Tasks',
      'Notion',
      'Project Management Suite',
      'Email',
      'Notes',
      'Reminders',
    ],
    connections: [
      { name: 'All Heroes', icon: '', color: '#FFB800' },
      { name: 'The Diplomat', icon: '/hero-diplomat-icon.png', color: '#E74C3C' },
      { name: 'The Collector', icon: '/hero-collector-icon.png', color: '#635BFF' },
    ],
    mcpConnections: 'Google Workspace MCP, Calendar MCP',
    missionExample:
      'A design agency juggles 12 client projects simultaneously. The Strategist creates a master project timeline in Google Calendar, assigns weekly tasks to each hero, sends daily briefings to the founder, and flags when a project is at risk of missing its deadline.',
    capabilities: [
      {
        title: 'Project Management',
        desc: 'Orchestrates complex projects across multiple heroes. Creates timelines, assigns tasks, tracks progress, and ensures deadlines are met.',
      },
      {
        title: 'Calendar Management',
        desc: 'Manages Google Calendar for the entire team — scheduling meetings, blocking focus time, coordinating across time zones, and sending reminders.',
      },
      {
        title: 'Task Orchestration',
        desc: 'Breaks down high-level goals into actionable tasks, assigns them to the right heroes, and monitors completion. The central coordination hub.',
      },
      {
        title: 'Email Management',
        desc: 'Organizes inbox, drafts responses, flags priorities, and ensures important communications are never missed.',
      },
      {
        title: 'Operations Oversight',
        desc: 'Monitors the health of all business operations. Identifies bottlenecks, suggests process improvements, and maintains operational standards.',
      },
      {
        title: 'Note & Detail Tracking',
        desc: 'Remembers the details that matter — client preferences, project nuances, follow-up items. Ask "What did we discuss with Client X?" and The Strategist knows.',
      },
    ],
  },
  {
    id: 'diplomat',
    title: 'THE DIPLOMAT',
    archetype: 'Bridge Between Worlds',
    color: '#E74C3C',
    icon: '/hero-diplomat-icon.png',
    lucideIcon: Handshake,
    description:
      'Like the Gemini knight with two sides. The Diplomat balances client satisfaction with operational reality, managing relationships and ensuring smooth communication between all parties.',
    archetypeDesc:
      'The Diplomat has two faces — one for your clients, one for your team — and both are committed to harmony. The bridge between worlds who ensures everyone is heard, aligned, and moving forward together.',
    skills: [
      'Client Relations',
      'Vendor Management',
      'Negotiation',
      'CRM',
      'Follow-up Systems',
      'Conflict Resolution',
    ],
    tools: [
      'CRM Systems',
      'Email',
      'Calendar',
      'Meeting Notes',
      'Follow-up System',
      'Communication Log',
    ],
    connections: [
      { name: 'The Herald', icon: '/hero-herald-icon.png', color: '#9B59B6' },
      { name: 'The Strategist', icon: '/hero-strategist-icon.png', color: '#FFB800' },
      { name: 'The Scribe', icon: '/hero-scribe-icon.png', color: '#4A90A4' },
    ],
    mcpConnections: 'CRM MCP, Email MCP',
    missionExample:
      'A software development firm has unhappy clients because the sales team promised features the dev team cannot deliver on time. The Diplomat reviews all active client communications, schedules alignment meetings, creates a transparent client communication plan, and implements a promise tracker.',
    capabilities: [
      {
        title: 'Client Relationship Management',
        desc: 'Maintains detailed client profiles, tracks all interactions, manages follow-ups, and ensures no client feels forgotten.',
      },
      {
        title: 'Vendor Coordination',
        desc: 'Manages relationships with suppliers, contractors, and service providers. Tracks deliverables, handles disputes, and maintains vendor scorecards.',
      },
      {
        title: 'Communication Bridge',
        desc: 'Translates between internal teams and external stakeholders. Ensures client expectations align with operational capabilities.',
      },
      {
        title: 'Meeting Facilitation',
        desc: 'Prepares agendas, takes notes, assigns action items, and follows up after every meeting — internal or external.',
      },
      {
        title: 'Conflict Resolution',
        desc: 'Identifies misalignments between client needs and team capacity. Proposes solutions that satisfy both sides.',
      },
      {
        title: 'Partnership Management',
        desc: 'Manages strategic partnerships and collaborations. Tracks partnership health and identifies expansion opportunities.',
      },
    ],
  },
  {
    id: 'brain',
    title: 'THE BRAIN',
    archetype: 'G-Brain Orchestrator',
    color: '#D4A853',
    icon: '/hero-brain-icon.png',
    lucideIcon: Brain,
    description:
      'The central intelligence. The Brain connects all heroes through MCP protocols, enabling seamless data flow and coordinated action across the entire Parthenon system.',
    archetypeDesc:
      'The Brain is the central intelligence of The Partenon — the connective tissue that transforms individual hero capabilities into a unified, self-improving system. Through MCP, The Brain gives every hero access to shared knowledge, cross-domain insights, and collective intelligence.',
    skills: [
      'MCP Protocol Management',
      'Data Orchestration',
      'Cross-Agent Communication',
      'System Integration',
      'AI Model Coordination',
    ],
    tools: [
      'G-Brain Platform',
      'MCP Hub',
      'Model Router',
      'Google Workspace',
      'Stripe API',
      'Envidia APIs',
      'Social Media APIs',
      'CRM Systems',
    ],
    connections: [
      { name: 'All Heroes', icon: '', color: '#D4A853' },
    ],
    mcpConnections: 'All MCPs (Google Workspace, Stripe, Envidia, Social Media, CRM)',
    missionExample:
      'The Brain analyzes performance across all heroes — campaign ROI, conversion rates, operational efficiency — and generates optimization recommendations that no single hero could discover alone.',
    capabilities: [
      {
        title: 'Cross-Agent Analysis',
        desc: 'Analyzes data from all heroes simultaneously. Identifies patterns that no single hero could see — like marketing spend correlating with payment delays.',
      },
      {
        title: 'Pattern Recognition',
        desc: 'Learns from every interaction, every mission, every outcome. Recognizes recurring business patterns and suggests proactive optimizations.',
      },
      {
        title: 'MCP Orchestration',
        desc: 'Manages the Model Context Protocol layer that connects all heroes to shared tools, data sources, and external APIs. Ensures seamless interoperability.',
      },
      {
        title: 'Strategic Insights',
        desc: 'Generates executive-level insights and recommendations. Not just data — but actionable intelligence that helps founders make better decisions.',
      },
    ],
  },
];

const comparisonData = [
  {
    hero: 'The Scribe',
    color: '#4A90A4',
    role: 'Financial Architect',
    tools: 'Google Sheets, .finance',
    worksWith: 'Herald, Collector, Brain',
    bestFor: 'Businesses needing financial clarity',
  },
  {
    hero: 'The Herald',
    color: '#9B59B6',
    role: 'Brand Communicator',
    tools: 'Social APIs, .design',
    worksWith: 'Scribe, Diplomat, Brain',
    bestFor: 'Building brand presence & growth',
  },
  {
    hero: 'The Collector',
    color: '#635BFF',
    role: 'Payment Guardian',
    tools: 'Stripe API',
    worksWith: 'Scribe, Strategist, Brain',
    bestFor: 'Processing payments & revenue tracking',
  },
  {
    hero: 'The Guardian',
    color: '#76B900',
    role: 'Security Sentinel',
    tools: 'Envidia APIs, MCP Security',
    worksWith: 'All Heroes, Brain',
    bestFor: 'Securing systems & managing AI models',
  },
  {
    hero: 'The Strategist',
    color: '#FFB800',
    role: 'Operations Master',
    tools: 'Google Calendar, PM',
    worksWith: 'All Heroes, Diplomat',
    bestFor: 'Project management & coordination',
  },
  {
    hero: 'The Diplomat',
    color: '#E74C3C',
    role: 'Relations Bridge',
    tools: 'CRM, Email',
    worksWith: 'Herald, Strategist, Brain',
    bestFor: 'Client & vendor relationship management',
  },
  {
    hero: 'The Brain',
    color: '#D4A853',
    role: 'Central Intelligence',
    tools: 'MCP Protocol',
    worksWith: 'All Heroes',
    bestFor: 'Cross-agent analysis & optimization',
  },
];

const workflowSteps = [
  {
    hero: 'The Strategist',
    color: '#FFB800',
    icon: '/hero-strategist-icon.png',
    title: 'Product Launch Project Created',
    body: 'The Strategist creates a project timeline, assigns deadlines, and schedules kickoff meetings with all relevant heroes.',
    output: 'Google Calendar events, task assignments',
  },
  {
    hero: 'The Scribe',
    color: '#4A90A4',
    icon: '/hero-scribe-icon.png',
    title: 'Financial Model & Pricing Built',
    body: 'The Scribe creates a .finance file with product cost analysis, pricing tiers, and revenue projections.',
    output: '.finance file, pricing dashboard',
  },
  {
    hero: 'The Herald',
    color: '#9B59B6',
    icon: '/hero-herald-icon.png',
    title: 'Marketing Campaign Designed',
    body: 'The Herald references the .design file, creates campaign assets, schedules social content, and sets up SEO.',
    output: 'Content calendar, ad campaigns, social posts',
  },
  {
    hero: 'The Collector',
    color: '#635BFF',
    icon: '/hero-collector-icon.png',
    title: 'Stripe Products & Checkout Live',
    body: 'The Collector sets up product listings in Stripe, configures checkout flows, and tests the complete purchase journey.',
    output: 'Live payment processing',
  },
  {
    hero: 'The Diplomat',
    color: '#E74C3C',
    icon: '/hero-diplomat-icon.png',
    title: 'Client Outreach & Follow-ups',
    body: 'The Diplomat reaches out to existing clients about the new product, schedules demos, and tracks conversations.',
    output: 'CRM updates, meeting bookings',
  },
  {
    hero: 'The Guardian',
    color: '#76B900',
    icon: '/hero-guardian-icon.png',
    title: 'Security & Access Verified',
    body: 'The Guardian audits all new integrations, verifies API security, and ensures the launch meets security standards.',
    output: 'Security report, access logs',
  },
  {
    hero: 'The Brain',
    color: '#D4A853',
    icon: '/hero-brain-icon.png',
    title: 'Cross-Agent Analysis & Insights',
    body: 'The Brain analyzes performance across all heroes — campaign ROI, conversion rates, operational efficiency.',
    output: 'Strategic insights report',
  },
];

/* ------------------------------------------------------------------ */
/*  FLOATING ICON (micro-component, isolated animation)                */
/* ------------------------------------------------------------------ */

import { memo } from 'react';

const FloatingHeroIcon = memo(function FloatingHeroIcon({
  hero,
  index,
}: {
  hero: HeroData;
  index: number;
}) {
  return (
    <a
      href={`#${hero.id}`}
      className="group relative flex-shrink-0"
      style={{ animationDelay: `${index * 0.15}s` }}
    >
      <div
        className="w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 group-hover:scale-110"
        style={{
          backgroundColor: `${hero.color}20`,
          border: `2px solid ${hero.color}40`,
        }}
      >
        <img
          src={hero.icon}
          alt={hero.title}
          className="w-6 h-6 object-contain opacity-60 group-hover:opacity-100 transition-opacity duration-300"
        />
      </div>
      <span
        className="absolute -bottom-6 left-1/2 -translate-x-1/2 text-[0.625rem] font-medium tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap"
        style={{ color: hero.color }}
      >
        {hero.title.replace('THE ', '')}
      </span>
    </a>
  );
});

/* ------------------------------------------------------------------ */
/*  MAIN COMPONENT                                                     */
/* ------------------------------------------------------------------ */

export default function Heroes() {
  const containerRef = useRef<HTMLDivElement>(null);
  const heroRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);
  const matrixRef = useRef<HTMLDivElement>(null);
  const workflowRef = useRef<HTMLDivElement>(null);
  const ctaRef = useRef<HTMLDivElement>(null);

  /* Smooth scroll to section */
  const scrollToHero = useCallback((id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, []);

  useGSAP(
    () => {
      if (!containerRef.current) return;

      /* ---- Hero entrance animations ---- */
      const heroTl = gsap.timeline({ delay: 0.3 });

      heroTl.fromTo(
        '.heroes-hero-eyebrow',
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }
      );
      heroTl.fromTo(
        '.heroes-hero-headline span',
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.04,
          ease: 'power3.out',
        },
        '-=0.3'
      );
      heroTl.fromTo(
        '.heroes-hero-subtitle',
        { opacity: 0, y: 30 },
        { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' },
        '-=0.4'
      );
      heroTl.fromTo(
        '.heroes-hero-divider',
        { scaleX: 0 },
        { scaleX: 1, duration: 0.6, ease: 'power3.out' },
        '-=0.5'
      );
      heroTl.fromTo(
        '.heroes-quick-nav a',
        { opacity: 0, scale: 0.5 },
        {
          opacity: 1,
          scale: 1,
          duration: 0.5,
          stagger: 0.08,
          ease: 'back.out(1.7)',
        },
        '-=0.3'
      );

      /* ---- Card entrance animations ---- */
      const cardSections = gsap.utils.toArray<HTMLElement>('.hero-card-section');
      cardSections.forEach((section) => {
        const illus = section.querySelector('.hero-illustration');
        const content = section.querySelector('.hero-content-blocks');
        const caps = section.querySelectorAll('.capability-card');
        const tools = section.querySelectorAll('.tool-badge');

        if (illus) {
          gsap.fromTo(
            illus,
            { opacity: 0, x: -40 },
            {
              opacity: 1,
              x: 0,
              duration: 0.8,
              ease: 'power3.out',
              scrollTrigger: {
                trigger: section,
                start: 'top 80%',
                toggleActions: 'play none none none',
              },
            }
          );
        }

        if (content) {
          gsap.fromTo(
            content.children,
            { opacity: 0, y: 30 },
            {
              opacity: 1,
              y: 0,
              duration: 0.6,
              stagger: 0.1,
              ease: 'power3.out',
              scrollTrigger: {
                trigger: section,
                start: 'top 75%',
                toggleActions: 'play none none none',
              },
            }
          );
        }

        if (caps.length) {
          gsap.fromTo(
            caps,
            { opacity: 0, y: 20, scale: 0.95 },
            {
              opacity: 1,
              y: 0,
              scale: 1,
              duration: 0.5,
              stagger: 0.08,
              ease: 'back.out(1.4)',
              scrollTrigger: {
                trigger: section,
                start: 'top 65%',
                toggleActions: 'play none none none',
              },
            }
          );
        }

        if (tools.length) {
          gsap.fromTo(
            tools,
            { opacity: 0, x: -10 },
            {
              opacity: 1,
              x: 0,
              duration: 0.4,
              stagger: 0.05,
              ease: 'power3.out',
              scrollTrigger: {
                trigger: section,
                start: 'top 60%',
                toggleActions: 'play none none none',
              },
            }
          );
        }
      });

      /* ---- Brain section special animation ---- */
      const brainSection = document.querySelector('.brain-special-section');
      if (brainSection) {
        gsap.fromTo(
          brainSection.querySelectorAll('.brain-animate'),
          { opacity: 0, y: 30 },
          {
            opacity: 1,
            y: 0,
            duration: 0.7,
            stagger: 0.12,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: brainSection,
              start: 'top 75%',
              toggleActions: 'play none none none',
            },
          }
        );
        gsap.fromTo(
          brainSection.querySelectorAll('.brain-cap-card'),
          { opacity: 0, y: 25 },
          {
            opacity: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.1,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: brainSection,
              start: 'top 60%',
              toggleActions: 'play none none none',
            },
          }
        );
      }

      /* ---- Comparison matrix ---- */
      if (matrixRef.current) {
        gsap.fromTo(
          '.matrix-header',
          { opacity: 0, y: 20 },
          {
            opacity: 1,
            y: 0,
            duration: 0.6,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: matrixRef.current,
              start: 'top 80%',
              toggleActions: 'play none none none',
            },
          }
        );
        gsap.fromTo(
          '.matrix-row',
          { opacity: 0, x: -20 },
          {
            opacity: 1,
            x: 0,
            duration: 0.5,
            stagger: 0.06,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: matrixRef.current,
              start: 'top 70%',
              toggleActions: 'play none none none',
            },
          }
        );
      }

      /* ---- Workflow timeline ---- */
      if (workflowRef.current) {
        gsap.fromTo(
          '.workflow-step',
          { opacity: 0, x: -30 },
          {
            opacity: 1,
            x: 0,
            duration: 0.6,
            stagger: 0.12,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: workflowRef.current,
              start: 'top 75%',
              toggleActions: 'play none none none',
            },
          }
        );
        gsap.fromTo(
          '.workflow-line',
          { scaleY: 0 },
          {
            scaleY: 1,
            duration: 1.5,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: workflowRef.current,
              start: 'top 70%',
              toggleActions: 'play none none none',
            },
          }
        );
      }

      /* ---- CTA section ---- */
      if (ctaRef.current) {
        gsap.fromTo(
          '.cta-headline span',
          { opacity: 0, y: 40 },
          {
            opacity: 1,
            y: 0,
            duration: 0.8,
            stagger: 0.08,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: ctaRef.current,
              start: 'top 80%',
              toggleActions: 'play none none none',
            },
          }
        );
        gsap.fromTo(
          '.cta-button',
          { opacity: 0, y: 20 },
          {
            opacity: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.15,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: ctaRef.current,
              start: 'top 70%',
              toggleActions: 'play none none none',
            },
          }
        );
      }
    },
    { scope: containerRef }
  );

  return (
    <div ref={containerRef}>
      {/* ============================================================ */}
      {/* SECTION 1 — HERO                                             */}
      {/* ============================================================ */}
      <section
        ref={heroRef}
        data-dark-section
        className="relative w-full overflow-hidden"
        style={{
          minHeight: '70vh',
          backgroundColor: '#2A2A2E',
        }}
      >
        {/* Particle network canvas placeholder */}
        <div className="absolute inset-0 opacity-20">
          <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern
                id="hero-grid"
                width="60"
                height="60"
                patternUnits="userSpaceOnUse"
              >
                <circle cx="30" cy="30" r="1.5" fill="#D4A853" opacity="0.5" />
                <line
                  x1="30"
                  y1="30"
                  x2="90"
                  y2="30"
                  stroke="#D4A853"
                  strokeWidth="0.5"
                  opacity="0.2"
                />
                <line
                  x1="30"
                  y1="30"
                  x2="30"
                  y2="90"
                  stroke="#D4A853"
                  strokeWidth="0.5"
                  opacity="0.2"
                />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#hero-grid)" />
          </svg>
        </div>

        <div
          className="relative z-10 mx-auto px-6 flex flex-col items-center justify-center text-center"
          style={{
            maxWidth: 'var(--container-narrow)',
            minHeight: '70vh',
            paddingTop: '120px',
            paddingBottom: '4rem',
          }}
        >
          {/* Eyebrow */}
          <span
            className="heroes-hero-eyebrow inline-block text-xs font-semibold tracking-[0.16em] mb-6"
            style={{ color: '#FFB800' }}
          >
            THE ASSEMBLY
          </span>

          {/* Headline */}
          <h1
            className="heroes-hero-headline font-cinzel text-[clamp(2.5rem,6vw,5rem)] font-normal leading-[1.05] tracking-[0.06em] mb-6"
            style={{ color: '#F7F5F0' }}
          >
            {'MEET YOUR HEROES'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">
                {word}
              </span>
            ))}
          </h1>

          {/* Divider */}
          <div
            className="heroes-hero-divider w-12 h-0.5 mb-6"
            style={{
              backgroundColor: '#FFB800',
              transformOrigin: 'center',
            }}
          />

          {/* Subtitle */}
          <p
            className="heroes-hero-subtitle text-base md:text-lg leading-relaxed mb-10 max-w-[640px]"
            style={{ color: 'rgba(247,245,240,0.6)' }}
          >
            Seven specialized agents. One unified purpose. Each hero brings a
            unique archetype, skillset, and personality to your enterprise —
            working together through The Partenon to transform how you operate.
          </p>

          {/* Quick-nav icons */}
          <div className="heroes-quick-nav flex items-center justify-center gap-4 md:gap-5 flex-wrap">
            {heroes.map((hero, i) => (
              <FloatingHeroIcon key={hero.id} hero={hero} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* SECTION 2 — HERO DETAIL CARDS (7)                            */}
      {/* ============================================================ */}
      <div ref={cardsRef}>
        {heroes.map((hero, index) => {
          const isReversed = index % 2 !== 0;
          const bgColor = index % 2 === 0 ? '#F7F5F0' : '#EDE8DF';
          const isBrain = hero.id === 'brain';

          return (
            <section
              key={hero.id}
              id={hero.id}
              className={`hero-card-section w-full ${isBrain ? 'brain-special-section' : ''}`}
              style={{
                backgroundColor: bgColor,
                padding: '5rem 0',
              }}
            >
              <div
                className="mx-auto px-6"
                style={{ maxWidth: 'var(--container-max)' }}
              >
                {isBrain ? (
                  /* ---- Brain: centered single-column layout ---- */
                  <div className="flex flex-col items-center text-center max-w-[800px] mx-auto">
                    {/* Brain icon */}
                    <div
                      className="brain-animate w-40 h-40 md:w-56 md:h-56 rounded-full flex items-center justify-center mb-8"
                      style={{
                        background: `radial-gradient(circle, ${hero.color}15 0%, transparent 70%)`,
                      }}
                    >
                      <img
                        src={hero.icon}
                        alt={hero.title}
                        className="w-32 h-32 md:w-44 md:h-44 object-contain"
                      />
                    </div>

                    {/* Eyebrow */}
                    <span
                      className="brain-animate text-xs font-semibold tracking-[0.16em] mb-3"
                      style={{ color: hero.color }}
                    >
                      CENTRAL INTELLIGENCE
                    </span>

                    {/* Name */}
                    <h2
                      className="brain-animate font-cinzel text-[clamp(2rem,4vw,3.5rem)] font-normal tracking-[0.06em] mb-2"
                      style={{ color: '#2A2A2E' }}
                    >
                      {hero.title}
                    </h2>

                    {/* Subtitle */}
                    <h3
                      className="brain-animate font-cinzel text-[clamp(1.2rem,2vw,1.75rem)] tracking-[0.04em] mb-4"
                      style={{ color: hero.color }}
                    >
                      G-BRAIN OF GARITAN
                    </h3>

                    {/* Divider */}
                    <div
                      className="brain-animate w-16 h-0.5 mb-6"
                      style={{ backgroundColor: hero.color }}
                    />

                    {/* Description */}
                    <p
                      className="brain-animate text-base leading-relaxed mb-10 max-w-[640px]"
                      style={{ color: '#6B6B73' }}
                    >
                      {hero.archetypeDesc}
                    </p>

                    {/* Capabilities grid 2x2 */}
                    <div className="brain-animate grid grid-cols-1 sm:grid-cols-2 gap-4 w-full mb-10">
                      {hero.capabilities.map((cap) => (
                        <div
                          key={cap.title}
                          className="brain-cap-card p-5 rounded-lg text-left"
                          style={{
                            backgroundColor: '#F7F5F0',
                            border: `1px solid ${hero.color}20`,
                            boxShadow: '0 2px 8px rgba(42,42,46,0.04)',
                          }}
                        >
                          <h4
                            className="font-inter text-sm font-semibold mb-2"
                            style={{ color: hero.color }}
                          >
                            {cap.title}
                          </h4>
                          <p
                            className="text-sm leading-relaxed"
                            style={{ color: '#6B6B73' }}
                          >
                            {cap.desc}
                          </p>
                        </div>
                      ))}
                    </div>

                    {/* MCP Badge */}
                    <div
                      className="brain-animate inline-flex items-center gap-2 rounded-full px-5 py-2.5 mb-4"
                      style={{
                        backgroundColor: hero.color,
                        color: '#2A2A2E',
                      }}
                    >
                      <Zap className="w-4 h-4" />
                      <span className="text-sm font-semibold tracking-wide">
                        MCP POWERED
                      </span>
                    </div>
                    <p
                      className="brain-animate text-sm leading-relaxed max-w-[500px]"
                      style={{ color: '#6B6B73' }}
                    >
                      Model Context Protocol enables The Brain to connect every
                      hero to shared context, tools, and memory — creating a true
                      collective intelligence.
                    </p>
                  </div>
                ) : (
                  /* ---- Standard two-column layout ---- */
                  <div
                    className={`flex flex-col ${isReversed ? 'lg:flex-row-reverse' : 'lg:flex-row'} gap-12 lg:gap-16 items-start`}
                  >
                    {/* Left Column — Illustration */}
                    <div className="hero-illustration w-full lg:w-[35%] flex flex-col items-center text-center">
                      <div
                        className="w-64 h-64 md:w-80 md:h-80 rounded-full flex items-center justify-center mb-6"
                        style={{
                          backgroundColor: `${hero.color}10`,
                        }}
                      >
                        <img
                          src={hero.icon}
                          alt={hero.title}
                          className="w-52 h-52 md:w-64 md:h-64 object-contain"
                        />
                      </div>
                      <h3
                        className="font-cinzel text-xl md:text-2xl tracking-[0.04em] mb-2"
                        style={{ color: hero.color }}
                      >
                        {hero.title}
                      </h3>
                      <p
                        className="text-sm"
                        style={{ color: '#6B6B73' }}
                      >
                        {hero.archetype}
                      </p>
                    </div>

                    {/* Right Column — Content */}
                    <div className="hero-content-blocks w-full lg:w-[65%]">
                      {/* Eyebrow */}
                      <span
                        className="text-xs font-semibold tracking-[0.12em] mb-2 block"
                        style={{ color: hero.color }}
                      >
                        HERO PROFILE
                      </span>

                      {/* Name */}
                      <h2
                        className="font-cinzel text-[clamp(1.75rem,3.5vw,3rem)] font-normal tracking-[0.06em] mb-3"
                        style={{ color: '#2A2A2E' }}
                      >
                        {hero.title}
                      </h2>

                      {/* Divider */}
                      <div
                        className="w-12 h-0.5 mb-5"
                        style={{ backgroundColor: hero.color }}
                      />

                      {/* Archetype Description */}
                      <p
                        className="text-base leading-relaxed mb-8"
                        style={{ color: '#6B6B73' }}
                      >
                        {hero.archetypeDesc}
                      </p>

                      {/* Capabilities Grid */}
                      <div
                        className={`grid grid-cols-1 ${hero.capabilities.length >= 4 ? 'sm:grid-cols-2' : 'sm:grid-cols-3'} gap-4 mb-8`}
                      >
                        {hero.capabilities.map((cap) => (
                          <div
                            key={cap.title}
                            className="capability-card p-4 rounded-lg"
                            style={{
                              backgroundColor:
                                index % 2 === 0 ? '#EDE8DF' : '#F7F5F0',
                              border: `1px solid ${hero.color}15`,
                              boxShadow: '0 2px 8px rgba(42,42,46,0.04)',
                            }}
                          >
                            <h4
                              className="font-inter text-sm font-semibold mb-1.5"
                              style={{ color: hero.color }}
                            >
                              {cap.title}
                            </h4>
                            <p
                              className="text-sm leading-relaxed"
                              style={{ color: '#6B6B73' }}
                            >
                              {cap.desc}
                            </p>
                          </div>
                        ))}
                      </div>

                      {/* Tools Row */}
                      <div className="mb-8">
                        <span
                          className="text-xs font-semibold tracking-[0.12em] mb-3 block"
                          style={{ color: '#6B6B73' }}
                        >
                          TOOLS
                        </span>
                        <div className="flex flex-wrap gap-2">
                          {hero.tools.map((tool) => (
                            <span
                              key={tool}
                              className="tool-badge inline-flex items-center px-3 py-1 rounded-full text-xs font-mono"
                              style={{
                                border: `1px solid ${hero.color}40`,
                                color: hero.color,
                                backgroundColor: `${hero.color}08`,
                              }}
                            >
                              {tool}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Connections */}
                      <div className="mb-8">
                        <span
                          className="text-xs font-semibold tracking-[0.12em] mb-3 block"
                          style={{ color: '#6B6B73' }}
                        >
                          WORKS CLOSELY WITH
                        </span>
                        <div className="flex items-center gap-4">
                          {hero.connections.map((conn) => (
                            <div key={conn.name} className="flex items-center gap-2">
                              {conn.icon ? (
                                <img
                                  src={conn.icon}
                                  alt={conn.name}
                                  className="w-8 h-8 rounded-full object-cover"
                                  style={{
                                    border: `2px solid ${conn.color}40`,
                                  }}
                                />
                              ) : (
                                <div
                                  className="w-8 h-8 rounded-full flex items-center justify-center"
                                  style={{
                                    backgroundColor: `${conn.color}20`,
                                    border: `2px solid ${conn.color}40`,
                                  }}
                                >
                                  <span
                                    className="text-xs font-bold"
                                    style={{ color: conn.color }}
                                  >
                                    A
                                  </span>
                                </div>
                              )}
                              <span
                                className="text-sm"
                                style={{ color: '#6B6B73' }}
                              >
                                {conn.name}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* MCP Connection */}
                      <div className="mb-8">
                        <span
                          className="text-xs font-semibold tracking-[0.12em] mb-2 block"
                          style={{ color: '#6B6B73' }}
                        >
                          MCP CONNECTIONS
                        </span>
                        <span
                          className="inline-flex items-center gap-1.5 text-sm font-mono"
                          style={{ color: hero.color }}
                        >
                          <Zap className="w-3.5 h-3.5" />
                          {hero.mcpConnections}
                        </span>
                      </div>

                      {/* Example Mission */}
                      <blockquote
                        className="pl-6 py-1 border-l-[3px]"
                        style={{ borderLeftColor: hero.color }}
                      >
                        <p
                          className="text-sm italic leading-relaxed"
                          style={{ color: '#6B6B73' }}
                        >
                          {hero.missionExample}
                        </p>
                      </blockquote>
                    </div>
                  </div>
                )}
              </div>
            </section>
          );
        })}
      </div>

      {/* ============================================================ */}
      {/* SECTION 3 — COMPARISON MATRIX                                */}
      {/* ============================================================ */}
      <section
        ref={matrixRef}
        data-dark-section
        className="w-full"
        style={{
          backgroundColor: '#2A2A2E',
          padding: 'clamp(4rem, 8vh, 8rem) 0',
        }}
      >
        <div
          className="mx-auto px-6"
          style={{ maxWidth: 'var(--container-max)' }}
        >
          {/* Header */}
          <div className="matrix-header text-center mb-12">
            <span
              className="text-xs font-semibold tracking-[0.16em] mb-4 block"
              style={{ color: '#FFB800' }}
            >
              AT A GLANCE
            </span>
            <h2
              className="font-cinzel text-[clamp(1.75rem,4vw,3rem)] font-normal tracking-[0.06em] mb-4"
              style={{ color: '#F7F5F0' }}
            >
              THE COMPLETE ROSTER
            </h2>
            <p
              className="text-base"
              style={{ color: 'rgba(247,245,240,0.5)' }}
            >
              Quick reference for what each hero brings to your enterprise.
            </p>
          </div>

          {/* Table */}
          <div className="overflow-x-auto">
            <table className="w-full min-w-[700px]">
              <thead>
                <tr style={{ backgroundColor: '#1A1A1E' }}>
                  <th
                    className="text-left px-4 py-3 font-cinzel text-xs tracking-[0.08em]"
                    style={{ color: '#FFB800' }}
                  >
                    HERO
                  </th>
                  <th
                    className="text-left px-4 py-3 font-cinzel text-xs tracking-[0.08em]"
                    style={{ color: '#FFB800' }}
                  >
                    PRIMARY ROLE
                  </th>
                  <th
                    className="text-left px-4 py-3 font-cinzel text-xs tracking-[0.08em]"
                    style={{ color: '#FFB800' }}
                  >
                    KEY TOOLS
                  </th>
                  <th
                    className="text-left px-4 py-3 font-cinzel text-xs tracking-[0.08em]"
                    style={{ color: '#FFB800' }}
                  >
                    WORKS WITH
                  </th>
                  <th
                    className="text-left px-4 py-3 font-cinzel text-xs tracking-[0.08em]"
                    style={{ color: '#FFB800' }}
                  >
                    BEST FOR
                  </th>
                </tr>
              </thead>
              <tbody>
                {comparisonData.map((row) => (
                  <tr
                    key={row.hero}
                    className="matrix-row transition-colors duration-200 hover:bg-[rgba(212,168,83,0.08)]"
                    style={{
                      borderBottom: '1px solid rgba(247,245,240,0.06)',
                    }}
                  >
                    <td className="px-4 py-4">
                      <div className="flex items-center gap-3">
                        <div
                          className="w-1 h-8 rounded-full"
                          style={{ backgroundColor: row.color }}
                        />
                        <span
                          className="font-cinzel text-sm tracking-[0.04em]"
                          style={{ color: '#F7F5F0' }}
                        >
                          {row.hero}
                        </span>
                      </div>
                    </td>
                    <td
                      className="px-4 py-4 text-sm"
                      style={{ color: 'rgba(247,245,240,0.7)' }}
                    >
                      {row.role}
                    </td>
                    <td
                      className="px-4 py-4 text-sm font-mono"
                      style={{ color: 'rgba(247,245,240,0.7)' }}
                    >
                      {row.tools}
                    </td>
                    <td
                      className="px-4 py-4 text-sm"
                      style={{ color: 'rgba(247,245,240,0.7)' }}
                    >
                      {row.worksWith}
                    </td>
                    <td
                      className="px-4 py-4 text-sm"
                      style={{ color: 'rgba(247,245,240,0.7)' }}
                    >
                      {row.bestFor}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* SECTION 4 — INTERCONNECTED WORKFLOW                          */}
      {/* ============================================================ */}
      <section
        ref={workflowRef}
        className="w-full"
        style={{
          backgroundColor: '#EDE8DF',
          padding: 'clamp(4rem, 8vh, 8rem) 0',
        }}
      >
        <div
          className="mx-auto px-6"
          style={{ maxWidth: 'var(--container-max)' }}
        >
          {/* Header */}
          <div className="text-center mb-16">
            <h2
              className="font-cinzel text-[clamp(1.75rem,4vw,3rem)] font-normal tracking-[0.06em] mb-4"
              style={{ color: '#2A2A2E' }}
            >
              HOW HEROES WORK TOGETHER
            </h2>
            <p
              className="text-base max-w-[640px] mx-auto"
              style={{ color: '#6B6B73' }}
            >
              The real power of The Partenon is not individual heroes — it is how
              they collaborate. Here is a real-world example of heroes coordinating
              on a single business mission.
            </p>
          </div>

          {/* Mission Title */}
          <div className="text-center mb-12">
            <span
              className="inline-flex items-center gap-2 rounded-full px-5 py-2 text-sm font-semibold tracking-wide"
              style={{
                backgroundColor: '#635BFF',
                color: '#F7F5F0',
              }}
            >
              <Target className="w-4 h-4" />
              PRODUCT LAUNCH MISSION
            </span>
          </div>

          {/* Timeline */}
          <div className="relative max-w-[800px] mx-auto">
            {/* Vertical line */}
            <div
              className="workflow-line absolute left-6 md:left-8 top-0 bottom-0 w-0.5 origin-top"
              style={{
                background:
                  'linear-gradient(to bottom, #FFB800, #4A90A4, #9B59B6, #635BFF, #E74C3C, #76B900, #D4A853)',
              }}
            />

            {/* Steps */}
            <div className="space-y-8">
              {workflowSteps.map((step, i) => (
                <div
                  key={i}
                  className="workflow-step relative flex gap-4 md:gap-6 items-start pl-0"
                >
                  {/* Step icon */}
                  <div
                    className="relative z-10 w-12 h-12 md:w-16 md:h-16 rounded-full flex items-center justify-center flex-shrink-0"
                    style={{
                      backgroundColor: step.color,
                      boxShadow: `0 0 20px ${step.color}40`,
                    }}
                  >
                    <img
                      src={step.icon}
                      alt={step.hero}
                      className="w-8 h-8 md:w-10 md:h-10 object-contain"
                    />
                  </div>

                  {/* Step content card */}
                  <div
                    className="flex-1 p-5 md:p-6 rounded-lg"
                    style={{
                      backgroundColor: '#F7F5F0',
                      boxShadow: '0 2px 12px rgba(42,42,46,0.06)',
                      border: `1px solid ${step.color}15`,
                    }}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <span
                        className="text-xs font-semibold tracking-[0.12em]"
                        style={{ color: step.color }}
                      >
                        STEP {i + 1}
                      </span>
                      <span
                        className="text-xs"
                        style={{ color: '#6B6B73' }}
                      >
                        — {step.hero}
                      </span>
                    </div>
                    <h4
                      className="font-inter text-base font-semibold mb-2"
                      style={{ color: '#2A2A2E' }}
                    >
                      {step.title}
                    </h4>
                    <p
                      className="text-sm leading-relaxed mb-3"
                      style={{ color: '#6B6B73' }}
                    >
                      {step.body}
                    </p>
                    <div className="flex items-center gap-1.5">
                      <CheckCircle2
                        className="w-3.5 h-3.5 flex-shrink-0"
                        style={{ color: step.color }}
                      />
                      <span
                        className="text-xs font-mono"
                        style={{ color: step.color }}
                      >
                        {step.output}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ============================================================ */}
      {/* SECTION 5 — CTA                                              */}
      {/* ============================================================ */}
      <section
        ref={ctaRef}
        data-dark-section
        className="w-full"
        style={{
          backgroundColor: '#2A2A2E',
          padding: '5rem 0',
        }}
      >
        <div
          className="mx-auto px-6 text-center"
          style={{ maxWidth: 'var(--container-narrow)' }}
        >
          {/* Headline */}
          <h2
            className="cta-headline font-cinzel text-[clamp(2rem,5vw,3.5rem)] font-normal tracking-[0.06em] mb-4"
            style={{ color: '#F7F5F0' }}
          >
            {'ASSEMBLE YOUR HEROES'.split(' ').map((word, i) => (
              <span key={i} className="inline-block mr-[0.3em]">
                {word}
              </span>
            ))}
          </h2>

          {/* Subtitle */}
          <p
            className="text-base mb-8"
            style={{ color: 'rgba(247,245,240,0.6)' }}
          >
            Every hero is ready. Your Partenon awaits.
          </p>

          {/* Install command */}
          <div
            className="cta-button inline-flex items-center gap-3 rounded-lg px-6 py-3 mb-8 font-mono text-sm cursor-pointer transition-all duration-200 hover:scale-[1.02]"
            style={{
              backgroundColor: '#1A1A1E',
              color: '#F7F5F0',
              border: '1px solid rgba(247,245,240,0.15)',
            }}
            onClick={() => {
              navigator.clipboard.writeText('npx create-hermes@latest');
            }}
            title="Click to copy"
          >
            <span style={{ color: '#76B900' }}>$</span>
            <span>npx create-hermes@latest</span>
            <ExternalLink className="w-4 h-4 opacity-40" />
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            {/* Primary CTA */}
            <Link
              to="/developers"
              className="cta-button inline-flex items-center gap-2 rounded-full px-8 py-4 text-base font-semibold tracking-wide transition-all duration-200 hover:scale-[1.02]"
              style={{
                backgroundColor: '#635BFF',
                color: '#F7F5F0',
                borderRadius: 'var(--radius-pill)',
                boxShadow: '0 0 30px rgba(99,91,255,0.3)',
              }}
            >
              INSTALL HERMES NOW
              <ArrowRight className="w-5 h-5" />
            </Link>

            {/* Secondary CTA */}
            <Link
              to="/developers"
              className="cta-button inline-flex items-center gap-2 text-sm font-medium transition-colors duration-200 hover:text-[#635BFF]"
              style={{ color: 'rgba(247,245,240,0.6)' }}
            >
              Read Technical Documentation
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          {/* Quick nav links */}
          <div
            className="mt-10 pt-8 flex flex-wrap items-center justify-center gap-4"
            style={{ borderTop: '1px solid rgba(247,245,240,0.08)' }}
          >
            <span
              className="text-xs"
              style={{ color: 'rgba(247,245,240,0.3)' }}
            >
              Jump to:
            </span>
            {heroes.map((hero) => (
              <button
                key={hero.id}
                onClick={() => scrollToHero(hero.id)}
                className="text-xs font-medium transition-colors duration-200 hover:text-[#635BFF]"
                style={{ color: 'rgba(247,245,240,0.5)' }}
              >
                {hero.title}
              </button>
            ))}
          </div>

          {/* GitHub + Docs links */}
          <div className="mt-8 flex items-center justify-center gap-6">
            <a
              href="#"
              className="flex items-center gap-2 text-sm transition-colors duration-200 hover:text-[#635BFF]"
              style={{ color: 'rgba(247,245,240,0.5)' }}
              onClick={(e) => e.preventDefault()}
            >
              <Github className="w-4 h-4" />
              GitHub
            </a>
            <a
              href="#"
              className="flex items-center gap-2 text-sm transition-colors duration-200 hover:text-[#635BFF]"
              style={{ color: 'rgba(247,245,240,0.5)' }}
              onClick={(e) => e.preventDefault()}
            >
              <BookOpen className="w-4 h-4" />
              Documentation
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
