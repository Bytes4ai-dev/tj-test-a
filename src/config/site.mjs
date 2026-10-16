// The ONE site config file (TJD-641). Contact, public URL and author live here and nowhere else.
// No phone number and no personal email may ever be added here (scripts/prelaunch-check.sh enforces it on dist/).
export const site = {
  name: 'Bytes4AI',
  // Absolute base URL used for og:url / og:image. PLACEHOLDER until the DEV/production domain is decided
  // (see PRELAUNCH-CHECKLIST.md). Override at build time with SITE_URL.
  url: process.env.SITE_URL || 'http://localhost:8080',
  author: {
    name: 'Ravi Singh',
    initials: 'RS',
    title: 'Senior AI Architect and Principal Data Architect',
    location: 'Keller TX',
    linkedin: 'https://www.linkedin.com/in/rpsingh1982',
    linkedinLabel: 'linkedin.com/in/rpsingh1982',
  },
  // Contact / "Book a review". mode: 'placeholder' | 'mailto' | 'form'.
  // PLACEHOLDER until RP supplies a business email or booking link.
  contact: {
    mode: 'placeholder',
    mailto: '', // business address only, e.g. a shared hello@ mailbox; never a personal email
    formAction: '', // https URL of a hosted form; used when mode is 'form'
    placeholderText: 'Business contact details are coming soon. Until then, reach Ravi on LinkedIn.',
  },
};
