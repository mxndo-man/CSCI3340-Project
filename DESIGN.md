---
name: Shortlist
description: A voxel-style look for a shared internship tracker. Square blocks, dusk sky, meadow greens, one marigold accent.
colors:
  marigold: "#f2c230"
  marigold-hi: "#ffe27a"
  marigold-lo: "#b5820c"
  ink: "#17130a"
  sky: "#3e5881"
  sky-deep: "#40566f"
  night: "#0f2118"
  meadow-900: "#142b1f"
  meadow-800: "#1a3828"
  meadow-600: "#2e6a41"
  leaf: "#8fbf7a"
  mist: "#e6eedf"
  mist-dim: "#a8bda5"
  haze-line: "#b9c8d4"
  white: "#ffffff"
typography:
  display:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(3.25rem, 9.2vw, 7rem)"
    fontWeight: 500
    lineHeight: 0.96
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(2.25rem, 5vw, 3.75rem)"
    fontWeight: 500
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  subhead:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "clamp(1.5rem, 2.6vw, 2rem)"
    fontWeight: 500
    lineHeight: 1.12
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Familjen Grotesk, Segoe UI, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.55
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
  gutter: "clamp(1.25rem, 4vw, 3rem)"
  band: "clamp(4.5rem, 10vw, 8.5rem)"
  wrap: "76rem"
components:
  button-primary:
    backgroundColor: "{colors.marigold}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.625rem 1.375rem 0.875rem"
    height: "3rem"
  button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "0.625rem 1.375rem"
    height: "3rem"
  button-quiet-hover:
    backgroundColor: "{colors.white}"
    textColor: "{colors.sky-deep}"
  button-light:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "0.375rem 1rem 0.625rem"
    height: "2.5rem"
  panel:
    backgroundColor: "{colors.meadow-800}"
    textColor: "{colors.mist}"
    rounded: "{rounded.none}"
  card:
    backgroundColor: "{colors.meadow-800}"
    textColor: "{colors.mist}"
    rounded: "{rounded.none}"
    padding: "1.25rem"
  board-card:
    backgroundColor: "{colors.night}"
    textColor: "{colors.mist}"
    rounded: "{rounded.none}"
    padding: "1.25rem"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.mist}"
    rounded: "{rounded.none}"
    padding: "0.125rem 0.5rem"
  chip-good:
    backgroundColor: "{colors.meadow-600}"
    textColor: "{colors.mist}"
  chip-warn:
    backgroundColor: "transparent"
    textColor: "{colors.marigold}"
  fact-tile:
    backgroundColor: "{colors.meadow-800}"
    textColor: "{colors.mist}"
    rounded: "{rounded.none}"
    padding: "1rem"
  check-tag:
    backgroundColor: "{colors.marigold}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    padding: "0 0.375rem"
  sample-label:
    textColor: "{colors.leaf}"
    typography: "{typography.label}"
  ruler:
    backgroundColor: "{colors.night}"
    textColor: "{colors.mist-dim}"
    typography: "{typography.label}"
  stage-marker:
    backgroundColor: "{colors.meadow-800}"
    textColor: "{colors.mist-dim}"
    size: "2.5rem"
  stage-marker-current:
    backgroundColor: "{colors.marigold}"
    textColor: "{colors.mist}"
    size: "2.5rem"
  member-tile:
    backgroundColor: "{colors.meadow-600}"
    textColor: "{colors.mist}"
    typography: "{typography.label}"
    size: "2rem"
  member-tile-more:
    backgroundColor: "transparent"
    textColor: "{colors.mist-dim}"
    typography: "{typography.label}"
    size: "2rem"
  notice:
    backgroundColor: "{colors.mist}"
    textColor: "{colors.night}"
    padding: "0.75rem 1rem"
---

# Design System: Shortlist

This file describes how Shortlist looks, so new pages match the ones already built. The block at the top (between the `---` lines) lists the exact values, called **tokens**: named colours, type sizes and spacings. The text below explains when to use them.

**Where this applies today:** only the landing page (`templates/pages/landing.html` with `static/css/landing.css`). The app pages that extend `base.html` still use the older look and have not been migrated yet.

## Overview

**Creative North Star: "The Valley at Dusk"**

Shortlist looks like a small world built out of blocks. A dusk-blue sky sits at the top of the page, and everything under it is deep meadow green. Buttons and markers are solid blocks with a light top edge and a dark bottom edge, so they look like something you can press.

The look is friendly, but the words stay plain. Labels say what things are: posting, board, tracker, deadline. The blocky style is in the shapes, colours and motion, never in the wording.

Nothing is rounded, blurred or faded. Colour areas are flat, corners are square, and things move in a few visible steps instead of gliding.

**Key Characteristics:**
- Square corners everywhere (no rounding).
- Blocks have a lit top edge and a shaded bottom edge.
- Panels and cards have stepped "pixel" corners.
- A checker pattern (a "dither") joins one colour band to the next.
- Ruler ticks run along the top of sections, with a short ID.
- Marigold is the only warm colour.
- Motion moves in steps and never eases.
- Two typefaces: a warm grotesk for reading, a pixel face for IDs, dates, codes, timers and small labels.
- A feature section is a heading plus a small working copy of the real app page.

## Colors

A cool, dark page (sky blue over meadow green) with one warm colour, marigold, that always means "look here".

### Primary
- **Marigold** (`marigold`, #f2c230): the single warm accent. It marks the thing to act on or the place you are: the main button, the selected stage, the "Needs a check" tag, the text of a "look closer" chip, a countdown that is running out, the keyboard focus ring, the small block in the wordmark and the headline cursor.
- **Marigold Light** (`marigold-hi`, #ffe27a): the lit top edge of a marigold block.
- **Marigold Shade** (`marigold-lo`, #b5820c): the shaded bottom edge of a marigold block. Also the thin outline of a "look closer" chip and of a fact tile that needs a check.
- **Ink** (`ink`, #17130a): text on marigold and on white buttons.

### Secondary
- **Dusk Sky** (`sky`, #3e5881): the hero at the top of the page and the closing band at the bottom. Text on it is white.
- **Deep Sky** (`sky-deep`, #40566f): text on a white button when the pointer is over it.

### Neutral
- **Night** (`night`, #0f2118): the page background and the darkest green. Also the face of a board card.
- **Meadow 900** (`meadow-900`, #142b1f): the alternate band, one step lighter than Night.
- **Meadow 800** (`meadow-800`, #1a3828): the face of a panel, a posting card and a fact tile.
- **Meadow 600** (`meadow-600`, #2e6a41): panel edges, divider lines, thin outlines, member tiles, the dashed trail and the fill of an "in your favour" chip.
- **Leaf** (`leaf`, #8fbf7a): small labels on green, such as fact names, counts and the sample label.
- **Mist** (`mist`, #e6eedf): main text on green.
- **Mist Dim** (`mist-dim`, #a8bda5): supporting text on green, and ruler ticks.
- **Haze Line** (`haze-line`, #b9c8d4): the shaded bottom edge of a white button.
- **White** (`white`, #ffffff): text and outlines on Dusk Sky.

### Named Rules
**The One Warm Colour Rule.** Marigold is the only warm colour on a page. Use it for the main action, the current step, or something the user must notice. Never use it as a band background or for body text.

**The Flat Band Rule.** Every band is one flat colour. No gradients. To join two bands, use the dither strip (see Components).

**The Chip Colour Rule.** A chip's colour is its meaning. Filled green means the fact is in your favour. A marigold outline means look closer. A plain green outline is neutral. Never pick a chip colour for decoration.

## Typography

**Display Font:** Familjen Grotesk (with Segoe UI, system-ui, sans-serif)
**Body Font:** Familjen Grotesk (same family)
**Label Font:** Pixelify Sans (with ui-monospace, Consolas, monospace)

**Character:** Familjen Grotesk is a warm grotesk (a plain sans-serif with a friendly shape); it does all the reading. Pixelify Sans is a pixel face (letters drawn on a square grid); it appears small, like a readout on a device.

### Hierarchy
- **Display** (500, clamp(3.25rem, 9.2vw, 7rem), line-height 0.96): the one big headline in the hero. Centred.
- **Headline** (500, clamp(2.25rem, 5vw, 3.75rem), line-height 1.02): section headings.
- **Subhead** (500, clamp(1.5rem, 2.6vw, 2rem), line-height 1.12): a second heading inside a section, next to its demo.
- **Title** (600, 1.125rem, line-height 1.3): the name at the top of a card.
- **Body** (400, 1.0625rem, line-height 1.55): paragraphs. Supporting lines inside cards and tiles step down to 0.9375rem or 0.875rem.
- **Label** (Pixelify Sans 400, 0.8125rem, letter-spacing 0.05em, uppercase): IDs, dates, timers, counts, stage names, fact names and the sample label.

### Named Rules
**The Readout Rule.** The pixel face is for IDs, dates, codes, timers and small labels. Sentences, big headings and button text are always in Familjen Grotesk.

## Layout

- The page is a stack of full-width **bands** (horizontal strips of one colour). Content sits in a centred column up to 76rem wide.
- The side gutter is clamp(1.25rem, 4vw, 3rem), so it shrinks on phones.
- Bands have generous top and bottom padding: clamp(4.5rem, 10vw, 8.5rem) on top and slightly less below.
- The hero fills the first screen (at least 40rem tall). Text sits in the upper half; the lower half is left for the image.
- Small details are built from a 4px unit called a **voxel**: bevel edges, pixel corners and the dither are all 4px or 8px.
- Cards sit in a grid with a 1.25rem gap: three columns for board cards, two for posting cards.
- Key facts tiles sit in a two-column grid with a 0.75rem gap, under their sub-heading. The grid drops to one column below 34rem.
- Two breakpoints (widths where the layout changes): below 56rem, two-column sections become one column, three-column card grids become two, and the nav's section links hide. Below 34rem, hero buttons become full width, and card grids, tile grids and list rows become one column.

### Named Rules
**The Show It Rule.** A feature section is a heading plus a demo of the feature. It does not describe the feature in a paragraph. If the demo needs explaining, fix the demo.

**The Real Page Rule.** Every landing section is a small copy of a real app page, built from the same data and the same template helpers (small functions the app's own pages call to format a chip, a countdown or a fact). That way the landing page cannot drift from the app. Discover and Boards work this way today; the Tracker demo is still written by hand and should follow.

## Elevation & Depth

There are no soft shadows. Depth comes from hard edges and from flat colour steps (Night, then Meadow 900, then Meadow 800).

### Shadow Vocabulary
- **Block bevel** (`box-shadow: inset 0 -4px 0 <shade>, inset 0 4px 0 <light>`): a light strip inside the top edge and a dark strip inside the bottom edge. Used on buttons, member tiles and the selected stage.
- **Pixel corners** (`box-shadow: 0 -4px 0 0 <edge>, 0 4px 0 0 <edge>, -4px 0 0 0 <edge>, 4px 0 0 0 <edge>`): four hard 4px edges with no blur. Because the edges do not meet at the corners, each corner looks like a missing pixel. Used on panels and cards.
- **Thin outline** (`box-shadow: inset 0 0 0 1px <edge>`): a 1px line drawn inside the edge. Used on chips, fact tiles and the "+N" member tile. A fact tile that needs a check gets a 2px Marigold Shade outline instead.

### Named Rules
**The Hard Edge Rule.** Every shadow has zero blur. A shadow here is a drawn edge, not a glow.

**The Press Rule.** A pressed block moves down and loses its bottom edge: 2px on hover, 4px when pressed. The change happens in 3 steps over 120ms (`steps(3, end)`), not as a smooth slide.

## Shapes

- All corners are square (radius 0).
- Panel and card corners are stepped, made with the pixel-corner shadow above.
- Divider lines are solid: 2px Meadow 600 under a group heading inside a panel, and 1px (Meadow 600 at 55% opacity) between rows.
- Dashes and ticks are drawn with hard stops (8px on, 8px off), never dotted or faded.
- Images in the look are pixel art and are scaled without smoothing (`image-rendering: pixelated`).

## Components

### Buttons
- **Shape:** square block, 3rem tall (2.5rem for the small size), text in Familjen Grotesk 600.
- **Primary:** Marigold face, Ink text, block bevel in Marigold Light and Marigold Shade. One per group of actions.
- **Quiet:** no fill, white text, 2px white outline drawn inside the edge. For the second choice next to a primary button on Dusk Sky. On hover it fills white with Deep Sky text.
- **Light:** white face, Ink text, shaded bottom edge. Used small, in the nav.
- **Hover / Pressed:** follows the Press Rule.
- **Focus:** a 2px Marigold outline, 3px away from the element. On Dusk Sky the outline is white, because Marigold is too faint there.

### Panels
- **Corner Style:** stepped pixel corners.
- **Background:** Meadow 800 with Meadow 600 edges. A panel may use Night instead when it sits on Meadow 900.
- **Structure:** a group heading in the label face (Leaf) over a 2px line, then rows separated by 1px lines.
- **Internal Padding:** clamp(1rem, 2.5vw, 1.75rem) at the sides, 0.875rem above and below each row.

### Cards
A card is a panel with 1.25rem padding that holds one thing: a posting or a board. Cards copy the layout of the app's Discover and Boards pages.
- **Posting card:** the title, then a Mist Dim line with the organisation and work mode, then a row of chips, then a footer pinned to the bottom. The footer has the closing date on the left and a countdown in the label face on the right. The countdown turns Marigold when the deadline is near.
- **Board card:** Night face, at least 13rem tall. The board's name with a neutral chip for the member count, a Mist Dim line with the posting count, up to three saved postings (one line each, cut short with "…" if too long, each with a small square Meadow 600 bullet), then member tiles pinned to the bottom.
- **New-board card:** no face, a dashed Meadow 600 outline (2px, 8px on, 8px off) and one centred link in Mist Dim at weight 600 that turns Mist on hover.

### Chips
Small square tags that carry a posting's deciding facts (the few facts that settle whether you can apply). Text is Familjen Grotesk 500 at 0.8125rem, on one line, with 0.125rem by 0.5rem padding. Chips are not pressable, so they have no bevel.
- **In your favour:** Meadow 600 fill, Mist text, no outline.
- **Look closer:** no fill, Marigold text, 1px Marigold Shade outline.
- **Neutral:** no fill, Mist text, 1px Meadow 600 outline.

### Key Facts Tiles
One tile per fact, in a two-column grid. A tile is a Meadow 800 block with a 1px Meadow 600 outline and 1rem padding. Inside: the fact's name in the label face (Leaf), its value at weight 600, where it came from in Mist Dim at 0.875rem, and the quoted sentence underneath at 0.875rem when there is one. A fact that still needs a person to confirm it gets a 2px Marigold Shade outline and a small Marigold tag reading "Needs a check" beside the fact's name. On small screens the tiles stack in one column.

### Sample Label
One short line in the label face (Leaf) above each block of sample data. It names the app page being shown and says the content is sample data, for example "Discover · sample postings". It is a caption for sample data only; do not put it above a heading as decoration.

### Ruler
A thin strip along the top of a section. It draws tick marks (a short tick every 8px and a taller one every 80px) and holds a short ID on the left and, optionally, a date on the right, both in the label face.

### Dither Seam
A two-row checker pattern, 8px tall, placed on the top edge of the lower band and coloured to match that band. It makes one flat colour step into the next without a gradient.

### Navigation
The wordmark (the product name with a small Marigold block before it) sits on the left, section links in the middle, and Log in plus a small Light button on the right. Links are plain text at weight 500; on hover a 2px underline appears in steps. Below 56rem the section links hide.

### Stage Path
The signature component. Five square markers sit on a dashed trail, one per application stage, each with its name and a count in the label face. The selected marker turns Marigold, gets a block bevel and sits 4px higher. Choosing a marker shows that stage's entries in the panel below. Without JavaScript, every stage is listed.

### Member Tiles
2rem square blocks holding initials in the label face. Meadow 600 with a block bevel. A card shows up to four; any others are counted in one last tile ("+N") with no fill, Mist Dim text and a 1px Meadow 600 outline.

### Notices
Short system messages, fixed to the bottom right. Mist background, Night text, a Leaf bottom edge.

### Hero Image
A wide voxel valley image (3:1) at `static/img/landing/hero-valley.webp`. It sits along the bottom of the hero: 62% of the hero's height on wide screens and 46% on phones, cropped from the centre. Above it the hero is flat Dusk Sky, which is the same colour as the image's top edge, so the two join without a visible line. The headline and buttons always sit on the flat sky, never on the image's pink horizon or flowers. If the file is missing, the whole hero is flat Dusk Sky.

## Do's and Don'ts

### Do:
- **Do** keep every corner square.
- **Do** give pressable blocks a lit top edge and a shaded bottom edge.
- **Do** use Marigold for one main action per view, the current step, and things the user must notice.
- **Do** use the pixel face for IDs, dates, codes, timers and small labels.
- **Do** join colour bands with the dither seam.
- **Do** move things in steps (`120ms steps(3, end)`), and turn motion off when the user asks for reduced motion.
- **Do** label demonstration content as sample data, with a sample label above the block.
- **Do** show a feature with a small copy of its real app page, built from the same data and template helpers.
- **Do** let a chip's colour carry its meaning: filled green, marigold outline or plain outline.
- **Do** write labels in plain product words: posting, board, tracker, stage, deadline.
- **Do** keep text contrast at WCAG 2.1 AA (at least 4.5:1 for normal text). White on Dusk Sky is 7.2:1.

### Don't:
- **Don't** round corners.
- **Don't** use blurred shadows, glows or gradients.
- **Don't** use smooth easing (`ease`, `ease-in-out`) on transitions or animations.
- **Don't** add a second warm colour, and don't use Marigold as a band background or for body text.
- **Don't** set sentences, big headings or button text in the pixel face.
- **Don't** describe a feature in a paragraph under its section heading. Show the feature.
- **Don't** hand-write a landing demo that the app's own data and helpers can build.
- **Don't** use game words (party, quest, XP, levels) in copy, component names or section names.
- **Don't** show where the team is: no coordinates, city names or campus names. A posting's own job location is product data and stays.
- **Don't** copy colours or fonts from the older app pages into new work.
