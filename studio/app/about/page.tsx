import Link from "next/link";

export const metadata = {
  title: "About — Actually Works",
  description: "Who runs this channel, and the one rule it holds to.",
};

export default function About() {
  return (
    <main className="site" dir="ltr">
      <p className="kicker">
        <Link href="/">Actually Works</Link> · About
      </p>
      <h1>Every setup here was run before it was published.</h1>

      <section>
        <p>
          I am David. I am eighteen, I live in Flanders, and I have a day job that is
          not this. This channel is what I do with the hours around it.
        </p>
        <p>
          It exists because of a specific frustration: almost every AI tutorial shows
          the part that works. You copy it, you get a different screen, and the video
          never mentions the step where it breaks. So that step gets the same screen
          time here as the happy path.
        </p>
      </section>

      <section>
        <h2>The rule</h2>
        <p>
          Nothing gets published that has not been run. If a setup only half works, the
          episode says which half. If a number is an estimate, it is labelled as one.
          There is no reason to trust me yet, so the only thing I can offer is being
          checkable.
        </p>
      </section>

      <section>
        <h2>The work behind it</h2>
        <p>
          The episodes are produced by a pipeline I built: the narration is my own voice,
          cloned locally, and every reel passes a set of measurements before it is sent —
          speech pacing, caption position against the platform's safe area, loudness,
          frozen frames. Each of those checks exists because a real defect got through
          first.
        </p>
        <p>
          If you want the same kind of thing built for your business, that is the paid
          side, and it is the same promise: it gets tested before it gets handed over.
        </p>
      </section>

      <footer className="sfoot">
        <Link href="/">Episodes</Link>
        <Link href="/join">Email list</Link>
      </footer>
    </main>
  );
}
