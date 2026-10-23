# PropValueAI — Frontend Application (Phase 5)

## Overview
The PropValueAI frontend is a production-quality web application built with **Next.js (App Router)**, **TypeScript**, and **Tailwind CSS**. It connects strictly to the Spring Boot REST API for stateless JWT authentication, property valuations, and audit history tracking.

Designed strictly according to the approved design tokens in [`docs/PropValueAI-Design-Tokens-v1.0.md`](../docs/PropValueAI-Design-Tokens-v1.0.md).

---

## 1. Features & Screens Implemented

- **Public Landing Page (`/`):** High-converting real-estate presentation explaining residential price estimation, feature overview, and prominent mandatory educational disclaimer.
- **User Authentication:**
  - **Login (`/login`):** Email and password authentication issuing signed Bearer JWT token.
  - **Registration (`/register`):** Secure signup strictly assigning `ROLE_USER` (no admin self-registration).
- **Authenticated Dashboard (`/dashboard`):** Real-time workspace showing recent valuations, active model telemetry (`Random Forest v1.0.0`), target currency (`Lakhs INR`), and quick navigation.
- **New Property Valuation (`/predictions/new`):**
  - Two-column input form: Total Square Feet, BHK Configuration, Bathrooms, Balconies, and Area Classification.
  - Client-side validation, duplicate-submit prevention, and instant result presentation card with exact educational disclaimer.
- **Prediction History (`/predictions`):** Paginated, responsive history table strictly scoped to the authenticated caller with tabular price formatting.
- **Prediction Detail (`/predictions/[id]`):** Deep-dive record view verifying backend ownership enforcement (non-owners receive 403 Forbidden).
- **System Audit Log (`/admin`):** Administrative view for `ROLE_ADMIN` displaying system-wide predictions with pagination.

---

## 2. Architecture & Design System

- **Navy & Blue Palette:**
  - Sidebar & Strong Headings: `#10243A` (`brand-900`)
  - Primary Action / Active Nav: `#1769E0` (`primary-600`)
  - Hover Action: `#1254B8` (`primary-700`)
  - Canvas Background: `#F4F7FB`
  - Cards & Surfaces: `#FFFFFF` with subtle border `#DCE5EF`
- **Mandatory Educational Disclaimer:**
  > PropValueAI provides simulated estimates for educational demonstration purposes only. Predictions are not actual Pune market valuations.

---

## 3. Local Development Setup

### Step 1: Configure Environment Template
Copy the frontend template to `.env.local`:
```bash
cp .env.example .env.local
```
Configure your Spring Boot backend address (default: `http://localhost:8080`):
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080
```

### Step 2: Run Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Step 3: Run Type-Check & Production Build
```bash
npx tsc --noEmit
npm run build
```
All routes are compiled with zero errors and zero warnings.
