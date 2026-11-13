---
version: 1
slug: "templates-pages-landing-html"
primary_target: "templates/pages/landing.html"
related_targets: ["static/css/landing.css"]
---

# Landing page (`/`)

**Scope and mode:** the public front page, Persuade. First surface of the replacement visual world; app pages keep the old look until later passes. Standalone template with its own nav and footer; `base.html` untouched.

**Audience and job:** a student mid-hunt, usually on a laptop or phone at night after class. They should believe the people behind this have done the hunt themselves, then create an account. Secondary action: browse internships (only when a Discover page or its preview exists).

**Proof and content:** one sample posting rendered from the preview's fake data with every fact's source shown; a sample board with join code and comments; the status pipeline as a stage path. All demonstration data is labelled sample. Plain product language: no game terms (party, quest, XP, levels) and no location specifics (coordinates, city, campus). No usage numbers or testimonials.

**Constraints:** hero image comes later. A flat stand-in fills the slot; the real file dropped at `static/img/landing/hero-valley.webp` replaces it with no layout change. WCAG 2.1 AA. Checked at 1440 and 390.

**Unresolved:** final hero art; whether hero text needs a scrim once the art lands; when the app shell adopts this world.

## Direction contract

THESIS: The hunt is something you do with friends, not a funnel. Refuses the split hero with product screenshot and the three-icon feature row.

OWN-WORLD: Dusk-sky blue hero over a page of deep meadow greens; marigold is the only warm accent and marks only actions and the current step. Square corners everywhere; blocks carry a lit top face and shaded bottom face; panels use stepped pixel corners. A warm grotesk at very large and ordinary sizes against a small pixel face for measurements: codes, timers, dates, IDs. Ruler ticks edge every section.

STORY: You are not hunting alone; every fact shows where it came from; your friends and your applications live in one place; the builders are in the hunt too; create an account.

FIRST VIEWPORT: Full-bleed voxel valley slot, cover, anchored centre bottom. Nav overlaid on top. Headline "Don't hunt alone." centred in the upper sky at up to 7rem, one line of subcopy, marigold primary block button plus quiet secondary. Lower half left to the image. A solid ruler strip closes the hero with an ID and the date.

FORM: Voxel game world, user-pinned. seed: none (pinned) "voxel art approach with warm, fun inviting gameified aspects"; "Future hero: a voxel art valley image as seen in Voxel_Art_Landing_page.png". Signature interaction: the stage path, where choosing a stage moves the marigold marker and lists that stage's sample applications. Motion grammar: everything moves in steps, nothing eases.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
