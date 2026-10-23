# PropValueAI — Design Tokens v1.0

**Product:** PropValueAI — Real Estate Price Prediction Using Python and Machine Learning  
**Design direction:** Premium professional real-estate analytics  
**Reference:** Approved PropValueAI UI mockup  
**Frontend target:** Next.js + TypeScript + Tailwind CSS  
**Status:** Proposed baseline for review

> These tokens are proposed implementation values inspired by the visual direction of the generated mockup. They are not measured pixel values extracted from the image. The existing repository, `AGENTS.md`, approved architecture, and actual API contracts remain authoritative.

---

## 1. Design Principles

- Professional, clean, trustworthy real-estate analytics UI.
- Use navy for structure and blue for primary actions.
- Prefer white surfaces, light-grey backgrounds, subtle borders, and restrained shadows.
- Maintain consistent typography, spacing, controls, and navigation across screens.
- Design responsively for desktop, tablet, and mobile.
- Avoid generic AI chat interfaces, decorative AI icons, glowing gradients, and unrelated AI features.
- Do not display fabricated market statistics, fake prediction history, unsupported charts, or made-up valuation insights.

## 2. Color Tokens

### 2.1 Brand and Interface Colors

| Token | Value | Intended usage |
|---|---|---|
| `brand-900` | `#10243A` | Sidebar, strong headings, dark navigation |
| `brand-800` | `#183652` | Dark secondary surfaces and hover states |
| `primary-600` | `#1769E0` | Primary buttons, links, active navigation |
| `primary-700` | `#1254B8` | Primary button hover |
| `primary-100` | `#E8F1FF` | Selected and highlighted backgrounds |
| `canvas` | `#F4F7FB` | Main application background |
| `surface` | `#FFFFFF` | Cards, forms, tables, dialogs |
| `border` | `#DCE5EF` | Borders and dividers |
| `text-primary` | `#172B42` | Main content and headings |
| `text-secondary` | `#66778B` | Supporting text, metadata, labels |

### 2.2 Status Colors

| Token | Value | Intended usage |
|---|---|---|
| `success` | `#15803D` | Successful prediction or saved state |
| `success-bg` | `#EAF8EF` | Success alert background |
| `warning` | `#B45309` | Warnings and cautions |
| `warning-bg` | `#FFF7E6` | Warning background |
| `danger` | `#B42318` | Validation errors and failed requests |
| `danger-bg` | `#FEF0EF` | Error background |
| `info` | `#1769E0` | Informational notices |
| `info-bg` | `#EAF2FF` | Informational panels and disclaimer |

## 3. Typography

**Recommended font:** Inter, with a system sans-serif fallback.

| Token | Size | Weight | Intended usage |
|---|---:|---:|---|
| `text-xs` | 12px | 400–500 | Metadata and timestamps |
| `text-sm` | 14px | 400–500 | Labels and supporting text |
| `text-base` | 16px | 400 | Body text and inputs |
| `text-lg` | 18px | 600 | Card headings |
| `text-xl` | 20px | 600 | Section headings |
| `text-2xl` | 24px | 600–700 | Page titles |
| `text-3xl` | 30px | 700 | Landing page headline |
| `price-display` | 32–36px | 700 | Predicted price result |

### Typography Rules

- Main headings use dark navy; do not use bright blue for every heading.
- Use blue for important actions and selected states.
- Use tabular numerals for prices, counts, and dates where supported.
- Avoid excessive bold text and oversized headings inside dashboard cards.

## 4. Spacing and Layout

Use a 4px base spacing scale.

| Token | Value | Typical usage |
|---|---:|---|
| `space-1` | 4px | Icon/text gap |
| `space-2` | 8px | Compact control spacing |
| `space-3` | 12px | Form field spacing |
| `space-4` | 16px | Standard card padding |
| `space-5` | 20px | Section spacing |
| `space-6` | 24px | Dashboard card padding |
| `space-8` | 32px | Section separation |
| `space-10` | 40px | Large section spacing |
| `space-12` | 48px | Landing page spacing |

### Application Layout

- Desktop sidebar width: `248px`.
- Header height: `64px`.
- Main content maximum width: `1440px`.
- Desktop page padding: `32px`.
- Tablet page padding: `24px`.
- Mobile page padding: `16px`.
- Dashboard card gap: `20–24px`.
- Prediction form: two columns on desktop, one column on mobile.

## 5. Borders, Radii, and Shadows

| Token | Value | Intended usage |
|---|---|---|
| `radius-sm` | `6px` | Compact controls |
| `radius-md` | `10px` | Inputs and buttons |
| `radius-lg` | `14px` | Dashboard cards |
| `radius-xl` | `18px` | Landing sections and larger panels |
| `radius-full` | `9999px` | Pills and avatars |
| `shadow-card` | `0 2px 8px rgba(16,36,58,0.05)` | Standard cards |
| `shadow-dropdown` | `0 8px 24px rgba(16,36,58,0.12)` | Dropdowns and popovers |
| `border-default` | `1px solid #DCE5EF` | Cards and inputs |

**Rule:** Keep shadows subtle. Use spacing and borders—not heavy elevation—to establish hierarchy.

## 6. Component Tokens

### 6.1 Buttons

- Primary button: background `#1769E0`, white text.
- Primary hover: background `#1254B8`.
- Secondary button: white background, border `#DCE5EF`, text `#172B42`.
- Tertiary action: background `#E8F1FF`, text `#1769E0`.
- Height: `40–44px`.
- Horizontal padding: `16px`.
- Border radius: `8–10px`.
- Provide a clearly visible keyboard focus ring and disabled state.

### 6.2 Form Controls

- Height: `44px`.
- Background: `#FFFFFF`.
- Border: `1px solid #DCE5EF`.
- Border radius: `10px`.
- Internal horizontal padding: `12px`.
- Focus state: primary-blue border/ring with sufficient contrast.
- Use visible labels; do not rely on placeholders as labels.
- Display validation messages near the corresponding field.

### 6.3 Dashboard Cards

- Background: `#FFFFFF`.
- Border: `1px solid #DCE5EF`.
- Border radius: `14px`.
- Padding: `16–24px`.
- Shadow: `0 2px 8px rgba(16,36,58,0.05)`.
- Use real API data only. Do not seed the UI with fabricated statistics.

### 6.4 Tables

- White surface with subtle row dividers.
- Clear column headings and readable row spacing.
- Use tabular numerals for prices and numeric values.
- Respect backend pagination and sorting.
- On small screens, use a dedicated horizontal-scroll container when necessary.

### 6.5 Alerts and Disclaimer

- Success: `#EAF8EF` background, `#15803D` text.
- Warning: `#FFF7E6` background, `#B45309` text.
- Error: `#FEF0EF` background, `#B42318` text.
- Information: `#EAF2FF` background, `#1769E0` text.

Required exact disclaimer:

> PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.

## 7. Screen-Specific Design Rules

### 7.1 Public Landing Page

- Light background with a professional residential architecture image.
- Strong navy/blue headline and concise product explanation.
- Clear Sign in and Get Started actions.
- Explain property price estimation without implying verified live market valuations.
- Show the educational-purpose disclaimer.

### 7.2 Login and Registration

- Centered white form card.
- Restrained background imagery.
- Clear labels, inline validation, loading, and API error states.
- Implement only flows supported by the existing backend.

### 7.3 Authenticated Dashboard

- Navy sidebar, white top bar, light canvas.
- Compact cards and a prominent New Prediction action.
- Display only values supported by actual API responses.
- If there is no dashboard-summary endpoint, use an action-oriented dashboard instead of invented analytics.

### 7.4 Prediction Form and Result

- Structured property inputs based on the real backend request DTO.
- Two-column desktop layout and one-column mobile layout.
- Clear field labels, validation, loading, and error states.
- Prominent estimated price result, using only actual response fields.
- Show the exact required disclaimer.
- Do not display fabricated confidence percentages, market trends, comparable sales, or investment advice.

### 7.5 Prediction History

- Use the existing authenticated history endpoint.
- Show only fields returned by the backend.
- Include loading, empty, error, and retry states.
- Never allow a user to retrieve another user's records by changing a user ID.

### 7.6 Admin Prediction History

- Implement only if supported by the existing admin endpoint and response contract.
- Show the view only to authenticated administrators.
- Treat frontend role checks as presentation controls; Spring Security remains authoritative.

### 7.7 Mobile Views

- Below `640px`: compact header/navigation and single-column forms.
- `640–1023px`: flexible tablet layout.
- `1024px` and above: desktop sidebar and wider content layout.
- `1280px` and above: additional breathing room with restrained content width.
- Prevent page-level horizontal overflow.
- Ensure accessible forms, readable result cards, and usable tables.

## 8. Responsive Breakpoints

Use Tailwind's standard breakpoints unless the existing repository defines different conventions.

| Breakpoint | Width | Layout guidance |
|---|---:|---|
| Mobile | `< 640px` | Compact navigation, one-column forms |
| Tablet | `640–1023px` | Flexible columns and compact navigation |
| Desktop | `>= 1024px` | Full sidebar and desktop content |
| Wide desktop | `>= 1280px` | More whitespace and controlled content width |

## 9. Suggested Frontend Organization

Adapt this structure to the existing repository; do not impose it if a different approved structure already exists.

```text
frontend/
├── app/
├── components/
│   ├── layout/
│   ├── ui/
│   ├── dashboard/
│   └── prediction/
├── lib/
│   ├── api/
│   └── auth/
├── types/
└── app/globals.css
```

Use CSS variables as the single source of truth and map them to Tailwind utilities. Avoid duplicating color definitions across files.

## 10. Non-Negotiable Product and Architecture Constraints

1. Preserve the approved backend and API contracts.
2. The browser communicates only with Spring Boot.
3. Guest predictions are prohibited.
4. Never show fake market statistics, fake prediction history, or unsupported analytics.
5. Display the exact educational disclaimer provided in this document.
6. Do not introduce a generic AI chatbot or unrelated AI features.
7. Do not change the approved architecture without explicit approval.
8. Keep accessibility, responsive behavior, loading states, and error handling consistent.
9. Never expose database credentials, JWT secrets, or backend secrets in frontend code.
10. Do not commit or push unless explicitly authorized.

## 11. Implementation Note

This document defines the proposed visual tokens and screen styling rules. Before implementation, inspect `AGENTS.md`, `docs/architecture.md`, `docs/api-contracts.md`, and the actual backend source. Existing project decisions and API contracts take precedence over assumptions in a visual mockup.
