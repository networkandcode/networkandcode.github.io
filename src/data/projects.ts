export interface Project {
  title: string;
  name: string;
  description: string;
  articleUrl: string;
  repoUrl?: string;
  image?: string;
  techStack: string[];
}

export const featuredProjects: Project[] = [
  {
    title: "BoutiqueBot - Agentic AI Shopping Assistant",
    name: "boutiquebot",
    description: "AI-powered conversational shopping assistant demonstrating Model Context Protocol (MCP) agent workflows, Google Gemini integration, and an interactive Streamlit user interface.",
    articleUrl: "https://www.youtube.com/watch?v=LjT4EP2kYHo",
    repoUrl: "https://github.com/networkandcode/boutique-bot",
    image: "/images/projects/boutique_bot_screenshot.jpg",
    techStack: ["Gemini AI", "MCP-Agent", "Streamlit", "Python"]
  },
  {
    title: "BrailleBoard - Text to Braille Web App",
    name: "brailleboard",
    description: "Accessibility-focused web application that converts text to Braille, featuring speech-to-text input via Web Speech API, note management, and Appwrite backend authentication with OTP support.",
    articleUrl: "https://networkandcode.hashnode.dev/text-to-braille-webpp-with-appwrite-nextjs-and-web-speech-api",
    repoUrl: "https://github.com/networkandcode/brailleboard",
    image: "/images/projects/brailleboard_screenshot.jpg",
    techStack: ["Next.js", "Appwrite", "Web Speech API", "React"]
  },
  {
    title: "CricScore - Single-User Cricket Scoring App",
    name: "cricscore",
    description: "Single-user cricket match scoring application built to track and record match progress, manage overs, calculate run rates, and persist innings state in real-time to Appwrite database.",
    articleUrl: "https://dev.to/networkandcode/cricket-scoring-app-using-appwrite-nextjs-3730",
    repoUrl: "https://github.com/networkandcode/cricscore",
    image: "/images/projects/cricscore_screenshot.png",
    techStack: ["Next.js", "Appwrite", "TailwindCSS", "React Context"]
  },
  {
    title: "Notes App with Next.js & HarperDB",
    name: "notes",
    description: "Lightweight full-stack note-taking web application with Auth0 authentication, CRUD endpoints in Next.js API routes, instant client-side search filtering, and cloud persistence in HarperDB.",
    articleUrl: "https://dev.to/networkandcode/notes-app-with-nextjs-2l4g",
    repoUrl: "https://github.com/networkandcode/notes-app",
    image: "/images/projects/notes_app_screenshot.png",
    techStack: ["Next.js", "HarperDB", "Auth0", "Vercel"]
  },
  {
    title: "School Management & Admin App",
    name: "school admin",
    description: "School administrative management web application deployed on Linode cloud infrastructure, covering fundamental administrative workflows, student records, and server hosting configurations.",
    articleUrl: "https://networkandcode.hashnode.dev/school-admin-app-with-nextjs-on-linode",
    repoUrl: "https://github.com/networkandcode/sms",
    image: "/images/projects/school_admin_screenshot.jpg",
    techStack: ["Next.js", "Linode Cloud", "Docker", "Node.js"]
  },
  {
    title: "Online Shop with Next.js & HarperDB",
    name: "shop",
    description: "Turnkey e-commerce storefront supporting product catalogs, categories, cart management, HarperDB schema design with role-based security, and Stripe payment processing.",
    articleUrl: "https://networkandcode.hashnode.dev/online-shop-with-nextjs-and-harperdb",
    repoUrl: "https://github.com/networkandcode/shop",
    image: "/images/projects/shop_app_screenshot.jpg",
    techStack: ["Next.js", "HarperDB", "Stripe", "React"]
  }
];
