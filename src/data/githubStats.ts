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
    description: "AI conversational shopping assistant powered by Google Gemini, Model Context Protocol (MCP) agent framework, and Streamlit.",
    language: "Python / Streamlit",
    role: "Creator & Maintainer"
  },
  {
    name: "brailleboard",
    fullName: "networkandcode/brailleboard",
    url: "https://github.com/networkandcode/brailleboard",
    description: "Accessibility-focused web app converting text to Braille, built with Appwrite backend, Next.js, and Web Speech API.",
    language: "TypeScript / Next.js",
    role: "Creator & Lead Developer"
  },
  {
    name: "cricscore",
    fullName: "networkandcode/cricscore",
    url: "https://github.com/networkandcode/cricscore",
    description: "Single-user cricket match scoring app tracking live match statistics and state persistence with Appwrite and Next.js.",
    language: "TypeScript / Next.js",
    role: "Creator & Maintainer"
  },
  {
    name: "notes-app",
    fullName: "networkandcode/notes-app",
    url: "https://github.com/networkandcode/notes-app",
    description: "Full-stack note-taking web application with Auth0 authentication, Next.js API routes, and HarperDB database storage.",
    language: "TypeScript / Next.js",
    role: "Creator & Maintainer"
  },
  {
    name: "sms",
    fullName: "networkandcode/sms",
    url: "https://github.com/networkandcode/sms",
    description: "School administrative management application deployed on Linode cloud with student records and administrative workflows.",
    language: "TypeScript / Next.js",
    role: "Creator & Maintainer"
  }
];

export const monthlyContributions = [
  { month: "Sep 2025", count: 124 },
  { month: "Oct 2025", count: 90 },
  { month: "Nov 2025", count: 82 },
  { month: "Dec 2025", count: 75 },
  { month: "Jan 2026", count: 115 },
  { month: "Feb 2026", count: 130 },
  { month: "Mar 2026", count: 142 },
  { month: "Apr 2026", count: 168 },
  { month: "May 2026", count: 155 },
  { month: "Jun 2026", count: 190 },
  { month: "Jul 2026", count: 175 },
  { month: "Aug 2026", count: 142 }
];
