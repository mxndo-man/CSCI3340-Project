# User stories: first draft (issue #12)

*Add each story as one board item in Backlog, ordered as below. Interviews (Oct 28) will revise them.*
*Format: "As a ___, I want ___ so that ___," plus acceptance criteria that will be used to check & prove it's done.*

| # | Story | Acceptance Criteria | Milestone | Owner |
| --- | --- | --- | --- | --- |
| 1 | As a student, I want to sign up and log in so that my boards and applications are mine. | Sign up, log in, log out; password reset email (console/Mailpit in dev); app pages redirect to login when logged out | D2 | Azaelp2005 |
| 2 | As a student, I want to set my display name, graduation term, and time zone so that friends recognize me and reminders arrive at the right hour. | Edit profile page; display name shows on boards and comments | D2 | Azaelp2005 |
| 3 | As a student, I want new internships from employers to appear automatically so that I don't have to check each company's site. | Sync runs every 6 h; new postings added, changed ones updated, removed ones marked closed; one failing employer doesn't stop the rest | D2 | liamreeves34 |
| 4 | As a student, I want to filter internships by citizenship, clearance, degree, work mode, deadline, and pay so that I only see ones I can apply to. | Filters combine; sorted by deadline; paginated; closed postings badged | D2 | mxndo-man |
| 5 | As a student, I want to see where each fact about a posting came from so that I know whether to trust it. | Each field shows its source (job board, AI, person); AI fields show the sentence they came from | D2 | mxndo-man |
| 6 | As a student, I want to create a board and share a join code so that my friends and I can collect postings together. | Creator becomes owner; join by code; members can leave; owner can remove members; non-members can't see the board | D2 | mxndo-man |
| 7 | As a board member, I want to save postings to our board and comment on them so that we can share what we know. | Save/remove; comments visible only to members | D2 | mxndo-man |
| 8 | As a student, I want to paste a posting's text or upload a PDF so that jobs from sites we don't sync are tracked too. | Fields fill in within seconds without the page hanging; pasting the same posting twice doesn't duplicate it; if reading fails, a manual form opens with the text | D2 | mxndo-man, liamreeves34 |
| 9 | As a student, I want to confirm or fix facts the AI wasn't sure about so that everyone sees correct information. | Review queue shows each uncertain field with its evidence; accept or edit; users corrections are never overwritten; posting marked verified when all are resolved | Final | mxndo-man, liamreeves34 |
| 10 | As a student, I want to track each application's status so that I know where I stand everywhere. | One application per posting; statuses saved then applied to a profile. current status like "applied" "interview" then offer/rejected/withdrawn. | Final | Azaelp2005 |
| 11 | As a student, I want tasks with due dates, optionally tied to an application, so that I don't forget next steps. | Create/edit/delete/mark done; only I can see mine | Final | Azaelp2005 |
| 12 | As a student, I want to save a search and be told about new matches so that good postings find me. | Saved searches are private; new matches appear in the digest | Final | Azaelp2005 |
| 13 | As a student, I want a home page showing this week at a glance so that I know what to do first. | Deadlines in the next 14 days, applications by status, recent board postings; works for a brand-new user | D2 | mxndo-man, Azaelp2005 |