import Explorer from './explorer';

import auditGuideline from '@/data/audit-guideline.json';
import auditReports from '@/data/audit-reports.json';
import auditRisks from '@/data/audit-risks.json';
import cryptoNotes from '@/data/crypto-notes.json';
import financials from '@/data/financials.json';
import needsReview from '@/data/needs-review.json';
import projects from '@/data/projects.json';
import relations from '@/data/relations.json';
import sources from '@/data/sources.json';
import tokens from '@/data/tokens.json';
import vasps from '@/data/vasps.json';

export default function Home() {
  return (
    <Explorer
      datasets={{
        auditGuideline,
        auditReports,
        auditRisks,
        cryptoNotes,
        financials,
        needsReview,
        projects,
        relations,
        sources,
        tokens,
        vasps,
      }}
    />
  );
}
