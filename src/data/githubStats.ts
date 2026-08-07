export interface ContributionStat {
  year: string;
  count: number;
  level: number;
}

export interface RepoSummary {
  totalRepos: number;
  topLanguages: { name: string; percentage: number; color: string }[];
  categories: { name: string; count: number }[];
}

export const githubProfileSummary: RepoSummary = {
  totalRepos: 64,
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
