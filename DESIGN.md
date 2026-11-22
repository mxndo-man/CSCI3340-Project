---
name: Shortlist
description: A cozy, blocky mountain look for a shared internship tracker. Square pixel boxes, warm cream by day, the landing page's valley greens by night, one gold for "look here".
colors:
  canvas: "#f4ebdb"
  paper: "#fffbf3"
  sunk: "#ebddc6"
  line: "#decbae"
  edge: "#c4a983"
  line-strong: "#9a825f"
  bar: "#fffbf3"
  ink: "#2e2419"
  ink-soft: "#4a3a28"
  ink-muted: "#6e583d"
  action: "#b4532f"
  action-hover: "#953f1f"
  action-ink: "#9a4423"
  action-soft: "#f6dccb"
  on-action: "#fffbf3"
  gold: "#f2b92e"
  gold-hi: "#ffd977"
  gold-lo: "#b9861a"
  on-gold: "#2e2419"
  gold-ink: "#7a5208"
  gold-soft: "#fbe7b0"
  band-pine: "#4e5c37"
  on-pine: "#f4ebdb"
  good-ink: "#45602e"
  good-soft: "#dde6c4"
  alert-ink: "#a3362b"
  alert-soft: "#f6d6ce"
  info-ink: "#2f5482"
  info-soft: "#d8e3f1"
  hero-sky: "#3e5881"
typography:
  hero:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(3.25rem, 9.2vw, 7rem)"
    fontWeight: 500
    lineHeight: 0.96
    letterSpacing: "-0.035em"
  wordmark:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "1.375rem"
    fontWeight: 700
    letterSpacing: "-0.02em"
  display:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "3.25rem"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.03em"
  h1:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "2.25rem"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  h2:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Pixelify Sans, ui-monospace, Consolas, monospace"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "0.05em"
rounded:
  none: "0px"
spacing:
  voxel: "4px"
---

# Design System: Shortlist

This file describes how Shortlist looks, so every page matches. The block at the top lists the exact values, called **tokens** (named colours, sizes and fonts). The tokens live in `styles/styles.css`; this file explains when to use each one.

**Where this applies:** every page. App pages get it through `templates/base.html` and the Tailwind classes made from the tokens (for example `bg-paper`, `text-ink`, `shadow-pixel`).

## Overview

**North star: "Golden hour in a mountain town."** Approachable, cozy and a little game-like. Boxes are solid blocks with square, stepped "pixel" corners. Buttons are blocks with a lit top edge and a shaded bottom edge that sink when pressed. Things move in a few visible steps instead of gliding. The words stay plain and human; the game feel lives in shapes, colour and motion, never in game words.

**Two modes, same roles.** Dark mode (the landing page's valley greens) is the default; light mode is warm cream and terracotta. A visitor switches with the sun/moon switch in the header: a square track with a gold block that slides, in steps, to the current mode. The choice is kept in their browser.

## Colors

Templates use **roles** (what a colour is for), never raw hex values. Each role has a light and a dark value, so a page written with roles works in both modes.

| Role | Light | Dark | Use |
|---|---|---|---|
| `canvas` | #f4ebdb (Sand) | #0f2118 (Night) | the page background |
| `bar` | #fffbf3 | #142b1f | the header |
| `paper` | #fffbf3 | #1a3828 (Meadow 800) | the face of every box: cards, panels, menus, dialogs, inputs |
| `sunk` | #ebddc6 | #21422f | hover fills, the selected item in a list, pressed-in areas |
| `line` | #decbae (Clay) | #2e6a41 | thin dividers inside boxes |
| `edge` | #c4a983 | #2e6a41 (Meadow 600) | the 4px pixel edge around every box |
| `line-strong` | #9a825f | #5f8f62 | input borders and edges that must be seen (3:1) |
| `ink` | #2e2419 | #e6eedf (Mist) | main text |
| `ink-soft` | #4a3a28 | #cfdccb | secondary text that still reads as body |
| `ink-muted` | #6e583d | #a8bda5 | supporting text, captions, placeholders |
| `action` | #b4532f (Adobe) | #b4532f | buttons you press to do something |
| `action-hover` | #953f1f | #953f1f | an action under the pointer, and its shaded edge |
| `action-ink` | #9a4423 | #f2a27b | links and accent text |
| `action-soft` | #f6dccb (Pueblo) | #3d2a1c | tinted background for something selected |
| `on-action` | #fffbf3 | #fffbf3 | text on an action fill |
| `gold` | #f2b92e | #f2b92e | "look here": the wordmark block, Sign up, toast edges, selection, current stage |
| `hero-sky` | #3e5881 | #3e5881 | the landing hero's sky, matched to the top edge of its image |
| `gold-ink` / `gold-soft` | #7a5208 / #fbe7b0 | #f5c85a / #3a3514 | "look closer" chips and notices, the preview banner |
| `good-ink` / `good-soft` | #45602e / #dde6c4 (Sage) | #e6eedf / #2e6a41 | in your favour |
| `alert-ink` / `alert-soft` | #a3362b / #f6d6ce | #f09a88 / #45231f | closed, unpaid, delete, form errors |
| `info-ink` / `info-soft` | #2f5482 / #d8e3f1 | #9dbde6 / #1c2f3c | neutral information |
| `band-pine` / `on-pine` | #4e5c37 / #f4ebdb | #0a1710 / #e6eedf | the footer band |

Gold uses `on-gold` (#2e2419) for text in both modes.

### Named Rules
**The Gold Rule.** Gold means "look here or you're here": the next thing to do, the current step, something that needs a check, something done. Use it sparingly; never as a large background.

**The Action Rule.** Adobe (`action`) is for buttons that do something. Links and accent text use `action-ink`.

**The Status Rule.** A chip or notice's colour is its meaning: `good` is in your favour, `gold` is look closer, `alert` is against you or destructive, neutral is `sunk`. Never pick a status colour for decoration.

**The Plain Header Rule.** The header has no colour. It is set apart from the page by its own face (`bar`) and a hard 4px edge underneath (`shadow-bar`).

## Typography

- **Familjen Grotesk** does all the reading: headings, body, buttons. Class `font-sans` (the default).
- **Pixelify Sans** is for readouts only: IDs, dates, codes, timers, counts and small labels. Use the `readout` class (Pixelify, 0.8125rem, uppercase, slight letter spacing) or `font-pixel`.

| Class | Size | Use |
|---|---|---|
| `text-wordmark` | 1.375rem bold | the product name in the header and footer |
| `text-hero` | clamp(3.25rem, 9.2vw, 7rem) | the landing hero's headline only |
| `text-display` | 3.25rem | the one big number or headline on a page |
| `text-h1` | 2.25rem, 600 | page titles |
| `text-h2` | 1.5rem, 600 | section headings and dialog titles |
| `text-title` | 1.125rem, 600 | the name at the top of a card |
| `text-base` | 1rem | body text and form fields |
| `text-sm` / `text-xs` | 0.875 / 0.75rem | supporting lines, captions |

**The Readout Rule.** Sentences, headings and button text are never in the pixel face. Large numbers that must be read at a glance (the counts in the landing page's stage blocks) use the reading face in bold, because the pixel face's 1 and 2 blur at that size.

## Shape and depth

- **Every corner is square.** There is no rounding anywhere, including avatars, dots and chips.
- **Pixel corners** (`shadow-pixel`): four hard 4px edges in `edge` that don't meet, so each corner looks like a missing pixel. Every box uses this one style. To colour one box's edge (for example gold for a fact that needs a check), set `[--box-edge:var(--color-gold-lo)]` on it.
- **Hover on a clickable box:** `hover:shadow-soft` darkens the edge to `line-strong`.
- **Menus and dialogs:** `shadow-pop`, the pixel edge in `line-strong` plus a hard drop below.
- **Pressable blocks** have a lit top and shaded bottom edge (`shadow-bevel-action`, `shadow-bevel-gold`, `shadow-bevel-paper`) and the `press` class, which sinks them 2px on hover and 4px when pressed.
- **No blur.** No soft shadows, glows, gradients or blurred backdrops.

## Motion

Everything moves in 3 visible steps over 120ms (`steps(3, end)`). This is the default for every `transition` class. Menus and toasts step in the same way. All motion turns off when the visitor asks for reduced motion.

## Layout

- Content sits in a centred column (`max-w-6xl`, `px-4 sm:px-6`), the same as the header and footer.
- Boxes in a grid need at least a 1rem gap, because the pixel edge sits 4px outside each box.
- Spacing comes from Tailwind's scale, which steps in 4px (one voxel).
- Pages are checked at 1440 and 390 px wide, in both modes.

## Components

Shared pieces live in `templates/components/` and the class helpers in `apps/ui/templatetags/ui.py`.

- **Buttons** (`{% button_class %}`, `components/button.html`): square blocks. `primary`: Adobe with a bevel. `secondary`: paper with a 2px `line-strong` border and a shaded bottom edge. `ghost`: no fill, `sunk` on hover. `danger`: alert text, `alert-soft` on hover. Sizes `sm` (h-9) and `md` (h-11). One primary per view.
- **Chips** (`components/chip.html`): small square tags, 0.75rem text, filled with the status `-soft` colour and its `-ink` text. Tones: `good`, `warn` (gold), `alert`, neutral (`sunk`), and `accent` (`action-soft` with `action-ink`) for a label that isn't a status, such as a selected filter.
- **Notices** (`components/banner.html`): a status-tinted area with a 2px edge in the status colour. No pixel corners, because notices sit inside cards.
- **Fields** (`components/field.html`, `{% ui_widget %}`): label above, a square input on `paper` with a 2px `line-strong` border; focus turns the border `action-ink`; errors use `alert-ink`.
- **Avatars** (`components/avatar.html`): flat square tiles with initials in the pixel face, tinted by person.
- **Countdown** (`components/countdown.html`): a clock icon and the time left as a readout: `alert-ink` when 5 days or fewer, `gold-ink` when 10 or fewer, `ink-muted` otherwise.
- **Empty state** (`components/empty_state.html`): a dashed `line-strong` outline with a heading, one line, and one action.
- **Toggle** (`components/toggle.html`): a square track with a square knob; Adobe when on.
- **Header** (`base.html`): the gold wordmark block, nav links with a 4px `ink` bar under the current page, the light/dark switch, the account menu, and a gold Sign up block.
- **Landing sections** (`pages/landing.html`): full-width bands that alternate `canvas` and `bar`; each band rises out of the one above along a `ridgeline` in its own colour. The hero stops a little short of the screen and carries a "See how it works" prompt, so it's clear there's more below.
- **Footer** (`base.html`): a Pine band with a stepped pixel ridgeline (`ridgeline`) rising out of the page.
- **Toasts** (`base.html`): `ink` with `canvas` text and a gold bottom edge.

## Voice

Approachable and human. Say what the product does in plain words: postings, boards, tracker, deadline; facts are **extracted** and shown as "Extracted · 94% confident". Never claim the product decides who can apply, and don't use slogans that tell people what not to do. No game words (party, quest, XP, levels) and no location details about the team.

## Do's and Don'ts

### Do:
- **Do** use roles (`bg-paper`, `text-ink`...) instead of raw colours.
- **Do** give every box pixel corners with `shadow-pixel`.
- **Do** keep text at WCAG 2.1 AA (4.5:1, or 3:1 for large text) in both modes.
- **Do** use the pixel face only for readouts.
- **Do** check light and dark mode for every page you change.

### Don't:
- **Don't** round corners, blur shadows or use gradients.
- **Don't** colour the header.
- **Don't** use Gold for large areas or for decoration.
- **Don't** use a thick coloured line down one side of a box.
- **Don't** put a box with pixel corners inside another one. Inside a card, use a flat fill (`bg-canvas`), and a 2px inset ring (`ring-2 ring-inset`) when it needs an edge.
- **Don't** add hard-coded colours, fonts or sizes; add a token instead.
