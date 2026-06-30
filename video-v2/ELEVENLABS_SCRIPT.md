 Sound
# ElevenLabs Narration Script — Partenon Hackathon Video v2

> Voice recommendation: a calm, confident male or female English voice (e.g., **Adam**, **Bella**, **Antoni**, or a cloned calm narrator).  
> Settings: Stability ~0.45, Similarity ~0.75, Style Exaggeration ~0.25.  
> Model: Eleven Multilingual v2 or Turbo v2.5.

---

## How ElevenLabs reads this

- Use **SSML** in the project/script box (most ElevenLabs voices support `<break>`, `<emphasis>`, and `<prosody>`).
- `<break time="Xms"/>` adds silence. Use it for dramatic pauses.
- `<emphasis level="strong">word</emphasis>` makes a word punchier.
- `<prosody rate="..." pitch="...">` controls speed and tone.
- Each block is a paragraph / scene. Upload the SSML block as one generation, or split into scenes if you want precise timing.

---

## Full SSML narration

```xml
<speak>

<prosody rate="95%" pitch="-2%">

<p>
  <s>Most AI tells you what to do.<break time="500ms"/></s>
  <s><emphasis level="strong">Hermes does it.</emphasis></s>
</p>

<break time="700ms"/>

<p>
  <s>Small business owners do not fail because they lack ideas.</s>
  <s>They fail because the operations eat them alive.</s>
  <s><break time="400ms"/>Receipts.<break time="400ms"/> Invoices.<break time="400ms"/> Follow-ups.<break time="500ms"/></s>
  <s>The work that does not require genius still requires time.</s>
</p>

<break time="700ms"/>

<p>
  <s>We built a home for Hermes inside the business.</s>
  <s><break time="400ms"/><emphasis level="strong">The Partenon.</emphasis><break time="400ms"/></s>
  <s>Seven profiles. One shared memory.</s>
  <s><break time="300ms"/>The Scribe reads the receipts.</s>
  <s>The Herald writes the copy.</s>
  <s>The Collector chases the money.</s>
  <s>The Guardian watches the keys.</s>
  <s>The Strategist plans the week.</s>
  <s>The Diplomat keeps the clients.</s>
  <s>And the Brain remembers everything.</s>
</p>

<break time="700ms"/>

<p>
  <s>Every capability is tagged.</s>
  <s><emphasis level="moderate">Live</emphasis> runs out of the box.</s>
  <s><emphasis level="moderate">Connect</emphasis> needs your credentials.</s>
  <s><emphasis level="moderate">Roadmap</emphasis> is labeled clearly.</s>
  <s>No surprises.</s>
</p>

<break time="700ms"/>

<p>
  <s>You install it.</s>
  <s>You configure the heroes you need.</s>
  <s>You run missions.</s>
  <s>And if you want help, our workshop loads your real business into the system in ninety minutes.</s>
</p>

<break time="700ms"/>

<p>
  <s>The goal is <emphasis level="strong">one million</emphasis> installations.</s>
  <s>Because every install is one more founder spending time on product, customers, and growth.</s>
  <s><break time="500ms"/><emphasis level="strong">Hermes</emphasis> is the agent.</s>
  <s><emphasis level="strong">The Partenon</emphasis> is the home.</s>
</p>

</prosody>

</speak>
```

---

## Plain-text version (if SSML is not supported)

Use this if you are pasting into a simple text box without SSML. Add manual line breaks and punctuation to force pauses.

```
Most AI tells you what to do. [pause]
Hermes does it. [pause]

Small business owners do not fail because they lack ideas. They fail because the operations eat them alive. [pause]
Receipts. [pause] Invoices. [pause] Follow-ups. [pause]
The work that does not require genius still requires time. [pause]

We built a home for Hermes inside the business. [pause]
The Partenon. [pause]
Seven profiles. One shared memory. [pause]
The Scribe reads the receipts.
The Herald writes the copy.
The Collector chases the money.
The Guardian watches the keys.
The Strategist plans the week.
The Diplomat keeps the clients.
And the Brain remembers everything. [pause]

Every capability is tagged.
Live runs out of the box.
Connect needs your credentials.
Roadmap is labeled clearly.
No surprises. [pause]

You install it.
You configure the heroes you need.
You run missions.
And if you want help, our workshop loads your real business into the system in ninety minutes. [pause]

The goal is one million installations.
Because every install is one more founder spending time on product, customers, and growth. [pause]
Hermes is the agent.
The Partenon is the home.
```

---

## Director notes (not read by ElevenLabs)

- **Scene 1 (Hook):** Keep it low and confident. The pause after "do" is critical.
- **Scene 2 (Problem):** Slow down slightly on "eat them alive." The list "Receipts. Invoices. Follow-ups." should feel like punches.
- **Scene 3 (Home):** "The Partenon" should land like a title card. Each hero line should be crisp and rhythmic.
- **Scene 4 (Tags):** Treat Live / Connect / Roadmap like product labels.
- **Scene 5 (Use):** Conversational, not salesy.
- **Scene 6 (Mission):** Build to the final two sentences. End clean, no trailing music overlap.

---

## Suggested output

Generate as one file and save it as:

```
video-v2/assets/narration.wav
```

(or `narration.mp3` if that is what ElevenLabs exports). Once you have it, I will sync it to the images and build the final video.
