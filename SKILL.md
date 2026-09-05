---
name: free-linkedin-outreach
description: Research and verify job-outreach contacts for target companies or job posts, write concise personalized LinkedIn connection messages, and create a safe one-click Copy + Open LinkedIn outreach queue with completion tracking. Use when a user asks to find recruiters, hiring managers, product or engineering contacts; create LinkedIn outreach batches; personalize connection notes under 300 characters; correct current-versus-former employment mistakes; or turn a contact spreadsheet/list into an interactive outreach workflow.
---

# Free LinkedIn Outreach

## Problem

Job seekers lose time opening profiles, copying messages, and tracking outreach manually. Public results also mix current employees with alumni, which can produce inaccurate company-specific messages.

## Solution

Build a verified contact batch and an interactive queue. Each contact receives a role-aware message and one **Copy + Open LinkedIn** action. Clicking it copies the message, opens the profile, marks the contact prepared, turns the contact block green, and updates progress. Keep the final Connect, Add a note, review, and Send steps manual.

## Required inputs

Collect or infer:

- Target companies or a job-post URL
- Desired roles and functions
- Candidate strengths from the resume, LinkedIn profile, or conversation
- Contacts per company; default to 5
- Batch size; default to 20 contacts unless the user specifies companies instead
- Known prior contacts or outreach history to avoid duplicates

Ask one focused question only when a missing input would materially change the results.

## Workflow

### 1. Understand the target

For a job post, extract the company, role, location, product/domain, responsibilities, and likely reporting function. For a company list, preserve the user's order or stated priority.

Summarize the target companies before contact research when the user asks to review priorities first.

### 2. Find the right people

For each company, target 5 useful contacts:

1. Recruiter or talent acquisition partner aligned with the role or location
2. Second recruiter, talent leader, HR business partner, or people leader
3. Hiring-manager-level contact in the relevant function
4. Product, engineering, software QA, AI/data, program, or operations team member
5. Another relevant manager, senior individual contributor, or referral route

At small companies without two recruiters, use a people/HR leader or founder and label the substitution honestly. Never pad the list with unrelated contacts.

### 3. Verify identity and employment

Use public web search first and LinkedIn/profile pages as primary identity evidence when available. Use an authenticated browser only when direct interaction or missing public detail requires it.

Verify all of the following before inclusion:

- Correct person
- Correct company
- Current title or relationship status
- Direct LinkedIn profile URL
- Relevance to the target role

Label each contact as `Current`, `Alumni`, `Parent company`, `Founder/advisor`, `Ecosystem`, or `Uncertain`. Prefer current employees. Exclude weak matches instead of presenting guesses as facts.

If a company was acquired, renamed, or closed, identify the best current route and preserve the legacy relationship label.

### 4. Prevent mistakes and duplicates

Compare names and normalized LinkedIn URLs against prior batches, trackers, and outreach history. Do not reuse a person unless the user explicitly asks.

Never describe an alumnus as a current employee. If current employment cannot be verified, remove the company name from the message and make the request a general job inquiry or referral question.

### 5. Write the message

Keep every message below 300 characters including spaces. Aim for 210–275 characters so LinkedIn formatting does not push it over the limit.

Use this structure:

1. `Hi {First name}, I'm {Candidate name}.`
2. State 2–4 relevant strengths with evidence from the candidate's background.
3. State interest in the company, function, or kind of opportunity.
4. Ask the person to review the profile, suggest a fit, or connect the candidate with the right team.

Adjust the action step by recipient:

- Recruiter: ask for profile review and matching roles.
- Hiring manager: ask whether the background fits the team.
- Team member: ask which team or role would be relevant.
- Executive/founder: ask for direction to the appropriate person.
- Alumnus/uncertain: ask a general job or career-direction question without implying current employment.

Avoid generic praise, exaggerated enthusiasm, fake familiarity, and claims about work that were not verified. Do not start with phrases such as “your work is fascinating.” Lead with the candidate's value and a clear action.

### 6. Validate the contact file

Store contacts as JSON or CSV using [references/contact-schema.md](references/contact-schema.md). Run:

```bash
python3 scripts/validate_outreach.py contacts.json --contacts-per-company 5 --max-message-length 299
```

Fix all errors before creating the queue. Treat warnings about missing recruiter coverage or uncertain employment as review items.

### 7. Create the outreach queue

When an in-conversation interactive surface is supported, create a responsive HTML queue in the workspace root and display it in wide mode. Otherwise, create a standalone HTML file.

Required queue behavior:

- Group or filter contacts by company.
- Show name, verified title, function, relationship status, message, and character count.
- Provide one **Copy + Open LinkedIn** button per contact.
- Use a normal LinkedIn profile link with `target="_blank"` and `rel="noopener noreferrer"` so opening remains a user action.
- Copy the customized message on the same click.
- Turn the full contact block green after clicking.
- Change visible status to `Prepared` with a checkmark; never rely on color alone.
- Persist prepared IDs with `localStorage` when available.
- Show prepared count and overall progress.
- Support keyboard use and mobile widths.
- Keep the first render useful without configuration.

Do not automate clicking Connect, Add a note, Send, Follow, or Message on LinkedIn. Do not scrape authenticated LinkedIn pages at scale or bypass rate limits, login walls, or platform protections.

### 8. Final quality check

Confirm:

- Requested company and contact counts match.
- At least two talent/people routes exist per company where feasible.
- Every profile URL is direct and unique.
- Current-versus-former status is explicit.
- All messages are under 300 characters.
- Messages use verified candidate strengths and a concrete action step.
- The button copies, opens, changes status, turns the block green, and updates progress.
- No connection request or message is sent automatically.

## Installation

### From GitHub

1. Clone or download the repository containing this folder.
2. Copy the complete `free-linkedin-outreach` folder into the Codex skills directory, commonly `~/.codex/skills/`.
3. Keep `SKILL.md`, `agents/`, `scripts/`, and `references/` together.
4. Open a new conversation or refresh the Skills page if the skill is not immediately listed.

Alternatively, ask Codex to install the skill from the public GitHub repository URL.

### From ChatGPT Skills

Open **Plugins → Skills**, locate **Free LinkedIn Outreach**, and add or enable it for the workspace.

## Usage

Invoke the skill explicitly:

```text
Use $free-linkedin-outreach for these 10 companies. Find five current contacts per company, including two recruiters where possible, write messages under 300 characters using my resume, and create the Copy + Open LinkedIn queue.
```

For a job post:

```text
Use $free-linkedin-outreach with this job URL. Find the recruiter, likely hiring manager, and three relevant team members. Avoid everyone in my previous batches.
```

For alumni correction:

```text
Use $free-linkedin-outreach to audit this batch. If someone no longer works at the company, rewrite the message as a general job inquiry without the company name.
```
