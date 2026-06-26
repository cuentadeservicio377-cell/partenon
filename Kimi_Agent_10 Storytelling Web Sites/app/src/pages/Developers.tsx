import { useRef, useState, useCallback, useMemo } from 'react';
import { Link } from 'react-router';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import {
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  Terminal,
  Shield,
  CreditCard,
  Calendar,
  Users,
  Brain,
  BookOpen,
  MessageSquare,
  Zap,
  ArrowRight,
  Database,
  FileJson,
  Download,
} from 'lucide-react';

gsap.registerPlugin(ScrollTrigger);

/* ═══════════════════════════════════════════
   Hero data
   ═══════════════════════════════════════════ */

interface Hero {
  key: string;
  name: string;
  role: string;
  mcpServer: string;
  color: string;
  colorVar: string;
  icon: React.ReactNode;
  description: string;
  fileFormat: string;
  fileFormatDef: string;
  capabilities: { name: string; mcpTool: string; api: string; output: string }[];
  mcpTools: string[];
  cliExample: string;
  configInterface: string;
  integrations: string[];
}

const heroes: Hero[] = [
  {
    key: 'scribe',
    name: 'THE SCRIBE',
    role: 'Finance',
    mcpServer: 'sheets-mcp',
    color: '#4A90A4',
    colorVar: '--hero-scribe',
    icon: <BookOpen className="h-5 w-5" />,
    description:
      'Financial data agent. Handles all Google Sheets operations, financial modeling, dashboard creation, and the .finance file format. Built on Google Sheets API with custom query functions and Chart.js visualization.',
    fileFormat: '.finance',
    fileFormatDef: `interface FinanceFile {\n  version: "1.0";\n  business: {\n    name: string;\n    type: "cafe" | "construction" | "retail" | "saas" | "custom";\n    currency: string;\n  };\n  costs: {\n    fixed: CostItem[];\n    variable: CostItem[];\n  };\n  revenue: RevenueStream[];\n  dashboards: DashboardConfig[];\n}`,
    capabilities: [
      { name: 'Financial Modeling', mcpTool: 'sheets.create_model', api: 'Google Sheets API', output: '.finance file' },
      { name: 'Dashboard Creation', mcpTool: 'sheets.build_dashboard', api: 'Google Sheets API, Chart.js', output: 'Live dashboard URL' },
      { name: 'Data Analysis', mcpTool: 'sheets.analyze_data', api: 'Google Sheets API', output: 'Analysis report' },
    ],
    mcpTools: ['sheets.create_model', 'sheets.build_dashboard', 'sheets.analyze_data', 'sheets.sync_data', 'sheets.export_report'],
    cliExample: `$ hermes activate scribe\n\u2713 The Scribe initialized\n\u2713 Google Sheets API connected\n\u2713 .finance parser loaded\n\n$ hermes mission scribe --type financial-model \\\n  --business "Caf\u00e9 Central" --industry cafe\n\n\ud83d\udccb Mission: Build Financial Model\n\u2713 Fixed costs: 4 items\n\u2713 Variable costs: 7 items\n\u2713 Break-even calculation complete`,
    configInterface: `interface ScribeConfig {\n  googleSheets: {\n    credentials: string;\n    spreadsheetId: string;\n    range: string;\n  };\n  financeFile: {\n    format: ".finance";\n    schema: "v1.0";\n    fields: ["cost_fixed", "cost_variable", "revenue", "tax_rate"];\n  };\n  dashboard: {\n    enabled: boolean;\n    template: "financial_overview" | "cash_flow" | "custom";\n    refreshInterval: number;\n  };\n}`,
    integrations: ['Google Sheets API v4'],
  },
  {
    key: 'herald',
    name: 'THE HERALD',
    role: 'Communication',
    mcpServer: 'comms-mcp',
    color: '#9B59B6',
    colorVar: '--hero-herald',
    icon: <MessageSquare className="h-5 w-5" />,
    description:
      'Communication and marketing agent. Manages social media APIs, brand strategy, SEO/GEO optimization, and the .design file format. Integrates with major social platforms and analytics tools.',
    fileFormat: '.design',
    fileFormatDef: `interface DesignFile {\n  version: "1.0";\n  brand: {\n    voice: VoiceConfig;\n    visual: VisualConfig;\n    messaging: MessageConfig;\n    audience: AudienceConfig;\n  };\n  campaigns: Campaign[];\n  seo: SEOConfig;\n}`,
    capabilities: [
      { name: 'Social Media Mgmt', mcpTool: 'comms.social_post', api: 'Instagram, Twitter, LinkedIn APIs', output: 'Published content' },
      { name: 'Brand Strategy', mcpTool: 'comms.brand_guide', api: 'Internal ML', output: '.design file' },
      { name: 'SEO/GEO Optimizer', mcpTool: 'comms.optimize_seo', api: 'Google Analytics', output: 'SEO report' },
    ],
    mcpTools: ['comms.social_post', 'comms.brand_guide', 'comms.optimize_seo', 'comms.analyze_engagement', 'comms.schedule_content'],
    cliExample: `$ hermes activate herald\n\u2713 The Herald initialized\n\u2713 Social APIs connected\n\u2713 .design parser loaded\n\n$ hermes mission herald --type brand-strategy \\\n  --audience "young professionals"\n\n\ud83d\udce2 Mission: Build Brand Strategy\n\u2713 Voice profile generated\n\u2713 Visual identity mapped\n\u2713 Messaging framework created`,
    configInterface: `interface HeraldConfig {\n  brandFile: {\n    format: ".design";\n    schema: "v1.0";\n    sections: ["voice", "visual", "messaging", "audience"];\n  };\n  socialAccounts: string[];\n  contentStrategy: {\n    seoEnabled: boolean;\n    geoTargeting: boolean;\n    calendarIntegration: boolean;\n  };\n}`,
    integrations: ['Instagram API', 'Twitter API', 'LinkedIn API', 'Google Analytics'],
  },
  {
    key: 'collector',
    name: 'THE COLLECTOR',
    role: 'Payments/Stripe',
    mcpServer: 'stripe-mcp',
    color: '#635BFF',
    colorVar: '--hero-collector',
    icon: <CreditCard className="h-5 w-5" />,
    description:
      'Payment processing agent. Full Stripe SDK integration \u2014 payments, subscriptions, invoicing, revenue tracking, and fraud monitoring. Handles all financial transactions for the enterprise.',
    fileFormat: '.revenue',
    fileFormatDef: `interface RevenueFile {\n  version: "1.0";\n  stripe: {\n    products: Product[];\n    subscriptions: Subscription[];\n    paymentMethods: string[];\n  };\n  tracking: {\n    metrics: string[];\n    alerts: AlertConfig;\n  };\n}`,
    capabilities: [
      { name: 'Payment Processing', mcpTool: 'stripe.process_payment', api: 'Stripe API', output: 'Payment confirmation' },
      { name: 'Subscription Mgmt', mcpTool: 'stripe.manage_subs', api: 'Stripe Billing', output: 'Subscription state' },
      { name: 'Revenue Tracking', mcpTool: 'stripe.track_revenue', api: 'Stripe Sigma', output: 'Revenue report' },
    ],
    mcpTools: ['stripe.process_payment', 'stripe.manage_subs', 'stripe.track_revenue', 'stripe.generate_invoice', 'stripe.monitor_fraud'],
    cliExample: `$ hermes activate collector\n\u2713 The Collector initialized\n\u2713 Stripe SDK connected\n\u2713 .revenue parser loaded\n\n$ hermes mission collector --type payment-setup \\\n  --business "Caf\u00e9 Central"\n\n\ud83d\udcb3 Mission: Setup Payments\n\u2713 Product catalog created\n\u2713 Payment methods configured\n\u2713 Webhook endpoints registered`,
    configInterface: `interface CollectorConfig {\n  stripe: {\n    apiKey: string;\n    webhookSecret: string;\n    products: string[];\n    subscriptions: boolean;\n  };\n  paymentMethods: ["card", "bank_transfer", "digital_wallet"];\n  invoicing: {\n    autoGenerate: boolean;\n    template: string;\n    reminderDays: number[];\n  };\n}`,
    integrations: ['Stripe API (Payments, Billing, Connect, Sigma)'],
  },
  {
    key: 'guardian',
    name: 'THE GUARDIAN',
    role: 'Security/Envidia',
    mcpServer: 'security-mcp',
    color: '#76B900',
    colorVar: '--hero-guardian',
    icon: <Shield className="h-5 w-5" />,
    description:
      'Security and AI model management agent. Manages API keys through encrypted vault, Envidia GPU allocation, access control policies, and audit logging. Ensures enterprise-grade security across all hero operations.',
    fileFormat: '.security',
    fileFormatDef: `interface SecurityFile {\n  version: "1.0";\n  policies: {\n    accessControl: RBACConfig;\n    audit: AuditConfig;\n    keyRotation: RotationConfig;\n  };\n  envidia: {\n    gpuAllocation: GPUConfig;\n    modelAccess: ModelConfig;\n  };\n}`,
    capabilities: [
      { name: 'API Key Vault', mcpTool: 'security.manage_keys', api: 'HashiCorp Vault', output: 'Key policy' },
      { name: 'GPU Allocation', mcpTool: 'security.allocate_gpu', api: 'Envidia API', output: 'GPU config' },
      { name: 'Access Control', mcpTool: 'security.set_policies', api: 'Internal RBAC', output: 'Policy file' },
    ],
    mcpTools: ['security.manage_keys', 'security.allocate_gpu', 'security.set_policies', 'security.audit_log', 'security.rotate_keys'],
    cliExample: `$ hermes activate guardian\n\u2713 The Guardian initialized\n\u2713 Envidia API connected\n\u2713 Key vault mounted\n\n$ hermes mission guardian --type security-audit \\\n  --scope "all heroes"\n\n\ud83d\udee1\uFE0F Mission: Security Audit\n\u2713 All API keys verified\n\u2713 Access policies updated\n\u2713 Audit log enabled`,
    configInterface: `interface GuardianConfig {\n  envidia: {\n    apiKey: string;\n    models: string[];\n    rateLimits: {\n      requestsPerMinute: number;\n      tokensPerDay: number;\n    };\n  };\n  apiKeyManager: {\n    rotationPolicy: "daily" | "weekly" | "monthly";\n    alertOnExposure: boolean;\n  };\n  accessControl: {\n    rbac: boolean;\n    auditLog: boolean;\n  };\n}`,
    integrations: ['Envidia API', 'OpenAI API', 'HashiCorp Vault'],
  },
  {
    key: 'strategist',
    name: 'THE STRATEGIST',
    role: 'Admin',
    mcpServer: 'ops-mcp',
    color: '#FFB800',
    colorVar: '--hero-strategist',
    icon: <Calendar className="h-5 w-5" />,
    description:
      'Operations and project management agent. Orchestrates Google Calendar, task queues, email processing, and internal coordination. The central nervous system of project execution.',
    fileFormat: '.operations',
    fileFormatDef: `interface OperationsFile {\n  version: "1.0";\n  calendar: {\n    provider: "google";\n    syncDirection: string;\n    reminderSettings: ReminderConfig;\n  };\n  tasks: {\n    methodology: string;\n    autoAssign: boolean;\n    queues: QueueConfig[];\n  };\n}`,
    capabilities: [
      { name: 'Calendar Sync', mcpTool: 'ops.sync_calendar', api: 'Google Calendar API', output: 'Sync state' },
      { name: 'Task Management', mcpTool: 'ops.manage_tasks', api: 'Bull/BullMQ', output: 'Task queue' },
      { name: 'Email Processing', mcpTool: 'ops.parse_email', api: 'Gmail API', output: 'Parsed actions' },
    ],
    mcpTools: ['ops.sync_calendar', 'ops.manage_tasks', 'ops.parse_email', 'ops.schedule_meeting', 'ops.send_reminder'],
    cliExample: `$ hermes activate strategist\n\u2713 The Strategist initialized\n\u2713 Google Calendar connected\n\u2713 Task queues ready\n\n$ hermes mission strategist --type project-setup \\\n  --methodology agile\n\n\ud83d\udcc5 Mission: Setup Project Mgmt\n\u2713 Calendar synchronized\n\u2713 Task boards created\n\u2713 Reminder system active`,
    configInterface: `interface StrategistConfig {\n  googleCalendar: {\n    credentials: string;\n    calendarId: string;\n    syncDirection: "bidirectional" | "push" | "pull";\n  };\n  projectManagement: {\n    methodology: "agile" | "waterfall" | "hybrid";\n    autoAssign: boolean;\n    reminderSettings: {\n      beforeHours: number[];\n      channels: ["email", "slack", "in_app"];\n    };\n  };\n}`,
    integrations: ['Google Calendar API', 'Gmail API', 'Bull/BullMQ'],
  },
  {
    key: 'diplomat',
    name: 'THE DIPLOMAT',
    role: 'Relations',
    mcpServer: 'crm-mcp',
    color: '#E74C3C',
    colorVar: '--hero-diplomat',
    icon: <Users className="h-5 w-5" />,
    description:
      'Client relationship management agent. Handles CRM operations, external communications, meeting scheduling, and partnership management. The bridge between internal operations and external stakeholders.',
    fileFormat: '.relations',
    fileFormatDef: `interface RelationsFile {\n  version: "1.0";\n  crm: {\n    provider: string;\n    contacts: Contact[];\n    interactions: Interaction[];\n  };\n  communications: {\n    templates: Template[];\n    followUpRules: FollowUpConfig;\n  };\n}`,
    capabilities: [
      { name: 'CRM Operations', mcpTool: 'crm.sync_contacts', api: 'HubSpot / Salesforce', output: 'CRM state' },
      { name: 'Meeting Scheduler', mcpTool: 'crm.schedule_meeting', api: 'Google Meet API', output: 'Meeting link' },
      { name: 'Follow-up Engine', mcpTool: 'crm.auto_followup', api: 'Email APIs', output: 'Sent messages' },
    ],
    mcpTools: ['crm.sync_contacts', 'crm.schedule_meeting', 'crm.auto_followup', 'crm.log_interaction', 'crm.generate_proposal'],
    cliExample: `$ hermes activate diplomat\n\u2713 The Diplomat initialized\n\u2713 CRM connected\n\u2713 .relations parser loaded\n\n$ hermes mission diplomat --type client-onboard \\\n  --client "Acme Corp"\n\n\ud83e\udd1d Mission: Onboard Client\n\u2713 CRM profile created\n\u2713 Welcome sequence sent\n\u2713 Meeting scheduled`,
    configInterface: `interface DiplomatConfig {\n  crm: {\n    provider: "salesforce" | "hubspot" | "custom";\n    apiKey: string;\n    syncInterval: number;\n  };\n  clientPortal: {\n    enabled: boolean;\n    whiteLabel: boolean;\n    notificationChannels: string[];\n  };\n  followUp: {\n    autoReminders: boolean;\n    escalationRules: EscalationRule[];\n  };\n}`,
    integrations: ['HubSpot API / Salesforce API', 'Google Meet API', 'Email APIs'],
  },
  {
    key: 'brain',
    name: 'THE BRAIN',
    role: 'G-Brain / MCP Hub',
    mcpServer: 'gbrain-mcp',
    color: '#D4A853',
    colorVar: '--hero-brain',
    icon: <Brain className="h-5 w-5" />,
    description:
      'Central intelligence orchestrator. Manages the MCP protocol layer, cross-agent context sharing, pattern recognition, and strategic insight generation. The meta-agent that makes The Parten\u00f3n greater than the sum of its parts.',
    fileFormat: '.brain',
    fileFormatDef: `interface BrainFile {\n  version: "1.0";\n  orchestration: {\n    loadBalancing: string;\n    failover: boolean;\n    healthCheckInterval: number;\n  };\n  contextSharing: {\n    enabled: boolean;\n    ttl: string;\n    accessRules: AccessRule[];\n  };\n}`,
    capabilities: [
      { name: 'Context Sharing', mcpTool: 'brain.share_context', api: 'MCP Protocol', output: 'Shared context' },
      { name: 'Pattern Analysis', mcpTool: 'brain.find_patterns', api: 'Internal ML', output: 'Insight report' },
      { name: 'MCP Orchestration', mcpTool: 'brain.orchestrate', api: 'MCP SDK', output: 'Agent mesh' },
    ],
    mcpTools: ['brain.share_context', 'brain.find_patterns', 'brain.orchestrate', 'brain.register_agent', 'brain.generate_insight'],
    cliExample: `$ hermes activate brain\n\u2713 G-Brain initialized\n\u2713 MCP Hub started\n\n$ hermes mission brain --type cross-agent-analysis \\\n  --scope "all heroes" --pattern "revenue"\n\n\ud83e\udde0 Mission: Cross-Agent Analysis\n\u2713 All contexts indexed\n\u2713 Pattern correlation complete\n\u2713 3 strategic insights generated`,
    configInterface: `interface BrainConfig {\n  mcpHub: {\n    version: "1.0";\n    protocol: "model_context_protocol";\n    transports: ["stdio", "http", "websocket"];\n  };\n  orchestration: {\n    loadBalancing: "round_robin" | "least_loaded" | "priority";\n    failover: boolean;\n    healthCheckInterval: number;\n  };\n}`,
    integrations: ['Model Context Protocol (MCP) SDK'],
  },
];

/* ═══════════════════════════════════════════
   Syntax highlighter helper
   ═══════════════════════════════════════════ */

function SyntaxHighlight({ code, dark = true }: { code: string; dark?: boolean }) {
  const highlighted = useMemo(() => {
    // Simple syntax highlighting for TypeScript
    const lines = code.split('\n');
    return lines.map((line) => {
      let styled = line;
      // Keywords
      styled = styled.replace(/\b(interface|type|const|let|var|import|export|from|return|await|async|new|class|function|if|else|for|of)\b/g, '<span class="sh-keyword">$1</span>');
      // Types
      styled = styled.replace(/\b(string|number|boolean|void|any|null|undefined|never|unknown|object|Record|Array|Promise|ReactNode)\b/g, '<span class="sh-type">$1</span>');
      // Strings
      styled = styled.replace(/("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g, '<span class="sh-string">$1</span>');
      // Comments
      styled = styled.replace(/(\/\/.*)/g, '<span class="sh-comment">$1</span>');
      // Numbers
      styled = styled.replace(/\b(\d+(?:\.\d+)?)\b/g, '<span class="sh-number">$1</span>');
      // Boolean
      styled = styled.replace(/\b(true|false)\b/g, '<span class="sh-boolean">$1</span>');
      // Property names before :
      styled = styled.replace(/(\w+)(\s*:)(?!\s*\w)/g, '<span class="sh-prop">$1</span>$2');
      return styled;
    }).join('\n');
  }, [code]);

  return (
    <pre
      className="font-mono text-[0.8125rem] leading-[1.6] overflow-x-auto p-5 rounded-md whitespace-pre"
      style={{
        backgroundColor: dark ? '#1A1A1E' : '#F0EDE6',
        color: dark ? '#F7F5F0' : '#2A2A2E',
        letterSpacing: '0.02em',
      }}
      dangerouslySetInnerHTML={{ __html: highlighted }}
    />
  );
}

/* ═══════════════════════════════════════════
   Code Block with copy button
   ═══════════════════════════════════════════ */

function CodeBlock({ code, dark = true }: { code: string; dark?: boolean }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }, [code]);

  return (
    <div className="relative group">
      <SyntaxHighlight code={code} dark={dark} />
      <button
        onClick={handleCopy}
        className="absolute top-3 right-3 p-2 rounded-md opacity-0 group-hover:opacity-100 transition-all duration-200 hover:bg-white/10"
        style={{ backgroundColor: dark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)' }}
        title="Copy to clipboard"
      >
        {copied ? (
          <Check className="h-4 w-4 text-[#76B900]" />
        ) : (
          <Copy className="h-4 w-4" style={{ color: dark ? 'rgba(247,245,240,0.5)' : 'rgba(42,42,46,0.5)' }} />
        )}
      </button>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Section Header
   ═══════════════════════════════════════════ */

function SectionHeader({
  eyebrow,
  headline,
  description,
  eyebrowColor = '#635BFF',
  textColor = '#2A2A2E',
  dividerColor = '#635BFF',
}: {
  eyebrow: string;
  headline: string;
  description?: string;
  eyebrowColor?: string;
  textColor?: string;
  dividerColor?: string;
}) {
  return (
    <div className="text-center mb-16" style={{ maxWidth: 'var(--container-narrow)', margin: '0 auto 4rem' }}>
      <span
        className="font-inter text-xs font-semibold tracking-[0.12em] uppercase block mb-4"
        style={{ color: eyebrowColor }}
      >
        {eyebrow}
      </span>
      <h2
        className="font-cinzel mb-4"
        style={{
          fontSize: 'clamp(2rem, 5vw, 4rem)',
          letterSpacing: '0.06em',
          lineHeight: 1.1,
          color: textColor,
        }}
      >
        {headline}
      </h2>
      <div
        className="mx-auto mb-4"
        style={{ width: '48px', height: '2px', backgroundColor: dividerColor }}
      />
      {description && (
        <p className="font-inter text-lg leading-relaxed" style={{ color: '#6B6B73', maxWidth: '600px', margin: '0 auto' }}>
          {description}
        </p>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════
   Architecture SVG Diagram Component
   ═══════════════════════════════════════════ */

function ArchitectureDiagram() {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);

  const cx = 400;
  const cy = 320;
  const heroRadius = 220;
  const infraRadius = 280;

  const heroPositions = useMemo(() => {
    return heroes.map((hero, i) => {
      const angle = (i * 2 * Math.PI) / 7 - Math.PI / 2;
      return {
        ...hero,
        x: cx + heroRadius * Math.cos(angle),
        y: cy + heroRadius * Math.sin(angle),
        angle,
        idx: i,
      };
    });
  }, []);

  const infraNodes = useMemo(() => {
    const labels = ['Google Workspace', 'Stripe Platform', 'Envidia Cloud', 'Nose Research'];
    const icons = ['G', 'S', 'E', 'N'];
    return labels.map((label, idx) => {
      const angle = (idx * 2 * Math.PI) / 4 - Math.PI / 2 + 0.3;
      return { label, icon: icons[idx], x: cx + infraRadius * Math.cos(angle), y: cy + infraRadius * Math.sin(angle) };
    });
  }, []);

  const getLineOpacity = (from: string, to: string) => {
    if (!hoveredNode) return 0.35;
    const f = from.replace('hero-', '');
    const t = to.replace('hero-', '');
    if (hoveredNode === 'hermes') {
      return from === 'hermes' || to === 'hermes' ? 0.9 : 0.1;
    }
    if (hoveredNode === 'brain') {
      return from === 'brain' || to === 'brain' ? 0.9 : 0.1;
    }
    if (hoveredNode.startsWith('hero-')) {
      const hk = hoveredNode.replace('hero-', '');
      return f === hk || t === hk ? 0.9 : 0.1;
    }
    return 0.35;
  };

  useGSAP(
    () => {
      if (!svgRef.current) return;
      const nodes = svgRef.current.querySelectorAll('.arch-node');
      const lines = svgRef.current.querySelectorAll('.arch-line');

      gsap.set(nodes, { opacity: 0, scale: 0.8 });
      gsap.set(lines, { strokeDasharray: 600, strokeDashoffset: 600 });

      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current,
          start: 'top 70%',
          end: 'bottom 30%',
          toggleActions: 'play none none none',
        },
      });

      tl.to(infraNodes.map((_, idx) => nodes[nodes.length - 4 + idx]), {
        opacity: 1, scale: 1, duration: 0.5, stagger: 0.08, ease: 'expo.out',
      }, 0);
      tl.to(nodes[0], { opacity: 1, scale: 1, duration: 0.6, ease: 'expo.out' }, 0.3);
      tl.to(heroPositions.map((_, idx) => nodes[idx + 1]), {
        opacity: 1, scale: 1, duration: 0.5, stagger: 0.08, ease: 'expo.out',
      }, 0.5);
      tl.to(nodes[nodes.length - 5], { opacity: 1, scale: 1, duration: 0.6, ease: 'expo.out' }, 0.9);
      tl.to(lines, { strokeDashoffset: 0, duration: 1.2, stagger: 0.02, ease: 'expo.out' }, 0.7);
    },
    { scope: containerRef },
  );

  return (
    <div ref={containerRef} className="w-full overflow-x-auto">
      <svg
        ref={svgRef}
        viewBox="0 0 800 640"
        className="w-full"
        style={{ minWidth: '700px' }}
      >
        <defs>
          {heroes.map((h) => (
            <filter key={h.key} id={`glow-${h.key}`}>
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          ))}
          <filter id="glow-hermes">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="glow-brain">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Background dots */}
        {Array.from({ length: 30 }).map((_, i) =>
          Array.from({ length: 20 }).map((_, j) => (
            <circle
              key={`dot-${i}-${j}`}
              cx={i * 30 + 20}
              cy={j * 30 + 20}
              r="0.8"
              fill="rgba(42,42,46,0.08)"
            />
          )),
        )}

        {/* Lines: Brain to infra */}
        {infraNodes.map((infra, i) => (
          <g key={`brain-infra-${i}`}>
            <line
              className="arch-line"
              x1={cx} y1={cy + 80}
              x2={infra.x} y2={infra.y}
              stroke="#D4A853"
              strokeWidth="1.5"
              opacity={getLineOpacity('brain', 'infra')}
            />
            <text
              x={(cx + infra.x) / 2}
              y={(cy + 80 + infra.y) / 2}
              fill="#6B6B73"
              fontSize="9"
              fontFamily="JetBrains Mono, monospace"
              textAnchor="middle"
            >
              External MCP
            </text>
          </g>
        ))}

        {/* Lines: Hermes to heroes */}
        {heroPositions.map((hero, i) => (
          <g key={`hermes-hero-${i}`}>
            <line
              className="arch-line"
              x1={cx} y1={cy}
              x2={hero.x} y2={hero.y}
              stroke={hero.color}
              strokeWidth="1.5"
              opacity={getLineOpacity('hermes', `hero-${hero.key}`)}
            />
            <text
              x={(cx + hero.x) / 2 + 8}
              y={(cy + hero.y) / 2}
              fill="#6B6B73"
              fontSize="9"
              fontFamily="JetBrains Mono, monospace"
              textAnchor="start"
            >
              Mission API
            </text>
          </g>
        ))}

        {/* Lines: Brain to heroes */}
        {heroPositions.map((hero, i) => (
          <g key={`brain-hero-${i}`}>
            <line
              className="arch-line"
              x1={cx} y1={cy + 80}
              x2={hero.x} y2={hero.y}
              stroke={hero.color}
              strokeWidth="1"
              strokeDasharray="4,4"
              opacity={getLineOpacity('brain', `hero-${hero.key}`)}
            />
            <text
              x={(cx + hero.x) / 2 - 10}
              y={(cy + 80 + hero.y) / 2 + 5}
              fill="#6B6B73"
              fontSize="8"
              fontFamily="JetBrains Mono, monospace"
              textAnchor="end"
            >
              MCP
            </text>
          </g>
        ))}

        {/* Infrastructure nodes */}
        {infraNodes.map((infra, i) => (
          <g
            key={`infra-${i}`}
            className="arch-node"
            onMouseEnter={() => setHoveredNode(`infra-${i}`)}
            onMouseLeave={() => setHoveredNode(null)}
            style={{ cursor: 'default' }}
          >
            <rect
              x={infra.x - 55}
              y={infra.y - 18}
              width="110"
              height="36"
              rx="6"
              fill="#F7F5F0"
              stroke="rgba(42,42,46,0.2)"
              strokeWidth="1"
            />
            <text
              x={infra.x}
              y={infra.y + 4}
              fill="#2A2A2E"
              fontSize="11"
              fontFamily="Inter, sans-serif"
              fontWeight="500"
              textAnchor="middle"
            >
              {infra.label}
            </text>
          </g>
        ))}

        {/* Brain node */}
        <g
          className="arch-node"
          onMouseEnter={() => setHoveredNode('brain')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <polygon
            points={`${cx},${cy + 40} ${cx + 60},${cy + 80} ${cx},${cy + 120} ${cx - 60},${cy + 80}`}
            fill="#D4A853"
            opacity={hoveredNode === 'brain' ? 0.2 : 0.1}
            stroke="#D4A853"
            strokeWidth="2"
            filter={hoveredNode === 'brain' ? 'url(#glow-brain)' : undefined}
          />
          <text x={cx} y={cy + 76} fill="#D4A853" fontSize="10" fontFamily="Cinzel, serif" fontWeight="600" textAnchor="middle" letterSpacing="0.08em">
            G-BRAIN
          </text>
          <text x={cx} y={cy + 92} fill="#6B6B73" fontSize="8" fontFamily="JetBrains Mono, monospace" textAnchor="middle">
            MCP Orchestrator
          </text>
        </g>

        {/* Hero nodes */}
        {heroPositions.map((hero) => (
          <g
            key={hero.key}
            className="arch-node"
            onMouseEnter={() => setHoveredNode(`hero-${hero.key}`)}
            onMouseLeave={() => setHoveredNode(null)}
            style={{ cursor: 'pointer' }}
          >
            <rect
              x={hero.x - 55}
              y={hero.y - 28}
              width="110"
              height="56"
              rx="8"
              fill={hero.color}
              opacity={hoveredNode === `hero-${hero.key}` ? 0.15 : 0.08}
              stroke={hero.color}
              strokeWidth="2"
              filter={hoveredNode === `hero-${hero.key}` ? `url(#glow-${hero.key})` : undefined}
            />
            <text
              x={hero.x}
              y={hero.y - 4}
              fill={hero.color}
              fontSize="10"
              fontFamily="Cinzel, serif"
              fontWeight="600"
              textAnchor="middle"
              letterSpacing="0.06em"
            >
              {hero.name}
            </text>
            <text
              x={hero.x}
              y={hero.y + 14}
              fill="#6B6B73"
              fontSize="8"
              fontFamily="JetBrains Mono, monospace"
              textAnchor="middle"
            >
              {hero.mcpServer}
            </text>
          </g>
        ))}

        {/* Hermes central node */}
        <g
          className="arch-node"
          onMouseEnter={() => setHoveredNode('hermes')}
          onMouseLeave={() => setHoveredNode(null)}
          style={{ cursor: 'pointer' }}
        >
          <polygon
            points={`${cx},${cy - 50} ${cx + 45},${cy - 25} ${cx + 45},${cy + 25} ${cx},${cy + 50} ${cx - 45},${cy + 25} ${cx - 45},${cy - 25}`}
            fill="#635BFF"
            opacity={hoveredNode === 'hermes' ? 0.25 : 0.12}
            stroke="#635BFF"
            strokeWidth="2.5"
            filter={hoveredNode === 'hermes' ? 'url(#glow-hermes)' : undefined}
          />
          <text x={cx} y={cy - 5} fill="#635BFF" fontSize="14" fontFamily="Cinzel, serif" fontWeight="600" textAnchor="middle" letterSpacing="0.1em">
            HERMES
          </text>
          <text x={cx} y={cy + 14} fill="#6B6B73" fontSize="8" fontFamily="JetBrains Mono, monospace" textAnchor="middle">
            Enterprise Core
          </text>
        </g>
      </svg>
    </div>
  );
}

/* ═══════════════════════════════════════════
   MCP Protocol Diagram
   ═══════════════════════════════════════════ */

function MCPDiagram() {
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);

  const mcpServers = [
    { name: 'Google Workspace MCP', tools: 'Sheets, Calendar, Gmail, Drive', color: '#4285F4' },
    { name: 'Stripe MCP', tools: 'Payments, Billing, Connect', color: '#635BFF' },
    { name: 'Envidia MCP', tools: 'GPU, Models, Security', color: '#76B900' },
    { name: 'Social APIs MCP', tools: 'Instagram, Twitter, LinkedIn', color: '#9B59B6' },
    { name: 'CRM MCP', tools: 'HubSpot, Salesforce', color: '#E74C3C' },
    { name: 'Hero Agent Pool', tools: 'scribe, herald, collector...', color: '#D4A853' },
  ];

  const cx = 400;
  const cy = 220;
  const radius = 200;

  const serverPositions = mcpServers.map((s, idx) => {
    const angle = (idx * 2 * Math.PI) / 6 - Math.PI / 2;
    return { ...s, x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle), angle, idx };
  });

  useGSAP(
    () => {
      if (!svgRef.current) return;
      const nodes = svgRef.current.querySelectorAll('.mcp-node');
      const lines = svgRef.current.querySelectorAll('.mcp-line');

      gsap.set(nodes, { opacity: 0, scale: 0.8 });
      gsap.set(lines, { strokeDasharray: 400, strokeDashoffset: 400 });

      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current,
          start: 'top 70%',
          end: 'bottom 40%',
          toggleActions: 'play none none none',
        },
      });

      tl.to(serverPositions.map((_, i) => nodes[i + 1]), {
        opacity: 1, scale: 1, duration: 0.5, stagger: 0.08, ease: 'expo.out',
      }, 0);
      tl.to(nodes[0], { opacity: 1, scale: 1, duration: 0.6, ease: 'expo.out' }, 0.4);
      tl.to(lines, { strokeDashoffset: 0, duration: 0.8, stagger: 0.03, ease: 'expo.out' }, 0.3);
    },
    { scope: containerRef },
  );

  return (
    <div ref={containerRef} className="w-full overflow-x-auto">
      <svg ref={svgRef} viewBox="0 0 800 440" className="w-full" style={{ minWidth: '600px' }}>
        <defs>
          <filter id="glow-mcp-hub">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Grid background */}
        {Array.from({ length: 28 }).map((_, i) =>
          Array.from({ length: 16 }).map((_, j) => (
            <circle key={`mcp-dot-${i}-${j}`} cx={i * 30 + 15} cy={j * 30 + 15} r="0.6" fill="rgba(247,245,240,0.06)" />
          )),
        )}

        {/* Connection lines */}
        {serverPositions.map((server, i) => (
          <g key={`mcp-line-${i}`}>
            <line
              className="mcp-line"
              x1={cx} y1={cy}
              x2={server.x} y2={server.y}
              stroke={server.color}
              strokeWidth="1.5"
              opacity="0.5"
            />
            <text
              x={(cx + server.x) / 2}
              y={(cy + server.y) / 2 - 4}
              fill="rgba(247,245,240,0.4)"
              fontSize="8"
              fontFamily="JetBrains Mono, monospace"
              textAnchor="middle"
            >
              mcp.call()
            </text>
          </g>
        ))}

        {/* Server nodes */}
        {serverPositions.map((server, i) => (
          <g key={`mcp-srv-${i}`} className="mcp-node">
            <rect
              x={server.x - 65}
              y={server.y - 24}
              width="130"
              height="48"
              rx="8"
              fill={server.color}
              opacity="0.1"
              stroke={server.color}
              strokeWidth="1.5"
            />
            <text
              x={server.x}
              y={server.y - 4}
              fill={server.color}
              fontSize="10"
              fontFamily="Inter, sans-serif"
              fontWeight="600"
              textAnchor="middle"
            >
              {server.name}
            </text>
            <text
              x={server.x}
              y={server.y + 12}
              fill="rgba(247,245,240,0.4)"
              fontSize="8"
              fontFamily="JetBrains Mono, monospace"
              textAnchor="middle"
            >
              {server.tools}
            </text>
          </g>
        ))}

        {/* Central hub */}
        <g className="mcp-node">
          <circle
            cx={cx}
            cy={cy}
            r="48"
            fill="#D4A853"
            opacity="0.15"
            stroke="#D4A853"
            strokeWidth="2.5"
            filter="url(#glow-mcp-hub)"
          />
          <text x={cx} y={cy - 6} fill="#D4A853" fontSize="12" fontFamily="Cinzel, serif" fontWeight="600" textAnchor="middle" letterSpacing="0.08em">
            G-BRAIN
          </text>
          <text x={cx} y={cy + 10} fill="rgba(247,245,240,0.6)" fontSize="9" fontFamily="JetBrains Mono, monospace" textAnchor="middle">
            MCP Server
          </text>
        </g>
      </svg>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Hero Spec Card Component
   ═══════════════════════════════════════════ */

function HeroSpecCard({ hero, index }: { hero: Hero; index: number }) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [expanded, setExpanded] = useState(false);

  useGSAP(
    () => {
      if (!cardRef.current) return;
      const items = cardRef.current.querySelectorAll('.spec-animate');

      gsap.fromTo(
        items,
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.08,
          ease: 'expo.out',
          scrollTrigger: {
            trigger: cardRef.current,
            start: 'top 80%',
            toggleActions: 'play none none none',
          },
        },
      );
    },
    { scope: cardRef },
  );

  const bgColor = index % 2 === 0 ? '#F7F5F0' : '#EDE8DF';

  return (
    <div
      ref={cardRef}
      id={`hero-${hero.key}`}
      className="w-full"
      style={{
        backgroundColor: hero.key === 'brain' ? '#2A2A2E' : bgColor,
        padding: 'clamp(2rem, 5vh, 4rem) 0',
      }}
    >
      <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 lg:gap-12">
          {/* Left column - info */}
          <div className="lg:col-span-3">
            <div className="spec-animate flex items-center gap-4 mb-4">
              <div
                className="flex items-center justify-center h-12 w-12 rounded-lg"
                style={{ backgroundColor: hero.color }}
              >
                <div className="text-white">{hero.icon}</div>
              </div>
              <div>
                <h3
                  className="font-cinzel text-xl"
                  style={{
                    color: hero.key === 'brain' ? '#F7F5F0' : '#2A2A2E',
                    letterSpacing: '0.04em',
                  }}
                >
                  {hero.name}
                </h3>
                <span
                  className="font-mono text-xs"
                  style={{ color: hero.color }}
                >
                  MCP Server: {hero.mcpServer}
                </span>
              </div>
            </div>

            <p
              className="spec-animate font-inter text-base leading-relaxed mb-6"
              style={{ color: hero.key === 'brain' ? 'rgba(247,245,240,0.7)' : '#6B6B73' }}
            >
              {hero.description}
            </p>

            {/* Capabilities table */}
            <div className="spec-animate mb-6">
              <h4
                className="font-inter text-sm font-semibold tracking-[0.08em] uppercase mb-3"
                style={{ color: hero.key === 'brain' ? '#F7F5F0' : '#2A2A2E' }}
              >
                Capabilities
              </h4>
              <div className="overflow-x-auto">
                <table className="w-full text-left" style={{ minWidth: '500px' }}>
                  <thead>
                    <tr style={{ borderBottom: `2px solid ${hero.color}30` }}>
                      {['Capability', 'MCP Tool', 'API/Integration', 'Output'].map((h) => (
                        <th
                          key={h}
                          className="font-inter text-xs font-semibold tracking-wide uppercase py-2 pr-4"
                          style={{ color: hero.color }}
                        >
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {hero.capabilities.map((cap, i) => (
                      <tr
                        key={i}
                        style={{
                          borderBottom: `1px solid ${hero.key === 'brain' ? 'rgba(247,245,240,0.08)' : 'rgba(42,42,46,0.08)'}`,
                        }}
                      >
                        <td className="font-inter text-sm py-2 pr-4" style={{ color: hero.key === 'brain' ? '#F7F5F0' : '#2A2A2E' }}>{cap.name}</td>
                        <td className="font-mono text-xs py-2 pr-4" style={{ color: hero.key === 'brain' ? 'rgba(247,245,240,0.6)' : '#6B6B73' }}>{cap.mcpTool}</td>
                        <td className="font-inter text-xs py-2 pr-4" style={{ color: hero.key === 'brain' ? 'rgba(247,245,240,0.6)' : '#6B6B73' }}>{cap.api}</td>
                        <td className="font-mono text-xs py-2" style={{ color: hero.color }}>{cap.output}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* MCP Tools */}
            <div className="spec-animate mb-4">
              <h4
                className="font-inter text-sm font-semibold tracking-[0.08em] uppercase mb-2"
                style={{ color: hero.key === 'brain' ? '#F7F5F0' : '#2A2A2E' }}
              >
                MCP Tools
              </h4>
              <div className="flex flex-wrap gap-2">
                {hero.mcpTools.map((tool) => (
                  <span
                    key={tool}
                    className="font-mono text-xs px-3 py-1 rounded-full"
                    style={{
                      backgroundColor: `${hero.color}15`,
                      color: hero.color,
                      border: `1px solid ${hero.color}30`,
                    }}
                  >
                    {tool}
                  </span>
                ))}
              </div>
            </div>

            {/* Expandable config interface */}
            <div className="spec-animate">
              <button
                onClick={() => setExpanded(!expanded)}
                className="flex items-center gap-2 font-inter text-sm font-medium transition-colors duration-200 hover:opacity-80"
                style={{ color: hero.color }}
              >
                {expanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                {expanded ? 'Hide Configuration' : 'Show Configuration'}
              </button>
              {expanded && (
                <div className="mt-3">
                  <CodeBlock code={hero.configInterface} dark={hero.key !== 'brain'} />
                </div>
              )}
            </div>
          </div>

          {/* Right column - CLI example */}
          <div className="lg:col-span-2 spec-animate">
            <div
              className="rounded-lg p-5 h-full"
              style={{
                backgroundColor: hero.key === 'brain' ? '#1A1A1E' : '#1A1A1E',
                border: `1px solid ${hero.color}30`,
              }}
            >
              <div className="flex items-center gap-2 mb-3">
                <Terminal className="h-4 w-4" style={{ color: hero.color }} />
                <span className="font-mono text-xs" style={{ color: hero.color }}>CLI Example</span>
              </div>
              <pre
                className="font-mono text-[0.75rem] leading-[1.7] overflow-x-auto whitespace-pre"
                style={{ color: '#F7F5F0' }}
              >
                {hero.cliExample}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Sequence Diagram Component
   ═══════════════════════════════════════════ */

function SequenceDiagram({ steps }: { steps: { from: string; to: string; label: string }[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const stepRefs = useRef<(HTMLDivElement | null)[]>([]);

  useGSAP(
    () => {
      stepRefs.current.forEach((el) => {
        if (!el) return;
        gsap.fromTo(
          el,
          { x: -20, opacity: 0 },
          {
            x: 0,
            opacity: 1,
            duration: 0.5,
            ease: 'expo.out',
            scrollTrigger: {
              trigger: el,
              start: 'top 85%',
              toggleActions: 'play none none none',
            },
          },
        );
      });
    },
    { scope: containerRef },
  );

  const uniqueActors = useMemo(() => {
    const actors = new Set<string>();
    steps.forEach((s) => { actors.add(s.from); actors.add(s.to); });
    return Array.from(actors);
  }, [steps]);

  const actorColors: Record<string, string> = {
    'Customer': '#4A90A4',
    'Stripe': '#635BFF',
    'Collector': '#635BFF',
    'Brain': '#D4A853',
    'Scribe': '#4A90A4',
    'Herald': '#9B59B6',
    'Sheets': '#4285F4',
    'Social': '#9B59B6',
    'Calendar': '#FFB800',
    'Strategist': '#FFB800',
    'Diplomat': '#E74C3C',
    'CRM': '#E74C3C',
    'Envidia': '#76B900',
    'Guardian': '#76B900',
    'Vault': '#76B900',
    'Hermes': '#635BFF',
    'All Heroes': '#D4A853',
  };

  return (
    <div ref={containerRef} className="w-full overflow-x-auto">
      <div className="flex gap-6" style={{ minWidth: `${uniqueActors.length * 100}px` }}>
        {/* Actor columns */}
        {uniqueActors.map((actor) => (
          <div key={actor} className="flex-1 flex flex-col items-center">
            <div
              className="font-inter text-xs font-semibold tracking-wide uppercase px-3 py-1.5 rounded-md mb-4"
              style={{
                backgroundColor: `${actorColors[actor] || '#635BFF'}20`,
                color: actorColors[actor] || '#635BFF',
                border: `1px solid ${actorColors[actor] || '#635BFF'}40`,
              }}
            >
              {actor}
            </div>
            <div className="w-px flex-1" style={{ backgroundColor: 'rgba(42,42,46,0.15)', minHeight: '200px' }} />
          </div>
        ))}
      </div>

      {/* Step arrows */}
      <div className="mt-4 space-y-3">
        {steps.map((step, i) => (
          <div
            key={i}
            ref={(el) => { stepRefs.current[i] = el; }}
            className="flex items-center gap-3"
          >
            <div
              className="font-mono text-xs px-3 py-2 rounded-md flex-1"
              style={{
                backgroundColor: `${actorColors[step.from] || '#635BFF'}08`,
                borderLeft: `3px solid ${actorColors[step.from] || '#635BFF'}`,
              }}
            >
              <span style={{ color: actorColors[step.from] || '#635BFF', fontWeight: 600 }}>{step.from}</span>
              <ArrowRight className="h-3 w-3 inline mx-2" style={{ color: '#6B6B73' }} />
              <span style={{ color: actorColors[step.to] || '#635BFF', fontWeight: 600 }}>{step.to}</span>
              <span className="ml-3" style={{ color: '#6B6B73' }}>{step.label}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Timeline Component
   ═══════════════════════════════════════════ */

function WorkshopTimeline() {
  const containerRef = useRef<HTMLDivElement>(null);

  const segments = [
    { label: 'Setup', duration: '15min', color: '#4A90A4', desc: 'Environment prep, dependency install' },
    { label: 'Onboarding', duration: '20min', color: '#635BFF', desc: 'Hermes init, enterprise config' },
    { label: 'Hero Config', duration: '30min', color: '#FFB800', desc: 'Enable heroes, set API keys' },
    { label: 'Integration Test', duration: '25min', color: '#76B900', desc: 'End-to-end flow test' },
    { label: 'Q&A', duration: '15min', color: '#9B59B6', desc: 'Open discussion' },
    { label: 'Next Steps', duration: '15min', color: '#D4A853', desc: 'Deployment, monitoring' },
  ];

  const totalMinutes = segments.reduce((acc, s) => acc + parseInt(s.duration), 0);

  useGSAP(
    () => {
      const items = containerRef.current?.querySelectorAll('.timeline-seg');
      if (!items) return;
      gsap.fromTo(
        items,
        { scaleX: 0, opacity: 0 },
        {
          scaleX: 1,
          opacity: 1,
          duration: 0.6,
          stagger: 0.1,
          ease: 'expo.out',
          scrollTrigger: {
            trigger: containerRef.current,
            start: 'top 80%',
            toggleActions: 'play none none none',
          },
        },
      );
    },
    { scope: containerRef },
  );

  return (
    <div ref={containerRef}>
      {/* Horizontal bar */}
      <div className="flex w-full rounded-xl overflow-hidden mb-6" style={{ height: '48px' }}>
        {segments.map((seg, i) => (
          <div
            key={i}
            className="timeline-seg relative flex items-center justify-center group"
            style={{
              width: `${(parseInt(seg.duration) / totalMinutes) * 100}%`,
              backgroundColor: seg.color,
              transformOrigin: 'left',
              cursor: 'pointer',
            }}
            title={`${seg.label} (${seg.duration}): ${seg.desc}`}
          >
            <span className="font-inter text-xs font-semibold text-white tracking-wide uppercase hidden sm:block">
              {seg.label}
            </span>
            <span className="font-mono text-[10px] text-white/70 ml-1 hidden md:block">
              {seg.duration}
            </span>
            {/* Tooltip */}
            <div
              className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10"
              style={{ backgroundColor: '#2A2A2E' }}
            >
              <div className="font-inter text-xs font-semibold text-white">{seg.label} ({seg.duration})</div>
              <div className="font-inter text-xs" style={{ color: '#6B6B73' }}>{seg.desc}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-4 justify-center">
        {segments.map((seg, i) => (
          <div key={i} className="flex items-center gap-2">
            <div className="h-3 w-3 rounded-sm" style={{ backgroundColor: seg.color }} />
            <span className="font-inter text-xs" style={{ color: '#6B6B73' }}>
              {seg.label} <span className="font-mono">({seg.duration})</span>
            </span>
          </div>
        ))}
      </div>

      {/* Time markers */}
      <div className="flex justify-between mt-3 px-1">
        <span className="font-mono text-xs" style={{ color: '#6B6B73' }}>0:00</span>
        <span className="font-mono text-xs" style={{ color: '#6B6B73' }}>{Math.floor(totalMinutes / 60)}:{(totalMinutes % 60).toString().padStart(2, '0')}</span>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Tabs Component
   ═══════════════════════════════════════════ */

function InstallTabs() {
  const [activeTab, setActiveTab] = useState(0);
  const contentRef = useRef<HTMLDivElement>(null);

  const tabs = [
    {
      label: 'Quick Start',
      code: `# One-line installation
$ npx create-hermes@latest my-enterprise

# Follow the interactive wizard
? What type of business?  Cafe / Retail / SaaS / Construction / Other
? Business name:  My Amazing Cafe
? Activate heroes:  [x] Scribe [x] Herald [x] Collector
                     [x] Guardian [x] Strategist [x] Diplomat
? Google account:  user@gmail.com
? Stripe account:  sk_test_...
? Envidia API key:  nv-...

# Hermes initializes
\u2713 Creating enterprise directory
\u2713 Configuring Google Workspace
\u2713 Connecting Stripe (test mode)
\u2713 Setting up Envidia security
\u2713 Activating all 7 heroes
\u2713 MCP protocol initialized
\u2713 G-Brain connected

# Access your Parten\u00f3n
$ hermes dashboard
# \u2192 Opens Google Sheets dashboard
# \u2192 Starts hero monitoring
# \u2192 Launches web interface`,
    },
    {
      label: 'Manual Setup',
      code: `# Clone the repository
$ git clone https://github.com/the-parthenon/hermes.git
$ cd hermes

# Install dependencies
$ npm install

# Copy environment template
$ cp .env.example .env
# Edit .env with your API keys

# Build
$ npm run build

# Start
$ npm run start`,
    },
    {
      label: 'Docker',
      code: `# Pull the image
$ docker pull ghcr.io/theparthenon/hermes:latest

# Run with environment variables
$ docker run -d \\
  --name hermes \\
  --env-file .env \\
  -p 3000:3000 \\
  ghcr.io/theparthenon/hermes:latest

# Or with inline env vars
$ docker run -d \\
  --name hermes \\
  -p 3000:3000 \\
  -e GOOGLE_CLIENT_ID=... \\
  -e STRIPE_SECRET_KEY=... \\
  -e ENVIDIA_API_KEY=... \\
  ghcr.io/theparthenon/hermes:latest`,
    },
  ];

  useGSAP(
    () => {
      if (contentRef.current) {
        gsap.fromTo(
          contentRef.current,
          { opacity: 0, y: 10 },
          { opacity: 1, y: 0, duration: 0.3, ease: 'expo.out' },
        );
      }
    },
    { dependencies: [activeTab] },
  );

  return (
    <div>
      {/* Tab bar */}
      <div className="flex gap-0 mb-6 border-b" style={{ borderColor: 'rgba(247,245,240,0.1)' }}>
        {tabs.map((tab, i) => (
          <button
            key={i}
            onClick={() => setActiveTab(i)}
            className="relative px-6 py-3 font-inter text-sm font-medium transition-colors duration-200"
            style={{
              color: activeTab === i ? '#F7F5F0' : 'rgba(247,245,240,0.4)',
            }}
          >
            {tab.label}
            {activeTab === i && (
              <div
                className="absolute bottom-0 left-0 right-0 h-0.5"
                style={{ backgroundColor: '#635BFF' }}
              />
            )}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div ref={contentRef} key={activeTab}>
        <CodeBlock code={tabs[activeTab].code} dark />
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════
   Main Developers Page
   ═══════════════════════════════════════════ */

export default function Developers() {
  const pageRef = useRef<HTMLDivElement>(null);
  const heroRef = useRef<HTMLDivElement>(null);

  /* ── Scroll to section handler ── */
  const scrollTo = useCallback((id: string) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  }, []);

  /* ── Hero entrance animations ── */
  useGSAP(
    () => {
      if (!heroRef.current) return;
      const tl = gsap.timeline({ delay: 0.3 });

      tl.fromTo('.dev-hero-eyebrow', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' });
      tl.fromTo('.dev-hero-headline', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.8, ease: 'expo.out' }, '-=0.3');
      tl.fromTo('.dev-hero-subtitle', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }, '-=0.4');
      tl.fromTo('.dev-hero-badge', { opacity: 0, scale: 0.8 }, {
        opacity: 1, scale: 1, duration: 0.4, stagger: 0.1, ease: 'back.out(1.7)',
      }, '-=0.3');
      tl.fromTo('.dev-hero-links', { opacity: 0 }, { opacity: 1, duration: 0.5, ease: 'expo.out' }, '-=0.2');
    },
    { scope: heroRef },
  );

  /* ── Section reveal animations ── */
  useGSAP(
    () => {
      // Architecture section
      gsap.fromTo('.arch-header', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, ease: 'expo.out',
        scrollTrigger: { trigger: '.arch-header', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Spec header
      gsap.fromTo('.spec-header', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, ease: 'expo.out',
        scrollTrigger: { trigger: '.spec-header', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // MCP section
      gsap.fromTo('.mcp-header', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, ease: 'expo.out',
        scrollTrigger: { trigger: '.mcp-header', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Data flow
      gsap.fromTo('.flow-header', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, ease: 'expo.out',
        scrollTrigger: { trigger: '.flow-header', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Workshop
      gsap.fromTo('.workshop-header', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, ease: 'expo.out',
        scrollTrigger: { trigger: '.workshop-header', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Install
      gsap.fromTo('.install-header', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, ease: 'expo.out',
        scrollTrigger: { trigger: '.install-header', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // API
      gsap.fromTo('.api-header', { y: 40, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.7, ease: 'expo.out',
        scrollTrigger: { trigger: '.api-header', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Repo tree
      gsap.fromTo('.repo-tree', { y: 30, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.6, ease: 'expo.out',
        scrollTrigger: { trigger: '.repo-tree', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Env table
      gsap.fromTo('.env-table-row', { x: -20, opacity: 0 }, {
        x: 0, opacity: 1, duration: 0.4, stagger: 0.05, ease: 'expo.out',
        scrollTrigger: { trigger: '.env-table', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // API table rows
      gsap.fromTo('.api-table-row', { x: -20, opacity: 0 }, {
        x: 0, opacity: 1, duration: 0.4, stagger: 0.05, ease: 'expo.out',
        scrollTrigger: { trigger: '.api-table', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // CLI table rows
      gsap.fromTo('.cli-table-row', { x: -20, opacity: 0 }, {
        x: 0, opacity: 1, duration: 0.4, stagger: 0.05, ease: 'expo.out',
        scrollTrigger: { trigger: '.cli-table', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Workshop materials
      gsap.fromTo('.workshop-card', { y: 30, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: 'expo.out',
        scrollTrigger: { trigger: '.workshop-cards', start: 'top 85%', toggleActions: 'play none none none' },
      });

      // Workshop format table
      gsap.fromTo('.format-table-row', { x: -20, opacity: 0 }, {
        x: 0, opacity: 1, duration: 0.4, stagger: 0.05, ease: 'expo.out',
        scrollTrigger: { trigger: '.format-table', start: 'top 85%', toggleActions: 'play none none none' },
      });
    },
    { scope: pageRef },
  );

  const techBadges = ['TypeScript', 'MCP Protocol', 'Stripe API', 'Envidia', 'Google Workspace'];
  const badgeColors: Record<string, string> = {
    TypeScript: '#4A90A4',
    'MCP Protocol': '#D4A853',
    'Stripe API': '#635BFF',
    Envidia: '#76B900',
    'Google Workspace': '#FFB800',
  };

  /* Sequence data */
  const flow1 = [
    { from: 'Customer', to: 'Stripe', label: 'Purchase completed' },
    { from: 'Stripe', to: 'Collector', label: 'webhook: payment.success' },
    { from: 'Collector', to: 'Brain', label: 'mcp.context.share(payment_data)' },
    { from: 'Brain', to: 'Scribe', label: 'mcp.context.request(financial_update)' },
    { from: 'Scribe', to: 'Sheets', label: 'Update revenue dashboard' },
    { from: 'Brain', to: 'Herald', label: 'mcp.insight.push(high_performing_product)' },
    { from: 'Herald', to: 'Social', label: 'Boost campaign for product' },
  ];

  const flow2 = [
    { from: 'Calendar', to: 'Strategist', label: 'Meeting scheduled' },
    { from: 'Strategist', to: 'Brain', label: 'mcp.context.share(meeting_notes)' },
    { from: 'Brain', to: 'Diplomat', label: 'mcp.context.request(client_context)' },
    { from: 'Diplomat', to: 'CRM', label: 'Log interaction' },
    { from: 'Brain', to: 'Strategist', label: 'mcp.insight.push(follow_up_tasks)' },
    { from: 'Strategist', to: 'Calendar', label: 'Create follow-up reminders' },
  ];

  const flow3 = [
    { from: 'Envidia', to: 'Guardian', label: 'Anomaly detected' },
    { from: 'Guardian', to: 'Brain', label: 'mcp.context.share(security_alert)' },
    { from: 'Brain', to: 'All Heroes', label: 'mcp.observe(security_status)' },
    { from: 'Guardian', to: 'Vault', label: 'Rotate affected keys' },
    { from: 'Brain', to: 'Hermes', label: 'mcp.insight.push(incident_report)' },
  ];

  return (
    <div ref={pageRef}>
      {/* Inject syntax highlighting styles */}
      <style>{`
        .sh-keyword { color: ${'#C586C0'}; }
        .sh-type { color: ${'#4EC9B0'}; }
        .sh-string { color: ${'#CE9178'}; }
        .sh-comment { color: ${'#6A9955'}; }
        .sh-number { color: ${'#B5CEA8'}; }
        .sh-boolean { color: ${'#569CD6'}; }
        .sh-prop { color: ${'#9CDCFE'}; }
      `}</style>

      {/* ═══════════════════════════════════════════
          SECTION 1: Technical Hero
          ═══════════════════════════════════════════ */}
      <section
        ref={heroRef}
        data-dark-section
        className="relative flex flex-col items-center justify-center text-center overflow-hidden"
        style={{
          minHeight: '100dvh',
          backgroundColor: '#1A1A1E',
          padding: 'clamp(6rem, 12vh, 10rem) 1rem clamp(4rem, 8vh, 6rem)',
        }}
      >
        {/* Grid background */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundImage: 'linear-gradient(rgba(99,91,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(99,91,255,0.04) 1px, transparent 1px)',
            backgroundSize: '30px 30px',
          }}
        />

        {/* Floating particles */}
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full pointer-events-none"
            style={{
              width: `${2 + Math.random() * 4}px`,
              height: `${2 + Math.random() * 4}px`,
              backgroundColor: 'rgba(99,91,255,0.15)',
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animation: `float ${6 + Math.random() * 8}s ease-in-out infinite`,
              animationDelay: `${Math.random() * 5}s`,
            }}
          />
        ))}

        <div className="relative z-10" style={{ maxWidth: 'var(--container-narrow)' }}>
          {/* Eyebrow */}
          <span
            className="dev-hero-eyebrow inline-block font-mono text-sm mb-6"
            style={{ color: '#76B900', letterSpacing: '0.08em' }}
          >
            TECHNICAL DOCUMENTATION / v1.0.0
          </span>

          {/* Headline */}
          <h1
            className="dev-hero-headline font-cinzel mb-6"
            style={{
              fontSize: 'clamp(3rem, 8vw, 7rem)',
              letterSpacing: '0.08em',
              lineHeight: 1.05,
              color: '#F7F5F0',
            }}
          >
            THE ARCHITECTURE
            <br />
            OF HEROES
          </h1>

          {/* Subtitle */}
          <p
            className="dev-hero-subtitle font-inter text-lg leading-relaxed mb-8"
            style={{ color: 'rgba(247,245,240,0.6)', maxWidth: '600px', margin: '0 auto 2rem' }}
          >
            A comprehensive technical reference for The Parten\u00f3n system — Model Context Protocol design, agent specifications, integration patterns, and deployment guides.
          </p>

          {/* Tech badges */}
          <div className="flex flex-wrap justify-center gap-3 mb-8">
            {techBadges.map((badge) => (
              <span
                key={badge}
                className="dev-hero-badge font-mono text-xs px-4 py-2 rounded-full"
                style={{
                  border: `1px solid ${badgeColors[badge]}60`,
                  color: '#F7F5F0',
                  backgroundColor: 'transparent',
                }}
              >
                {badge}
              </span>
            ))}
          </div>

          {/* Anchor links */}
          <div className="dev-hero-links">
            <span className="font-inter text-xs" style={{ color: 'rgba(247,245,240,0.4)' }}>
              JUMP TO:{''}
              {['Architecture', 'Heroes', 'MCP', 'Workshop', 'Install'].map((link, i, arr) => (
                <span key={link}>
                  <button
                    onClick={() => scrollTo(link.toLowerCase())}
                    className="ml-1 transition-colors duration-200 hover:text-[#635BFF]"
                    style={{ color: 'rgba(247,245,240,0.4)' }}
                  >
                    {link}
                  </button>
                  {i < arr.length - 1 && <span>,</span>}
                </span>
              ))}
            </span>
          </div>
        </div>

        {/* CSS for floating animation */}
        <style>{`
          @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
          }
        `}</style>
      </section>

      {/* ═══════════════════════════════════════════
          SECTION 2: System Architecture Overview
          ═══════════════════════════════════════════ */}
      <section
        id="architecture"
        className="w-full"
        style={{
          backgroundColor: '#F7F5F0',
          padding: 'var(--section-pad-y) 0',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
          <div className="arch-header">
            <SectionHeader
              eyebrow="ARCHITECTURE"
              headline="HOW THE PARTEN\u00d3N IS BUILT"
              description="A layered architecture connecting intelligent agents through the Model Context Protocol, unified by G-Brain and deployed on enterprise-grade infrastructure."
              eyebrowColor="#635BFF"
              textColor="#2A2A2E"
              dividerColor="#635BFF"
            />
          </div>
          <ArchitectureDiagram />
        </div>
      </section>

      {/* ═══════════════════════════════════════════
          SECTION 3: Hero Technical Specifications
          ═══════════════════════════════════════════ */}
      <section id="heroes">
        <div
          className="spec-header"
          style={{
            backgroundColor: '#F7F5F0',
            padding: 'var(--section-pad-y) 0 2rem',
          }}
        >
          <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
            <SectionHeader
              eyebrow="AGENT SPECIFICATIONS"
              headline="HERO TECHNICAL PROFILES"
              description="Each hero is a specialized agent with defined capabilities, MCP tools, API integrations, and file format handlers."
              eyebrowColor="#76B900"
              textColor="#2A2A2E"
              dividerColor="#76B900"
            />
          </div>
        </div>

        {heroes.map((hero, i) => (
          <HeroSpecCard key={hero.key} hero={hero} index={i} />
        ))}
      </section>

      {/* ═══════════════════════════════════════════
          SECTION 4: MCP Protocol Deep Dive
          ═══════════════════════════════════════════ */}
      <section
        id="mcp"
        data-dark-section
        style={{
          backgroundColor: '#2A2A2E',
          padding: 'var(--section-pad-y) 0',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
          <div className="mcp-header">
            <SectionHeader
              eyebrow="MODEL CONTEXT PROTOCOL"
              headline="THE NERVOUS SYSTEM"
              description="MCP is the protocol that transforms individual agents into a collective intelligence. Here's how it works inside The Parten\u00f3n."
              eyebrowColor="#D4A853"
              textColor="#F7F5F0"
              dividerColor="#D4A853"
            />
          </div>

          {/* MCP Architecture Diagram */}
          <div className="mb-16">
            <MCPDiagram />
          </div>

          {/* Protocol Flow Steps */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
            {[
              {
                step: '01',
                title: 'Context Registration',
                color: '#4A90A4',
                code: `await brain.registerContext({\n  agent: 'scribe',\n  type: 'financial_model',\n  data: financeFile,\n  access: ['herald', 'strategist', 'brain'],\n  ttl: '30d'\n});`,
              },
              {
                step: '02',
                title: 'Cross-Agent Discovery',
                color: '#9B59B6',
                code: `const context = await brain.discover({\n  requestedBy: 'herald',\n  type: 'financial_model',\n  scope: 'latest'\n});\n// Returns: The Scribe's financial data`,
              },
              {
                step: '03',
                title: 'Insight Generation',
                color: '#D4A853',
                code: `const insight = await brain.generateInsight({\n  pattern: 'correlation',\n  sources: ['scribe.revenue', \n    'herald.campaigns', \n    'collector.payments'],\n  output: 'optimization_report'\n});`,
              },
            ].map((item) => (
              <div
                key={item.step}
                className="rounded-lg overflow-hidden"
                style={{
                  backgroundColor: '#1A1A1E',
                  border: `1px solid ${item.color}25`,
                }}
              >
                <div className="px-5 py-3 flex items-center gap-3" style={{ borderBottom: `1px solid ${item.color}20` }}>
                  <span className="font-mono text-lg font-bold" style={{ color: item.color }}>{item.step}</span>
                  <span className="font-inter text-sm font-semibold" style={{ color: '#F7F5F0' }}>{item.title}</span>
                </div>
                <div className="p-4">
                  <CodeBlock code={item.code} dark />
                </div>
              </div>
            ))}
          </div>

          {/* MCP Protocol Schema Table */}
          <div>
            <h3 className="font-cinzel text-lg mb-6 text-center" style={{ color: '#F7F5F0', letterSpacing: '0.06em' }}>
              PROTOCOL METHODS
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left" style={{ minWidth: '700px' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid rgba(212,168,83,0.3)' }}>
                    {['Method', 'Direction', 'Purpose', 'Payload'].map((h) => (
                      <th key={h} className="font-inter text-xs font-semibold tracking-wide uppercase py-3 pr-4" style={{ color: '#D4A853' }}>
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[
                    { method: 'mcp.register()', dir: 'Hero \u2192 Brain', purpose: 'Register agent capabilities', payload: 'Agent config, tools, permissions' },
                    { method: 'mcp.context.share()', dir: 'Hero \u2192 Brain', purpose: 'Share work output', payload: 'Context type, data, access rules' },
                    { method: 'mcp.context.request()', dir: 'Hero \u2192 Brain', purpose: 'Request shared context', payload: 'Context type, filters' },
                    { method: 'mcp.observe()', dir: 'Brain \u2192 Hero', purpose: 'Subscribe to events', payload: 'Event patterns, callbacks' },
                    { method: 'mcp.insight.push()', dir: 'Brain \u2192 Hero', purpose: 'Deliver insights', payload: 'Insight data, confidence, actions' },
                    { method: 'mcp.tool.call()', dir: 'Brain \u2192 External', purpose: 'Execute external tool', payload: 'Tool name, parameters, auth' },
                  ].map((row, i) => (
                    <tr key={i} style={{ borderBottom: '1px solid rgba(247,245,240,0.06)' }}>
                      <td className="font-mono text-sm py-3 pr-4" style={{ color: '#F7F5F0' }}>{row.method}</td>
                      <td className="font-inter text-xs py-3 pr-4" style={{ color: 'rgba(247,245,240,0.6)' }}>{row.dir}</td>
                      <td className="font-inter text-sm py-3 pr-4" style={{ color: 'rgba(247,245,240,0.8)' }}>{row.purpose}</td>
                      <td className="font-inter text-xs py-3" style={{ color: 'rgba(247,245,240,0.5)' }}>{row.payload}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* MCP JSON-RPC example */}
          <div className="mt-12">
            <h3 className="font-cinzel text-lg mb-4 text-center" style={{ color: '#F7F5F0', letterSpacing: '0.06em' }}>
              JSON-RPC REQUEST EXAMPLE
            </h3>
            <div className="mx-auto" style={{ maxWidth: '600px' }}>
              <CodeBlock
                code={`{\n  "jsonrpc": "2.0",\n  "method": "tools/call",\n  "params": {\n    "name": "google_sheets_query",\n    "arguments": {\n      "spreadsheetId": "...",\n      "range": "A1:D100"\n    }\n  }\n}`}
                dark
              />
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════
          SECTION 5: Data Flow & Integration Patterns
          ═══════════════════════════════════════════ */}
      <section
        id="flow"
        style={{
          backgroundColor: '#F7F5F0',
          padding: 'var(--section-pad-y) 0',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
          <div className="flow-header">
            <SectionHeader
              eyebrow="INTEGRATION PATTERNS"
              headline="HOW DATA FLOWS THROUGH THE PARTEN\u00d3N"
              eyebrowColor="#635BFF"
              textColor="#2A2A2E"
              dividerColor="#635BFF"
            />
          </div>

          {/* Flow 1 */}
          <div className="mb-16">
            <h3 className="font-inter text-base font-semibold mb-4 flex items-center gap-2" style={{ color: '#2A2A2E' }}>
              <Zap className="h-5 w-5 text-[#FFB800]" />
              Example 1: Sale \u2192 Financial Update \u2192 Marketing
            </h3>
            <SequenceDiagram steps={flow1} />
          </div>

          {/* Flow 2 */}
          <div className="mb-16">
            <h3 className="font-inter text-base font-semibold mb-4 flex items-center gap-2" style={{ color: '#2A2A2E' }}>
              <Calendar className="h-5 w-5 text-[#4A90A4]" />
              Example 2: Meeting \u2192 Tasks \u2192 Follow-up
            </h3>
            <SequenceDiagram steps={flow2} />
          </div>

          {/* Flow 3 */}
          <div className="mb-16">
            <h3 className="font-inter text-base font-semibold mb-4 flex items-center gap-2" style={{ color: '#2A2A2E' }}>
              <Shield className="h-5 w-5 text-[#76B900]" />
              Example 3: Security Alert \u2192 System Response
            </h3>
            <SequenceDiagram steps={flow3} />
          </div>

          {/* Google Drive Structure */}
          <div>
            <h3 className="font-inter text-base font-semibold mb-4 flex items-center gap-2" style={{ color: '#2A2A2E' }}>
              <Database className="h-5 w-5 text-[#4285F4]" />
              Google Workspace File Structure
            </h3>
            <div
              className="rounded-lg p-6 overflow-x-auto"
              style={{ backgroundColor: '#1A1A1E', border: '1px solid rgba(247,245,240,0.08)' }}
            >
              <pre className="font-mono text-[0.8125rem] leading-[1.8]" style={{ color: '#F7F5F0' }}>
{`Google Drive / The Parten\u00f3n /
\u251C\u2500\u2500 \uD83D\uDCC1 enterprises/
\u2502   \u2514\u2500\u2500 \uD83D\uDCC1 {enterprise-name}/
\u2502       \u251C\u2500\u2500 \uD83D\uDCC4 enterprise.finance      \u2190 Scribe
\u2502       \u251C\u2500\u2500 \uD83D\uDCC4 enterprise.design       \u2190 Herald
\u2502       \u251C\u2500\u2500 \uD83D\uDCC4 enterprise.revenue      \u2190 Collector
\u2502       \u251C\u2500\u2500 \uD83D\uDCC4 enterprise.security     \u2190 Guardian
\u2502       \u251C\u2500\u2500 \uD83D\uDCC4 enterprise.operations   \u2190 Strategist
\u2502       \u251C\u2500\u2500 \uD83D\uDCC4 enterprise.relations    \u2190 Diplomat
\u2502       \u251C\u2500\u2500 \uD83D\uDCC4 enterprise.brain        \u2190 Brain
\u2502       \u2514\u2500\u2500 \uD83D\uDCC1 shared/
\u2502           \u251C\u2500\u2500 \uD83D\uDCC1 dashboards/
\u2502           \u251C\u2500\u2500 \uD83D\uDCC1 campaigns/
\u2502           \u251C\u2500\u2500 \uD83D\uDCC1 reports/
\u2502           \u2514\u2500\u2500 \uD83D\uDCC1 meetings/
\u251C\u2500\u2500 \uD83D\uDCC1 templates/
\u2502   \u251C\u2500\u2500 \uD83D\uDCC4 default.finance
\u2502   \u251C\u2500\u2500 \uD83D\uDCC4 default.design
\u2502   \u2514\u2500\u2500 \uD83D\uDCC4 default.operations
\u2514\u2500\u2500 \uD83D\uDCC1 archive/`}
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════
          SECTION 6: Workshop Technical Structure
          ═══════════════════════════════════════════ */}
      <section
        id="workshop"
        style={{
          backgroundColor: '#EDE8DF',
          padding: 'var(--section-pad-y) 0',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
          <div className="workshop-header">
            <SectionHeader
              eyebrow="WORKSHOP PROTOCOL"
              headline="THE 2-HOUR HERMES INSTALL SESSION"
              eyebrowColor="#FFB800"
              textColor="#2A2A2E"
              dividerColor="#FFB800"
            />
          </div>

          {/* Timeline */}
          <div className="mb-16">
            <WorkshopTimeline />
          </div>

          {/* Pre-workshop checklist */}
          <div className="mb-16">
            <h3 className="font-inter text-sm font-semibold tracking-[0.08em] uppercase mb-4" style={{ color: '#2A2A2E' }}>
              Pre-Workshop Checklist
            </h3>
            <CodeBlock
              code={`# Pre-workshop requirements
$ node --version  # >= 20.0.0
$ npm --version   # >= 10.0.0

# Required accounts (free tier acceptable)
# \u2713 Google account (for Workspace integration)
# \u2713 Stripe account (test mode for development)
# \u2713 Envidia account (API key for security features)

# One-line installation
$ npx create-hermes@latest my-partenon
$ cd my-partenon
$ hermes configure --interactive`}
              dark={false}
            />
          </div>

          {/* Workshop materials */}
          <div className="workshop-cards grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            {[
              {
                title: 'Workshop Slides',
                desc: 'Complete presentation deck for facilitators. Covers Parten\u00f3n concept, hero introductions, live demo script, and troubleshooting guide.',
                color: '#4A90A4',
              },
              {
                title: 'Participant Handbook',
                desc: 'PDF guide for workshop attendees. Step-by-step installation instructions, hero configuration cheat sheet, and FAQ.',
                color: '#9B59B6',
              },
              {
                title: 'Facilitator Script',
                desc: 'Detailed speaking notes for workshop leaders. Timing cues, talking points, and interaction prompts for each phase.',
                color: '#76B900',
              },
            ].map((card) => (
              <div
                key={card.title}
                className="workshop-card rounded-lg p-6 transition-all duration-300 hover:-translate-y-1"
                style={{
                  backgroundColor: '#F7F5F0',
                  border: `1px solid ${card.color}20`,
                  boxShadow: '0 4px 16px rgba(42,42,46,0.06)',
                }}
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className="h-8 w-8 rounded-md flex items-center justify-center" style={{ backgroundColor: `${card.color}15` }}>
                    <FileJson className="h-4 w-4" style={{ color: card.color }} />
                  </div>
                  <h4 className="font-inter text-base font-semibold" style={{ color: '#2A2A2E' }}>{card.title}</h4>
                </div>
                <p className="font-inter text-sm leading-relaxed mb-4" style={{ color: '#6B6B73' }}>
                  {card.desc}
                </p>
                <button
                  className="inline-flex items-center gap-1 font-inter text-sm font-medium transition-colors duration-200 hover:opacity-80"
                  style={{ color: card.color }}
                  onClick={() => alert('Coming soon!')}
                >
                  <Download className="h-4 w-4" />
                  Download
                </button>
              </div>
            ))}
          </div>

          {/* Workshop formats table */}
          <div className="format-table overflow-x-auto">
            <h3 className="font-inter text-sm font-semibold tracking-[0.08em] uppercase mb-4" style={{ color: '#2A2A2E' }}>
              Workshop Formats
            </h3>
            <table className="w-full text-left" style={{ minWidth: '700px' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid rgba(42,42,46,0.15)' }}>
                  {['Format', 'Duration', 'Audience', 'Capacity', 'Requirements'].map((h) => (
                    <th key={h} className="font-inter text-xs font-semibold tracking-wide uppercase py-3 pr-4" style={{ color: '#FFB800' }}>
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[
                  { format: 'Webinar (Virtual)', duration: '2 hours', audience: 'Global entrepreneurs', capacity: '500', req: 'Zoom + screen share' },
                  { format: 'University Session', duration: '3 hours', audience: 'Students & faculty', capacity: '100', req: 'Computer lab + projector' },
                  { format: 'Coworking Workshop', duration: '2.5 hours', audience: 'Coworking members', capacity: '30', req: 'Meeting room + WiFi' },
                  { format: 'BNI Chapter Meet', duration: '2 hours', audience: 'Business network', capacity: '25', req: 'Conference room' },
                  { format: 'Accelerator Cohort', duration: 'Full day', audience: 'Startup teams', capacity: '20', req: 'Workshop space + mentors' },
                ].map((row, i) => (
                  <tr key={i} className="format-table-row" style={{ borderBottom: '1px solid rgba(42,42,46,0.08)' }}>
                    <td className="font-inter text-sm py-3 pr-4" style={{ color: '#2A2A2E' }}>{row.format}</td>
                    <td className="font-mono text-xs py-3 pr-4" style={{ color: '#6B6B73' }}>{row.duration}</td>
                    <td className="font-inter text-sm py-3 pr-4" style={{ color: '#6B6B73' }}>{row.audience}</td>
                    <td className="font-mono text-sm py-3 pr-4" style={{ color: '#2A2A2E' }}>{row.capacity}</td>
                    <td className="font-inter text-xs py-3" style={{ color: '#6B6B73' }}>{row.req}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════
          SECTION 7: Repository & Installation
          ═══════════════════════════════════════════ */}
      <section
        id="install"
        data-dark-section
        style={{
          backgroundColor: '#1A1A1E',
          padding: 'var(--section-pad-y) 0',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
          <div className="install-header">
            <SectionHeader
              eyebrow="GET STARTED"
              headline="INSTALL HERMES IN ONE COMMAND"
              eyebrowColor="#635BFF"
              textColor="#F7F5F0"
              dividerColor="#635BFF"
            />
          </div>

          {/* Install tabs */}
          <div className="mb-16">
            <InstallTabs />
          </div>

          {/* Repository structure */}
          <div className="repo-tree mb-16">
            <h3 className="font-cinzel text-lg mb-4 text-center" style={{ color: '#F7F5F0', letterSpacing: '0.06em' }}>
              REPOSITORY STRUCTURE
            </h3>
            <div
              className="rounded-lg p-6 overflow-x-auto mx-auto"
              style={{
                maxWidth: '700px',
                backgroundColor: '#1A1A1E',
                border: '1px solid rgba(247,245,240,0.08)',
              }}
            >
              <pre className="font-mono text-[0.8125rem] leading-[1.8]" style={{ color: '#F7F5F0' }}>
{`the-partenon/
\u251C\u2500\u2500 \uD83D\uDCC1 apps/
\u2502   \u251C\u2500\u2500 \uD83D\uDCC1 hermes/           # Main orchestrator
\u2502   \u251C\u2500\u2500 \uD83D\uDCC1 web/              # Next.js marketing site
\u2502   \u2514\u2500\u2500 \uD83D\uDCC1 dashboard/        # React admin dashboard
\u251C\u2500\u2500 \uD83D\uDCC1 packages/
\u2502   \u251C\u2500\u2500 \uD83D\uDCC1 mcp-sdk/          # Model Context Protocol SDK
\u2502   \u251C\u2500\u2500 \uD83D\uDCC1 heroes/
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 scribe/       # sheets-mcp
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 herald/       # comms-mcp
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 collector/    # stripe-mcp
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 guardian/     # security-mcp
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 strategist/   # ops-mcp
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 diplomat/     # crm-mcp
\u2502   \u2502   \u2514\u2500\u2500 \uD83D\uDCC1 brain/        # gbrain-mcp
\u2502   \u251C\u2500\u2500 \uD83D\uDCC1 shared/
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 types/        # Shared TypeScript types
\u2502   \u2502   \u251C\u2500\u2500 \uD83D\uDCC1 config/       # Configuration schemas
\u2502   \u2502   \u2514\u2500\u2500 \uD83D\uDCC1 utils/        # Common utilities
\u2502   \u2514\u2500\u2500 \uD83D\uDCC1 ui/               # Shared UI components
\u251C\u2500\u2500 \uD83D\uDCC1 workshops/
\u2502   \u251C\u2500\u2500 \uD83D\uDCC1 slides/           # Presentation decks
\u2502   \u251C\u2500\u2500 \uD83D\uDCC1 handbooks/        # Participant guides
\u2502   \u2514\u2500\u2500 \uD83D\uDCC1 facilitator/      # Leader scripts
\u251C\u2500\u2500 \uD83D\uDCC4 README.md
\u251C\u2500\u2500 \uD83D\uDCC4 CONTRIBUTING.md
\u251C\u2500\u2500 \uD83D\uDCC4 LICENSE (MIT)
\u2514\u2500\u2500 \uD83D\uDCC4 package.json`}
              </pre>
            </div>
          </div>

          {/* Environment variables table */}
          <div className="env-table">
            <h3 className="font-cinzel text-lg mb-4 text-center" style={{ color: '#F7F5F0', letterSpacing: '0.06em' }}>
              ENVIRONMENT VARIABLES
            </h3>
            <div className="overflow-x-auto mx-auto" style={{ maxWidth: '800px' }}>
              <table className="w-full text-left" style={{ minWidth: '600px' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid rgba(99,91,255,0.3)' }}>
                    {['Variable', 'Required', 'Description', 'Example'].map((h) => (
                      <th key={h} className="font-inter text-xs font-semibold tracking-wide uppercase py-3 pr-4" style={{ color: '#635BFF' }}>
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[
                    { var: 'GOOGLE_CLIENT_ID', req: 'Yes', desc: 'Google OAuth client ID', ex: '123-abc.apps.googleusercontent.com' },
                    { var: 'GOOGLE_CLIENT_SECRET', req: 'Yes', desc: 'Google OAuth secret', ex: 'GOCSPX-...' },
                    { var: 'STRIPE_SECRET_KEY', req: 'Yes', desc: 'Stripe API key', ex: 'sk_test_...' },
                    { var: 'STRIPE_WEBHOOK_SECRET', req: 'Yes', desc: 'Stripe webhook endpoint secret', ex: 'whsec_...' },
                    { var: 'ENVIDIA_API_KEY', req: 'Yes', desc: 'Envidia platform API key', ex: 'nv-...' },
                    { var: 'OPENAI_API_KEY', req: 'Optional', desc: 'OpenAI for advanced features', ex: 'sk-...' },
                    { var: 'MCP_PORT', req: 'No', desc: 'MCP server port (default: 3001)', ex: '3001' },
                    { var: 'HERMES_ENV', req: 'No', desc: 'Environment (dev/staging/prod)', ex: 'development' },
                  ].map((row, i) => (
                    <tr key={i} className="env-table-row" style={{ borderBottom: '1px solid rgba(247,245,240,0.06)' }}>
                      <td className="font-mono text-sm py-3 pr-4" style={{ color: '#F7F5F0' }}>{row.var}</td>
                      <td className="font-inter text-xs py-3 pr-4" style={{ color: row.req === 'Yes' ? '#76B900' : 'rgba(247,245,240,0.5)' }}>{row.req}</td>
                      <td className="font-inter text-sm py-3 pr-4" style={{ color: 'rgba(247,245,240,0.7)' }}>{row.desc}</td>
                      <td className="font-mono text-xs py-3" style={{ color: 'rgba(247,245,240,0.4)' }}>{row.ex}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════
          SECTION 8: API Reference & Status
          ═══════════════════════════════════════════ */}
      <section
        id="api"
        style={{
          backgroundColor: '#F7F5F0',
          padding: 'var(--section-pad-y) 0',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 'var(--container-max)' }}>
          <div className="api-header">
            <SectionHeader
              eyebrow="API REFERENCE"
              headline="HERMES COMMAND LINE INTERFACE"
              eyebrowColor="#76B900"
              textColor="#2A2A2E"
              dividerColor="#76B900"
            />
          </div>

          {/* CLI Commands Table */}
          <div className="cli-table mb-16">
            <h3 className="font-inter text-sm font-semibold tracking-[0.08em] uppercase mb-4" style={{ color: '#2A2A2E' }}>
              CLI Commands
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left" style={{ minWidth: '600px' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid rgba(118,185,0,0.3)' }}>
                    {['Command', 'Description', 'Example'].map((h) => (
                      <th key={h} className="font-inter text-xs font-semibold tracking-wide uppercase py-3 pr-4" style={{ color: '#76B900' }}>
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[
                    { cmd: 'hermes init', desc: 'Initialize new enterprise', ex: 'hermes init --name "Cafe Central"' },
                    { cmd: 'hermes activate', desc: 'Activate a hero', ex: 'hermes activate scribe' },
                    { cmd: 'hermes deactivate', desc: 'Deactivate a hero', ex: 'hermes deactivate herald' },
                    { cmd: 'hermes mission', desc: 'Start a hero mission', ex: 'hermes mission scribe --type financial-model' },
                    { cmd: 'hermes status', desc: 'Check system status', ex: 'hermes status --verbose' },
                    { cmd: 'hermes dashboard', desc: 'Open web dashboard', ex: 'hermes dashboard --port 3000' },
                    { cmd: 'hermes test', desc: 'Run integration tests', ex: 'hermes test --all' },
                    { cmd: 'hermes deploy', desc: 'Deploy to production', ex: 'hermes deploy --target vercel' },
                    { cmd: 'hermes logs', desc: 'View system logs', ex: 'hermes logs --follow --hero scribe' },
                    { cmd: 'hermes config', desc: 'Edit configuration', ex: 'hermes config --edit' },
                    { cmd: 'hermes backup', desc: 'Backup enterprise data', ex: 'hermes backup --to google-drive' },
                  ].map((row, i) => (
                    <tr key={i} className="cli-table-row" style={{ borderBottom: '1px solid rgba(42,42,46,0.08)' }}>
                      <td className="font-mono text-sm py-3 pr-4" style={{ color: '#2A2A2E' }}>{row.cmd}</td>
                      <td className="font-inter text-sm py-3 pr-4" style={{ color: '#6B6B73' }}>{row.desc}</td>
                      <td className="font-mono text-xs py-3" style={{ color: '#635BFF' }}>{row.ex}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* REST API Endpoints */}
          <div className="api-table mb-16">
            <h3 className="font-inter text-sm font-semibold tracking-[0.08em] uppercase mb-4" style={{ color: '#2A2A2E' }}>
              REST API Endpoints
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left" style={{ minWidth: '600px' }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid rgba(99,91,255,0.3)' }}>
                    {['Endpoint', 'Method', 'Description'].map((h) => (
                      <th key={h} className="font-inter text-xs font-semibold tracking-wide uppercase py-3 pr-4" style={{ color: '#635BFF' }}>
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[
                    { endpoint: '/api/v1/heroes', method: 'GET', desc: 'List all heroes' },
                    { endpoint: '/api/v1/heroes/:id', method: 'GET', desc: 'Get hero details' },
                    { endpoint: '/api/v1/missions', method: 'POST', desc: 'Create new mission' },
                    { endpoint: '/api/v1/missions/:id', method: 'GET', desc: 'Get mission status' },
                    { endpoint: '/api/v1/mcp/tools', method: 'GET', desc: 'List available MCP tools' },
                    { endpoint: '/api/v1/mcp/call', method: 'POST', desc: 'Call MCP tool' },
                  ].map((row, i) => (
                    <tr key={i} className="api-table-row" style={{ borderBottom: '1px solid rgba(42,42,46,0.08)' }}>
                      <td className="font-mono text-sm py-3 pr-4" style={{ color: '#2A2A2E' }}>{row.endpoint}</td>
                      <td className="font-mono text-xs py-3 pr-4">
                        <span
                          className="px-2 py-0.5 rounded"
                          style={{
                            backgroundColor: row.method === 'GET' ? '#4A90A420' : '#635BFF20',
                            color: row.method === 'GET' ? '#4A90A4' : '#635BFF',
                          }}
                        >
                          {row.method}
                        </span>
                      </td>
                      <td className="font-inter text-sm py-3" style={{ color: '#6B6B73' }}>{row.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* System Status */}
          <div className="mb-16">
            <h3 className="font-inter text-sm font-semibold tracking-[0.08em] uppercase mb-4 text-center" style={{ color: '#2A2A2E' }}>
              System Status Response
            </h3>
            <div className="mx-auto" style={{ maxWidth: '600px' }}>
              <CodeBlock
                code={`{\n  "status": "healthy",\n  "version": "1.0.0",\n  "heroes": {\n    "scribe": { "status": "active", "lastMission": "2025-01-15T10:30:00Z" },\n    "herald": { "status": "active", "lastMission": "2025-01-15T09:15:00Z" },\n    "collector": { "status": "active", "lastMission": "2025-01-15T08:45:00Z" },\n    "guardian": { "status": "active", "lastCheck": "2025-01-15T11:00:00Z" },\n    "strategist": { "status": "active", "lastMission": "2025-01-15T10:00:00Z" },\n    "diplomat": { "status": "active", "lastMission": "2025-01-14T16:30:00Z" },\n    "brain": { "status": "active", "insightsGenerated": 147 }\n  },\n  "mcp": {\n    "connectedAgents": 7,\n    "contextObjects": 23,\n    "lastInsight": "2025-01-15T10:55:00Z"\n  },\n  "integrations": {\n    "google_workspace": "connected",\n    "stripe": "connected",\n    "envidia": "connected"\n  }\n}`}
                dark={false}
              />
            </div>
          </div>

          {/* CTA */}
          <div className="text-center">
            <h3 className="font-cinzel text-2xl mb-4" style={{ color: '#2A2A2E', letterSpacing: '0.04em' }}>
              READY TO BUILD?
            </h3>
            <Link
              to="/"
              className="inline-flex items-center gap-2 rounded-pill px-8 py-3.5 font-inter text-sm font-semibold tracking-[0.04em] text-white transition-all duration-200 hover:scale-[1.02] hover:shadow-glow-indigo mb-4"
              style={{
                backgroundColor: '#635BFF',
                borderRadius: 'var(--radius-pill)',
              }}
            >
              INSTALL HERMES
              <ArrowRight className="h-4 w-4" />
            </Link>
            <p className="font-inter text-sm" style={{ color: '#6B6B73' }}>
              <button
                onClick={() => alert('Coming soon!')}
                className="transition-colors duration-200 hover:text-[#635BFF]"
                style={{ color: '#6B6B73' }}
              >
                View Full Documentation on GitHub &rarr;
              </button>
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
