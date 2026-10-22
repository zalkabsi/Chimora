# Amazon Developer Hackathon: submission checklist

Verified against the [official rules](https://amazonappdev2026.devpost.com/rules)
and [Alexa+ track resources](https://amazonappdev2026.devpost.com/resources).

## Deadline

The rules list Friday, October 23, 2026 at 12:00 PM Pacific Daylight Time.
That is **10:00 PM GMT+3**. Devpost currently displays the same local deadline.

Before starting the entry, the entrant must confirm age-of-majority and
location eligibility, team or organization eligibility if applicable, and that
no sponsor, judge, administrator, or conflict-of-interest restriction applies.
If Chimora existed before August 31, 2026, explain and demonstrate the
significant changes made during the submission period.

The public-facing `work` branch uses a fresh Chimora history root dated
October 22, 2026. Earlier project commits are excluded from that branch. If the
live form asks about prior work, answer based on the project’s actual
development history and describe the changes made during the hackathon window
accurately.

## Do these first

1. Join the hackathon and create a Devpost submission draft in the entrant’s
   account. Check eligibility and select the Alexa+ primary track.
2. Make the project repository available to judges. Either publish it with an
   open-source license, or keep it private and invite `testing@devpost.com`
   plus the five Amazon reviewers: knmeiss, giolaq, anishamalde, mosesroth,
   and emersonsklar. Confirm that all six invitations are accepted.
3. Verify the local demo still runs and that its agent plan and tool trace are
   visible in the recorded clip.
4. Upload the 64-second English demo publicly to YouTube or Vimeo and add its
   URL to Devpost.
5. Complete product feedback for every developer tool, API, or SDK used.

The GitHub repository is already named `Chimora` and is currently private
(checked October 22, 2026). The `work` branch contains a clean Chimora-only
history root and the MIT license. Before submission, make the repo public or
keep it private and invite `testing@devpost.com` plus the five reviewers, then
confirm their access. This personal-account repository grants collaborators
write access.
The repository includes a Render Blueprint, but no hosting account has been
connected and no public app URL exists yet. After making the repository public,
deploy it and add the URL if the live Devpost form asks for “Try it Out.”

## Alexa+ requirement

The primary path is a working Agent Skill or self-hosted MCP server using MCP
specification 2025-11-25 or newer over Streamable HTTP. The rules also explicitly
allow a simulated Alexa+ experience in a web app, built with any agentic tool;
this path does not need an MCP surface or a specific framework. The repository
must contain the simulation source code, and the video must clearly show the
simulation working. Chimora follows this web-app path with a deterministic
local tool-using assistant: it selects a plan, invokes schedule/match or reply
tools, and exposes those actions in the interface. It does not use a hosted
language model or third-party agent framework. The rules do not define a
minimum framework or model for the simulation path, so describe the local agent
accurately and do not claim a live Alexa+ integration.

## Access and judging schedule

The official rules list judging as November 9–20, while Devpost’s schedule page
lists October 26–November 20. The rules say they prevail if materials conflict.
The rules require judge access through judging but do not set an invitation
acceptance date. To cover the discrepancy, aim to have all six private-repo
invitations accepted by October 26, 2026 at 10:00 PM GMT+3. GitHub invitations
expire after seven days, so send them close enough to judging that they remain
valid.

## Devpost form

Complete the required project name, tagline, story/description, built-with
tags, primary Alexa+ track, repository URL, demo video URL, and product
feedback. Check the live event form for additional required fields because
Devpost event questions can vary. If the site is private, include any login
credentials needed to evaluate it; the current app itself has no login.

Product feedback must cover each tool, API, or SDK used: what it was used for,
what worked, what needs work, how onboarding felt, and whether the entrant
would build with it again and why. State AWS services used, or say none if that
is accurate. Feature requests and friction logs are optional; record only real
friction.

## Judging

Stage one is pass/fail: the idea must fit the hackathon and reasonably apply
the track technology. Stage two weights these four criteria equally:

- **Tech implementation:** quality of the build and use of the chosen track.
- **Design:** completeness and clarity of the experience.
- **Potential impact:** a credible customer problem and audience.
- **Quality of the idea:** creative, well-considered use of the ecosystem.

Friction logs are optional but may add up to 10% during down-selection. A useful
entry records the attempted task, steps, expected and actual result, severity,
workaround, and an actionable suggestion. Record only real friction encountered.

## Optional mini-challenges

- **AWS Builder:** use and document AWS services or qualifying Kiro Crew work.
- **Open Source:** make an additional open-source project or contribution
  during the hackathon window, then provide its contribution URL, repository
  URL, GitHub username, and a short explanation. The primary Chimora
  submission by itself does not satisfy this extra-project requirement.

Neither mini-challenge is required for the Alexa+ track submission.

## Before pressing Submit

- [ ] Project description explains what it does and how it works.
- [ ] Required Devpost name, tagline, story, built-with tags, Alexa+ track,
      repository URL, demo URL, and feedback fields are complete.
- [ ] GitHub repository contains source, assets, run instructions, and the
      MIT license; if public, confirm the license appears on the repository
      page, or if private, invite `testing@devpost.com` and all five Amazon
      reviewers and confirm that each invitation is accepted.
- [ ] If the project existed before August 31, describe and demonstrate the
      significant updates made during the hackathon period.
- [ ] Video is public, English, shorter than three minutes, and shows the
      working simulation with clear narration and captions, without unlicensed
      marks, music, or footage.
- [ ] Judges can access the working demo and any required testing instructions
      through judging.
- [ ] Product feedback covers the tools actually used, what worked, what needs
      work, onboarding, and whether the entrant would build with them again.
- [ ] Alexa+ is selected as the primary track; optional mini-challenges are
      selected only if their extra requirements are met.
- [ ] All statements about integrations and demo behavior are accurate.
