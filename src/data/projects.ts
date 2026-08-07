export interface Project {
  title: string;
  name: string;
  description: string;
  articleUrl: string;
  repoUrl?: string;
  techStack: string[];
}

export const featuredProjects: Project[] = [
  {
    title: "BrailleBoard Web Application",
    name: "brailleboard",
    description: "Text-to-Braille conversion web application built with Appwrite backend, Next.js frontend, and Web Speech API for accessibility.",
    articleUrl: "https://networkandcode.hashnode.dev/text-to-braille-webpp-with-appwrite-nextjs-and-web-speech-api",
    repoUrl: "https://github.com/networkandcode/brailleboard",
    techStack: ["Next.js", "Appwrite", "Web Speech API", "React"]
  },
  {
    title: "CricScore - Cricket Scoring Web App",
    name: "cricscore",
    description: "Live cricket match scoring app with real-time score updates, match stats, and database management.",
    articleUrl: "https://dev.to/networkandcode/cricket-scoring-app-using-appwrite-nextjs-3730",
    repoUrl: "https://github.com/networkandcode/cricscore",
    techStack: ["Next.js", "Appwrite", "TailwindCSS", "Node.js"]
  },
  {
    title: "Notes App with Next.js & Serverless",
    name: "notes",
    description: "Full-stack notes application featuring instant search, dynamic tags, and cloud database persistence.",
    articleUrl: "https://dev.to/networkandcode/notes-app-with-nextjs-2l4g",
    repoUrl: "https://github.com/networkandcode/notes-app",
    techStack: ["Next.js", "Serverless", "React", "REST API"]
  },
  {
    title: "School Management System",
    name: "school admin",
    description: "Comprehensive school administrative dashboard deployed on Linode cloud with student records, attendance, and role-based access.",
    articleUrl: "https://networkandcode.hashnode.dev/school-admin-app-with-nextjs-on-linode",
    repoUrl: "https://github.com/networkandcode/sms",
    techStack: ["Next.js", "TypeScript", "Linode Cloud", "Docker"]
  },
  {
    title: "Online Shop with Next.js & HarperDB",
    name: "shop",
    description: "E-commerce web application backed by HarperDB NoSQL/SQL database and Next.js frontend rendering.",
    articleUrl: "https://networkandcode.hashnode.dev/online-shop-with-nextjs-and-harperdb",
    repoUrl: "https://github.com/networkandcode/shop",
    techStack: ["Next.js", "HarperDB", "GraphQL", "React"]
  }
];
