# Code Review Interview

Welcome! In this round you'll review a pull request written by a teammate, just like you would at work. There's no trick and no running code: read it, think about what could go wrong, and tell us what you'd say to the author.

**Round length:** 45 minutes

## Pick your language

The same pull request exists in three languages. The problems are the same in each, and no language scores higher than another. Open the one you're most comfortable with from the **Pull requests** tab:

| Language | Pull request | Code |
|---|---|---|
| Python (Flask, requests) | `[Python] Add order refunds and payment webhooks` | [`python/`](python/) |
| Java (Spring Boot, HttpClient) | `[Java] Add order refunds and payment webhooks` | [`java/`](java/) |
| Go (net/http, crypto/hmac) | `[Go] Add order refunds and payment webhooks` | [`go/`](go/) |

Review it in the **Files changed** tab. Click the `+` next to a line to leave a comment, or talk your comments through with the interviewer. Either is fine.

## What we're looking for

- **You find the problems that matter most.** Think about security, money, losing or corrupting data, and what happens when things fail, not only style.
- **You put them in order.** Tell us which issues must be fixed before merging and which can wait.
- **You explain the impact.** "If X happens, then Y goes wrong" is more useful than "this is bad".
- **You suggest a fix**, even a rough one.
- **You're kind and clear.** Review the code, not the person.

## Ground rules

- You don't need to run the code. Assume it compiles.
- Ask about anything that's unclear, such as how a helper behaves or how the system is used.
- You won't be marked down for missing small things. Finding the important problems matters more than finding all of them.

## Severity labels

Please start each comment with one of these:

| Label | Meaning |
|---|---|
| **Blocker** | Must be fixed before merging. Causes data loss, a security hole, lost money, or a crash. |
| **Major** | Should be fixed before merging. Wrong behavior or a real risk, but less severe. |
| **Minor** | Worth fixing, but could be a follow-up. |
| **Nit** | Style or small polish. Never blocks a merge. |

## What a good review comment looks like

An example from a different piece of code, so it gives nothing away:

| Weak comment | Strong comment |
|---|---|
| "This cache is wrong." | **Major:** This cache never expires entries, and the key includes the full search text. Every unique search adds an entry, so memory grows until the service is restarted, and stale prices are shown in the meantime. Could we cap it (for example 10,000 entries, least-recently-used out first) and expire entries after 5 minutes? |

The strong comment says what is wrong, what will happen because of it, and a way to fix it, with a severity label and a friendly tone.

## How the 45 minutes go

| Time | What happens |
|---|---|
| 0–5 min | Introductions and format |
| 5–8 min | Read the PR description and ask questions about the context |
| 8–33 min | Review the code. Thinking out loud is encouraged. |
| 33–42 min | Discussion of what you found |
| 42–45 min | Your questions for us |

## Repository layout

- `schema.sql`: the database tables, shared by all three versions.
- `python/`, `java/`, `go/`: the payments service in each language. On `main` they contain only the existing pieces: the database helpers, the merchant API-key check, and the shipping client. Those already exist, work correctly, and are not part of the PR.
