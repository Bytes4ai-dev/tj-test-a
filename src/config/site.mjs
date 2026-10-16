// The ONE site config file (TJD-641). Contact, public URL and author live here and nowhere else.
// No phone number and no personal email may ever be added here (scripts/prelaunch-check.sh enforces it on dist/).
export const site = {
  name: 'Bytes4AI',
  // Absolute base URL used for og:url / og:image / RSS links. Default = the DEV rvdemo-app URL (TJD-643 AC4,
  // PL ruling 56951); the production domain is set at go-live (see PRELAUNCH-CHECKLIST.md). Override with SITE_URL.
  url: process.env.SITE_URL || 'https://rvdemo-app-crnwvkk4ua-uc.a.run.app',
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
