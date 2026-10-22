# Devpost submission draft — Chimora

**Primary track:** Alexa+
**Experience path:** Simulated Alexa+ web app
**Mini-challenges:** None selected

## Project title

**Chimora — A calmer front desk for the moment someone arrives**

## Project tagline

**Appointment context at the door, with replies the owner approves.**

## Built with

**Python, FastAPI, JavaScript, HTML, CSS, Web Speech API (optional browser input).**
FFmpeg with its Flite filter is used only to add narration to the submitted demo
video; it is not part of the app. No hosted AI model, AWS service, Alexa+ SDK,
Ring API, or MCP server is used.

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
The voiceover uses FFmpeg's local Flite `slt` voice; the Bing speech host was
unreachable from the rendering environment.

1. **0:00–0:11:** Introduce the simulated Alexa+ web experience and trigger an
   expected arrival.
2. **0:11–0:17:** Show the assistant plan and local tool trace.
3. **0:17–0:34:** Ask about the 3:00 PM booking, edit the reply, and approve it.
4. **0:34–0:44:** Show the 30-minute early arrival and suggested response.
5. **0:44–0:58:** Show an unrecognized arrival and the assistant declining to
   guess who it is.
6. **0:58–1:04:** Close on the synthetic data and no-live-integration limits.

Before submission, upload the clip publicly to YouTube or Vimeo and add its
URL. It is under three minutes and contains no third-party footage, marks, or
music.

## Try it out

**GitHub repository:** <https://github.com/zalkabsi/Chimora> (public, MIT).

**Public app URL:** pending deployment. The repo includes `render.yaml`; after
connecting the repository to Render, deploy the Blueprint and paste the service
URL here if the live Devpost form requests it.

## Product feedback draft

Complete this section with the entrant’s own experience before submission.

- **Developer tools used:** Alexa+ simulated-experience path; Python, FastAPI,
  a browser-based front end, browser speech recognition when available, and
  FFmpeg/Flite for the demo narration.
- **What worked well:** Fill in from your actual build experience. Describe
  whether the rules-based tool flow and visible trace helped you demonstrate
  the scenario.
- **What needs work:** The demo does not validate behavior inside a real Alexa+
  surface and does not use a hosted language model. Describe what you found
  difficult while building or reviewing the official resources.
- **Onboarding:** Describe the resources you actually used and how clear the
  simulated-experience requirements were. Do not say you tested Alexa+ APIs or
  SDKs if you did not.
- **Would you build with Alexa+ again?** Answer based on the entrant’s own
  experience; do not treat this draft as submitted feedback.
- **AWS services:** None are currently used by the app. State this accurately
  if the submission form asks about AWS usage.

## Submission fields still requiring the entrant

- Join the hackathon and submit through the entrant’s Devpost account.
- The GitHub repository is public at
  <https://github.com/zalkabsi/Chimora>; verify the MIT license appears on its
  page and paste the repository URL into Devpost.
- Upload the final demo video publicly to YouTube or Vimeo and add its URL.
- Replace the product-feedback onboarding placeholder with firsthand feedback.
- Confirm entrant eligibility and select the Alexa+ track.
- Describe the local deterministic tool-using assistant accurately; do not
  call it a hosted AI model or a live Alexa+ integration.
- Deploy the app and replace the pending “Try it Out” URL if the event form
  requires a public test link.

## Sources

- [Hackathon overview and requirements](https://amazonappdev2026.devpost.com/)
- [Official rules](https://amazonappdev2026.devpost.com/rules)
- [Track resources](https://amazonappdev2026.devpost.com/resources)
