# Devpost submission reference — Chimora

**Status:** The entrant reports that the Devpost entry is complete and ready
to submit. Account-specific URLs and personal feedback are kept in Devpost.

**Primary track:** Alexa+
**Experience path:** Simulated Alexa+ web app
**Mini-challenges:** None selected

## Project title

**Chimora — A calmer front desk for the moment someone arrives**

## Project tagline

**Appointment context at the door, with replies the owner approves.**

## Built with

**Python, FastAPI, JavaScript, HTML, CSS, Web Speech API (optional browser input).**
Microsoft Edge online text-to-speech and FFmpeg are used only to add narration
to the submitted demo video; they are not part of the app. No hosted AI model,
AWS service, Alexa+ SDK, Ring API, or MCP server is used.

## Short description

Chimora helps a solo appointment-business owner respond when a visitor
arrives while their hands are busy. It checks the day’s bookings, explains a
schedule match and how early the visitor is, and drafts a courteous reply that
the owner can edit and approve.

## Project description

Small appointment businesses often have no receptionist. A customer can arrive
while the owner is repairing a device, serving another customer, or working in
the back. Chimora turns a simulated doorbell event into useful booking
context without pretending to verify who is at the door.

The demo includes a sample repair-studio schedule and three arrival scenarios:
an expected visitor, someone who arrives early, and a visitor with no booking
details. The owner can ask “Is my 3 o’clock here?” by typing or optional browser
speech input. Chimora shows the schedule lookup and arrival match in a
visible tool trace, explains its reasoning, and drafts a response for owner
review. The owner can edit, approve, or dismiss the reply. Approval is simulated;
the app does not send a message.

The app is an Alexa+ simulated web experience. A local rules-based assistant
selects tools for the current task: an appointment question triggers a schedule
lookup and arrival match, while a reply request creates an owner-review draft.
The plan and tool results are visible in the demo. The assistant is
deterministic and does not use a hosted language model or third-party agent
framework. The app uses synthetic data and local tools; it does not use live
Alexa+, Ring, MCP, a camera, facial recognition, a lock, or a real messaging
integration. These limits are deliberate so the demo stays honest and safe.

## Track-fit notes

The Alexa+ rules allow a simulated Alexa+ experience in a web app using an AI
or agentic tool, without requiring a live Alexa+ connection or MCP surface.
Chimora demonstrates a local deterministic tool-using assistant that
selects and runs tools based on the arrival and owner request. The rules do not
define a minimum model or framework for this simulation path; describe the
implementation exactly and do not claim a live Alexa+ integration.

## Recorded demo video (64 seconds)

The current narrated, upload-ready clip is
[`submission-assets/chimora-demo.mp4`](../submission-assets/chimora-demo.mp4).
It has an English voiceover, burned-in English captions, a separate caption
file at [`submission-assets/chimora-demo.srt`](../submission-assets/chimora-demo.srt),
and the matching voiceover script at
[`submission-assets/chimora-demo-narration.txt`](../submission-assets/chimora-demo-narration.txt).
The voiceover uses Microsoft Edge's online `en-US-AriaNeural` voice through
the `speech.platform.bing.com` endpoint.

1. **0:00–0:11:** Introduce the simulated Alexa+ web experience and trigger an
   expected arrival.
2. **0:11–0:17:** Show the assistant plan and local tool trace.
3. **0:17–0:34:** Ask about the 3:00 PM booking, edit the reply, and approve it.
4. **0:34–0:44:** Show the 30-minute early arrival and suggested response.
5. **0:44–0:58:** Show an unrecognized arrival and the assistant declining to
   guess who it is.
6. **0:58–1:04:** Close on the synthetic data and no-live-integration limits.

The clip is publicly uploaded; its YouTube or Vimeo URL is in the Devpost
entry. It is under three minutes and contains no third-party footage, marks,
or music.

## Try it out

**GitHub repository:** <https://github.com/zalkabsi/Chimora> (public, MIT).

**Public app URL:** The judge-facing URL is recorded in the Devpost entry if
the form requests a “Try it Out” link. The repo includes `render.yaml` for the
service deployment.

## Product feedback reference

The repository supports the factual details below. The entrant’s completed
personal feedback is in Devpost; this file keeps technical context for the
public repository.

- **Developer tools used:** Alexa+ simulated-experience path; Python, FastAPI,
  a browser-based front end, browser speech recognition when available, and
  Microsoft Edge online text-to-speech with FFmpeg for the demo narration.
- **What worked well (repo-backed option):** The three arrival scenarios,
  visible tool trace, and owner-reviewed reply draft make the simulated flow
  straightforward to demonstrate. Keep this only if it matches your experience.
- **What needs work (repo-backed facts):** The app is deterministic and local;
  it does not validate behavior inside a live Alexa+ surface or use a hosted
  language model. Browser speech input also depends on browser support. Add any
  build or resource friction only if it actually happened.
- **Onboarding (repo-backed facts):** The README asks for Python 3.10+ and `uv`,
  then gives two run commands; no account or API key is needed. The repo does
  not record how clear the official Alexa+ resources felt to the entrant.
- **Would you build with Alexa+ again?** The entrant’s response is in Devpost.
- **AWS services:** The app configuration and code document no AWS service use.
  The Devpost entry contains the entrant’s response for the full build.
- **Friction log:** No actual friction log is present. Do not invent one.

## Final submission status

The entrant reports that the Devpost fields, eligibility confirmations,
repository and video links, track selection, and product feedback are complete.
Submit the entry from the entrant’s Devpost account after the final review.

## Sources

- [Hackathon overview and requirements](https://amazonappdev2026.devpost.com/)
- [Official rules](https://amazonappdev2026.devpost.com/rules)
- [Track resources](https://amazonappdev2026.devpost.com/resources)
