# Chimora demo run sheet

The current narrated, upload-ready clip is
[`submission-assets/chimora-demo.mp4`](../submission-assets/chimora-demo.mp4)
(64 seconds, with English narration and captions burned in). The matching
[caption file](../submission-assets/chimora-demo.srt) and
[voiceover script](../submission-assets/chimora-demo-narration.txt) are included too.
The public YouTube or Vimeo URL is recorded in the Devpost entry.

## Reset

~~~sh
uv run uvicorn chimora.app:app --reload
~~~

Open <http://127.0.0.1:8000> and click **Reset demo**.

## Expected visitor

1. Point out the **Alexa+ track · simulated web app** label. Say that this is
   a local simulation with sample data, not a live Alexa+ connection.
2. Click **Expected arrival**. In the action trace, show the assistant plan,
   schedule lookup, arrival match, and owner-review draft.
3. Point out Elena’s 3:00 PM booking and the 2:58 PM arrival.
4. Ask or click **Is my 3 o’clock here?**
5. Show the appointment list and the transparent tool trace.
6. Edit the suggested reply and approve it.
7. Say clearly that approval only changes the local demo record; no message was sent.

## Early visitor

1. Click **Reset demo**.
2. Click **Early arrival**.
3. Point out that the visitor stated the 4:00 PM booking and arrived 30 minutes early.
4. Read the wait-or-return draft.

## Visitor with no booking details

1. Click **Reset demo**.
2. Click **Unrecognized visitor**.
3. Show that the app leaves the match unresolved and drafts a question instead
   of guessing who they are.

## Close

The schedule match is based on details the visitor states. The demo uses no
camera, face recognition, door lock, or message delivery. The owner reviews
every reply.
