# Chimora

**A voice-first front desk for solo appointment businesses.**

When a visitor arrives while an owner is busy, Chimora checks a sample
schedule, explains whether there is a likely appointment match, and drafts a
polite reply for the owner to review. It is designed as a simulated Alexa+
experience in a web app, one of the accepted Alexa+ track paths.

## Run the demo

Requirements: Python 3.10 or newer and uv.

~~~sh
uv sync --frozen --all-extras
uv run uvicorn chimora.app:app --reload
~~~

Open <http://127.0.0.1:8000>. No account, device, API key, database, or
third-party service is needed. The app starts with a small synthetic repair
studio schedule.

## Deploy a judge-accessible demo

The repository includes a Render Blueprint in [render.yaml](render.yaml).
After making the repository public, connect it to Render as a Blueprint and
deploy the `chimora` web service. Render supplies a public URL and checks
`/api/state` for health. The free service may sleep when idle, so allow for a
cold start before recording or evaluating the demo. All app data is synthetic
and stored in memory; a restart resets the sample schedule.

## Try the three arrival scenarios

1. **Expected arrival:** Elena says she has the 3:00 PM appointment and arrives
   at 2:58. Ask “Is my 3 o’clock here?” to see the schedule match and timing.
2. **Early arrival:** Marcus says he has the 4:00 PM appointment and arrives
   30 minutes early. Chimora suggests a wait-or-return reply.
3. **Unrecognized visitor:** A doorbell event arrives without a stated name or
   booking time. The assistant says it cannot match confidently and suggests
   asking the visitor for details.

The “What should I tell them?” prompt opens a reply draft. Edit, approve, or
dismiss it. Approval is recorded in the demo, but no message is delivered.
The text box supports typing; browsers that offer Web Speech input also show
an optional microphone control. Browser speech-recognition availability and
audio handling depend on the browser; typing avoids microphone use.

## How it works

- doorbell_event adds one of three controlled sample arrivals.
- list_appointments reads the synthetic daily schedule.
- match_arrival only matches a booking when the visitor-stated name and time
  correspond to the schedule. It does not infer identity.
- draft_reply creates an editable reply with pending status.
- approve_reply records the owner’s approval in the local simulation.

The local, rules-based assistant selects a short tool plan from the visitor
event or the owner’s question. For example, an appointment question selects
`list_appointments` and `match_arrival`; a reply request selects
`draft_reply`. The app shows the plan and each tool result in a trace. This is
a **simulated Alexa+ web experience** with a deterministic tool-using agent;
it does not use a hosted language model or third-party agent framework, and it
is not a live Alexa+ add-on or an MCP server.

## Safety and demo boundaries

- All visitors, bookings, and arrival times are synthetic.
- No camera, face recognition, door lock, real appointment provider, or
  messaging service is connected.
- Every reply remains a draft until the owner approves or dismisses it.
- An approval only changes the demo record. It does not send anything.
- The app stores state in process memory; restarting it resets the sample data.

## Hackathon submission checklist

The exact requirements and a prepared Devpost description are in
[docs/submission-checklist.md](docs/submission-checklist.md) and
[docs/devpost-submission.md](docs/devpost-submission.md). The code repository
must either be public with an open-source license or remain private and be
shared with `testing@devpost.com` and all five Amazon reviewers. For a private
repository, verify that every invitation is accepted. A working demo, a public
English YouTube/Vimeo video under three minutes, and product feedback are also
required.

The app and GitHub repository are both named **Chimora**. The repository is
currently private (checked October 22, 2026). Before submission, either make
it public under the included MIT license or invite the required Devpost and
Amazon reviewers and confirm their access.
The submission deadline shown by Devpost is October 23, 2026 at 12:00 PM PDT
(10:00 PM GMT+3).

## License

MIT. See [LICENSE](LICENSE).
