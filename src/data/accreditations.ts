export interface Accreditation {
  name: string;
  issuer: string;
  badgeUrl: string;
  category: string;
}

export const accreditations: Accreditation[] = [
  {
    name: "Google Cloud Certified Professional Machine Learning Engineer",
    issuer: "Google Cloud / Credly",
    badgeUrl: "https://www.credly.com/badges/34941099-1748-4461-ba2c-fcd4d025dacf/public_url",
    category: "AI & Machine Learning"
  },
  {
    name: "TensorFlow Developer Certificate",
    issuer: "Google TensorFlow / Credential.net",
    badgeUrl: "https://www.credential.net/110b864e-f4ec-4b68-9dd6-c23309d1b4f5#gs.3lt7s8",
    category: "AI & Machine Learning"
  },
  {
    name: "Grafana Observability Solution Architect",
    issuer: "Grafana Labs",
    badgeUrl: "https://grafanalabs.docebosaas.com/partners/share/v1/gamification/assigned_badge/c2554bfa-0467-42d4-9509-79222d575014/shared?lang=en&t=1727935294763",
    category: "Cloud Native & Observability"
  },
  {
    name: "AWS Community Builder",
    issuer: "Amazon Web Services",
    badgeUrl: "https://builder.aws.com/community/@shakir?tab=articles",
    category: "Cloud & Community"
  },
  {
    name: "GitHub Actions Certification",
    issuer: "GitHub / Credly",
    badgeUrl: "https://www.credly.com/badges/d7a21d30-6a22-4017-a958-6bd17089853a/public_url",
    category: "DevOps & CI/CD"
  },
  {
    name: "GitHub Advanced Security",
    issuer: "Microsoft / GitHub",
    badgeUrl: "https://learn.microsoft.com/api/credentials/share/en-gb/ShakirAhmedIbrahim-7900/2A5550EFB591CD47?sharingId=FFE0D97E583BFCA",
    category: "DevOps & Security"
  },
  {
    name: "Neo4j Certified Professional",
    issuer: "Neo4j GraphAcademy",
    badgeUrl: "https://graphacademy.neo4j.com/c/b0021312-fe0b-47fa-980b-f22c4e791c5a/",
    category: "Database & Graph Systems"
  },
  {
    name: "Apollo Graph Associate",
    issuer: "Apollo GraphQL",
    badgeUrl: "https://www.apollographql.com/tutorials/certifications/4d3cbcf3-b0f8-4bfe-bac1-dd5619463724",
    category: "GraphQL & API Architecture"
  }
];
