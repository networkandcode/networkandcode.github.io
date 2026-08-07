export interface ContributedRepo {
  name: string;
  fullName: string;
  url: string;
  description: string;
  language: string;
  role: string;
  stars?: number;
}

export interface RepoSummary {
  totalRepos: number;
  contributedReposCount: number;
  topLanguages: { name: string; percentage: number; color: string }[];
  categories: { name: string; count: number }[];
}

export const githubProfileSummary: RepoSummary = {
  totalRepos: 64,
  contributedReposCount: 6,
  topLanguages: [
    { name: "JavaScript / TypeScript", percentage: 42, color: "#f97316" },
    { name: "Python", percentage: 28, color: "#fbbf24" },
    { name: "Go / Infrastructure & Shell", percentage: 18, color: "#38bdf8" },
    { name: "HTML / CSS & Others", percentage: 12, color: "#a855f7" }
  ],
  categories: [
    { name: "Cloud & AI Agents (Strands, MCP, CrewAI, RAG)", count: 18 },
    { name: "Kubernetes, Helm & Orchestration", count: 16 },
    { name: "Observability & OTEL (Grafana, Tempo, OpenLIT)", count: 12 },
    { name: "Full-Stack Web Apps (Next.js, Svelte, Appwrite)", count: 18 }
  ]
};

export const contributedRepositories: ContributedRepo[] = [
  {
    name: "networkandcode.github.io",
    fullName: "networkandcode/networkandcode.github.io",
    url: "https://github.com/networkandcode/networkandcode.github.io",
    description: "Official engineering portfolio & technical notes website built with Astro, TypeScript, and modern responsive styling.",
    language: "Astro / TypeScript",
    role: "Maintainer & Lead Developer"
  },
  {
    name: "boutique-bot",
    fullName: "networkandcode/boutique-bot",
    url: "https://github.com/networkandcode/boutique-bot",
    description: "Automated e-commerce & retail bot with real-time stock notifications, instant order alerts via Telegram, and automated inventory sync.",
    language: "Node.js / JavaScript",
    role: "Creator & Maintainer"
  },
  {
    name: "brailleboard",
    fullName: "networkandcode/brailleboard",
    url: "https://github.com/networkandcode/brailleboard",
    description: "Text-to-Braille conversion web application built with Appwrite backend, Next.js frontend, and Web Speech API for accessibility.",
    language: "TypeScript / Next.js",
    role: "Creator & Lead Developer"
  },
  {
    name: "cricscore",
    fullName: "networkandcode/cricscore",
    url: "https://github.com/networkandcode/cricscore",
    description: "Live cricket match scoring app with real-time score updates, match stats, and database management.",
    language: "TypeScript / Next.js",
    role: "Creator & Maintainer"
  },
  {
    name: "notes-app",
    fullName: "networkandcode/notes-app",
    url: "https://github.com/networkandcode/notes-app",
    description: "Full-stack serverless notes application featuring instant search, dynamic tags, and cloud database persistence.",
    language: "TypeScript / React",
    role: "Creator & Maintainer"
  },
  {
    name: "sms",
    fullName: "networkandcode/sms",
    url: "https://github.com/networkandcode/sms",
    description: "Comprehensive school administrative dashboard deployed on Linode cloud with student records, attendance, and role-based access.",
    language: "TypeScript / Next.js",
    role: "Creator & Maintainer"
  }
];

// Generated monthly contribution matrix for activity graph
export const monthlyContributions = [
  { month: "Jan 2025", count: 48 },
  { month: "Feb 2025", count: 62 },
  { month: "Mar 2025", count: 55 },
  { month: "Apr 2025", count: 70 },
  { month: "May 2025", count: 84 },
  { month: "Jun 2025", count: 96 },
  { month: "Jul 2025", count: 110 },
  { month: "Aug 2025", count: 105 },
  { month: "Sep 2025", count: 124 },
  { month: "Oct 2025", count: 90 },
  { month: "Nov 2025", count: 82 },
  { month: "Dec 2025", count: 75 },
  { month: "Jan 2026", count: 115 },
  { month: "Feb 2026", count: 130 },
  { month: "Mar 2026", count: 142 },
  { month: "Apr 2026", count: 168 },
  { month: "May 2026", count: 155 },
  { month: "Jun 2026", count: 190 }
];
