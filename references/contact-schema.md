# Contact data schema

Use one object or row per contact.

## Required fields

| Field | Meaning |
|---|---|
| `company` | Target company or legacy brand |
| `name` | Contact's display name |
| `title` | Verified current title or best available relationship description |
| `function` | `Talent`, `Product`, `Engineering`, `Software QA`, `AI/Data`, `Program`, `Management`, or `Referral` |
| `relationship_status` | `Current`, `Alumni`, `Parent company`, `Founder/advisor`, `Ecosystem`, or `Uncertain` |
| `linkedin_url` | Direct LinkedIn profile URL |
| `message` | Customized outreach message under 300 characters |

## Recommended fields

| Field | Meaning |
|---|---|
| `verification_source` | LinkedIn or authoritative public page used for verification |
| `verified_on` | ISO date of the verification pass |
| `confidence` | `High`, `Medium`, or `Low` |
| `priority` | `P1`, `P2`, `P3`, or `P4` |
| `outreach_status` | `Not started`, `Prepared`, `Sent`, `Replied`, `Follow-up`, or `Skipped` |
| `notes` | Acquisition, alumni, location, or routing context |

## Example

```json
[
  {
    "company": "Example Health",
    "name": "Jordan Lee",
    "title": "Technical Recruiter",
    "function": "Talent",
    "relationship_status": "Current",
    "linkedin_url": "https://www.linkedin.com/in/example",
    "message": "Hi Jordan, I'm Apurva, an AI product professional with healthcare AI, EMR integration and software QA experience. I'm exploring product roles at Example Health. Could you review my profile and suggest a fit?",
    "verification_source": "https://www.linkedin.com/in/example",
    "verified_on": "2026-09-05",
    "confidence": "High",
    "priority": "P1",
    "outreach_status": "Not started"
  }
]
```
