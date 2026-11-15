# A&N Overseas — student information completeness standard

Updated: 2026-11-15

## Goal
A student should be able to research and compare study destinations, programmes, costs, admissions, scholarships, visas and arrival planning without having to search for basic information on another website. Official applications, payments and government visa submissions may still require the responsible institution's portal.

## Per-university publication checklist
- Verified institution identity, country, city, recognition status and official website
- Faculties, departments, programme names, qualification level, duration, language and study mode
- Programme-specific entry requirements, relevant previous degrees, GPA/CGPA, English evidence, MOI/waiver policy and document requirements
- Intake months, application windows, deadlines, dates and timezone; distinguish upcoming vs historical
- Programme-specific tuition with currency, per-semester/per-year basis, international-student status, deposits, application fee and source date
- Scholarships with eligibility, coverage, restrictions and verified deadlines
- Campus, accommodation, living costs, student work rules, dependant policy, post-study pathways and visa guidance, with jurisdiction and update dates
- Rankings with year, ranking provider, discipline where relevant; NA if not published
- Contact information and official references, embedded explanations and verification dates

## Data quality rules
1. Never manufacture missing fees, scholarships, programme availability, admission guarantees or deadlines.
2. Keep verified, historical, estimated and awaiting-verification values explicitly distinct.
3. A university-level intake, fee or deadline must not be presented as applying to every programme.
4. Time-sensitive facts need a source and checked date. Mark expired deadlines as expired.
5. Recognition, admission and visa eligibility are subject to the responsible authorities; do not guarantee outcomes.
6. Include BDT conversions only with an exchange-rate source, timestamp and clearly labeled approximate amount.
7. Avoid external navigation for basic research, but retain transparent citations and required official application/visa routes.
8. Preserve existing mobile layout, navigation, branding, and Sales Performance app code.

## Existing code inspected
- `an-global-universities.js`: directory seeds, supplementary imports and structured coverage report
- `an-portfolio-2026.js`: 20-section university profile
- `an-eligibility.js` and `an-eligibility-rules.js`: eligibility interface and selected published rules

## Acceptance criteria
The headline catalogue size of 6,210 must not be represented as 6,210 complete profiles. Report separately: total records, verified institution identities, programmes, programme-level fees, intakes, deadlines, eligibility, and fully complete profiles. Publish in audited batches, test on desktop and mobile, and never silently overwrite the production website from an unrelated repository.
