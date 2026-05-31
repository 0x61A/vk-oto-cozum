---
name: Industrial Velocity
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#e4beb9'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#ab8985'
  outline-variant: '#5b403d'
  surface-tint: '#ffb4ac'
  primary: '#ffb4ac'
  on-primary: '#690006'
  primary-container: '#ff544c'
  on-primary-container: '#5c0005'
  inverse-primary: '#bb171c'
  secondary: '#ffdf9e'
  on-secondary: '#3f2e00'
  secondary-container: '#fabd00'
  on-secondary-container: '#6a4e00'
  tertiary: '#c6c6c7'
  on-tertiary: '#2f3131'
  tertiary-container: '#909191'
  on-tertiary-container: '#282a2a'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad6'
  primary-fixed-dim: '#ffb4ac'
  on-primary-fixed: '#410002'
  on-primary-fixed-variant: '#93000d'
  secondary-fixed: '#ffdf9e'
  secondary-fixed-dim: '#fabd00'
  on-secondary-fixed: '#261a00'
  on-secondary-fixed-variant: '#5b4300'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Oswald
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
  headline-lg:
    fontFamily: Oswald
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Oswald
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  title-md:
    fontFamily: Oswald
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
    letterSpacing: 0.05em
  body-lg:
    fontFamily: Roboto Flex
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Roboto Flex
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-bold:
    fontFamily: Oswald
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
  section-gap: 80px
---

## Brand & Style
The brand personality is authoritative, high-performance, and dependable. It bridges the gap between raw automotive grit and modern technological precision. The target audience includes vehicle owners seeking expert technical solutions and professionals in the automotive repair industry.

The design style is **High-Contrast / Modern** with **Industrial** undertones. It utilizes a dark-mode default to evoke the atmosphere of a premium garage or high-end performance shop. Visuals are characterized by bold weights, sharp transitions, and a tactical use of color to highlight urgent information and call-to-actions.

## Colors
The palette is rooted in a deep, "Oil-Slick" Black (#121212) for primary backgrounds to create a high-end, focused environment. 

- **Primary Red (#E53935):** Used for critical actions, branding accents, and highlighting specialized services (e.g., DPF or Airbag solutions).
- **Secondary Yellow (#FFC107):** Reserved for secondary information, cautionary alerts, or contact details to ensure maximum visibility against dark backgrounds.
- **Pure White (#FFFFFF):** Used exclusively for high-readability body text and essential iconography.
- **Surface Neutrals:** Tiered shades of grey are used to define layout sections without breaking the dark-mode immersion.

## Typography
The typography system prioritizes impact and legibility. **Oswald** is used for all headings and labels to provide a condensed, mechanical, and strong aesthetic that mirrors automotive instrumentation. **Roboto Flex** is used for body copy to ensure technical details and service descriptions remain highly readable across all devices.

All headlines should utilize uppercase styling to reinforce the industrial, "signage-inspired" look of the brand.

## Layout & Spacing
The design system employs a **Fluid Grid** model with a standard 12-column structure for desktop. 

- **Desktop:** 12 columns with 24px gutters. Content is centered with wide 64px margins to maintain a premium, focused feel.
- **Tablet:** 8 columns with 20px gutters.
- **Mobile:** 4 columns with 16px gutters.

The spacing rhythm follows a strict 8px baseline grid. High-density information (like service lists) should use tight vertical spacing, while hero sections and service categories should utilize larger "section-gaps" to create a sense of scale and professionalism.

## Elevation & Depth
Depth is achieved through **Tonal Layers** rather than soft shadows, maintaining the clean, industrial aesthetic.

1.  **Floor (Level 0):** The main background (#121212).
2.  **Raised (Level 1):** Cards and containers use a slightly lighter surface color (#1A1A1A) with a thin, 1px low-contrast border (#333333).
3.  **Accent (Level 2):** Critical interactive elements or "active" cards may use a Primary Red (#E53935) glow—a very low-opacity outer blur—to simulate an LED or dashboard illumination effect.

Avoid heavy, fuzzy shadows; instead, use sharp "hard" shadows (2px displacement, 100% opacity) if a physical "cut-out" look is required for buttons.

## Shapes
The shape language is **Soft (Level 1)**. Elements have a subtle 0.25rem corner radius. This choice balances the "hard" industrial nature of the automotive sector with modern digital software expectations. 

Small UI elements like chips or badges may use the `rounded-lg` (0.5rem) setting to distinguish them from structural containers, but the overall system should avoid pill-shapes or fully rounded circles to maintain a disciplined, "engineered" appearance.

## Components

### Buttons
- **Primary:** Solid Primary Red (#E53935) with White Oswald Bold text. Sharp corners or 4px radius. High-impact.
- **Secondary:** Outlined White or Yellow (#FFC107) with 1px border.
- **Tertiary:** Text-only in Oswald, uppercase, with a right-arrow icon for "View More" actions.

### Input Fields
- Dark backgrounds (#1A1A1A) with 1px borders (#333333). 
- Active state: Border changes to Primary Red or Secondary Yellow.
- Labels are always Oswald, small-caps/uppercase, positioned above the field.

### Cards
- Service cards should feature a large icon or technical illustration at the top.
- Background: #1A1A1A.
- On hover, the border color transitions to Primary Red.

### Chips & Tags
- Used for service categories (e.g., "Klima", "EGR", "Mechanical").
- High-contrast: Yellow background with Black text for visibility, or Black background with Red border for "Technical" status.

### Progress & Status Indicators
- Use the Secondary Yellow for "In Progress" states and Primary Red for "Action Required" or "Diagnostic Faults" to mimic dashboard warning lights.