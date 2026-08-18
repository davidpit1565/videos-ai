# Guaranteed vs. "the model is following instructions"

The user asked for this distinction to be explicit. It is the difference between a claim
about **software** and a claim about **a language model's behaviour**, and conflating the two
is the single most common dishonesty in tutorials like this one. Scene S12 is built on this
table; keep it accurate if you re-edit.

## ✅ Mechanically guaranteed by the Custom Instructions feature

These are properties of OpenAI's product. They either happen or they're a bug.

- Your text is **stored** on your account when you press Save.
- It is **delivered to the model** at the start of every new conversation while the feature is enabled.
- It applies **across your devices** — web, mobile app, desktop app — because it lives on the account, not the device.
- It **persists** until you edit or delete it. It doesn't expire and it doesn't need reactivating.
- It applies to **new chats**. Conversations that already existed before you saved it may not reflect it.

## ⚠️ Not guaranteed — this is the model choosing to comply

These are tendencies, not mechanisms. They're strong, but they're probabilistic.

- That **every line is followed every time.** Instructions compete with each other and with the content of your message.
- That the **nine-step process runs in full** on every complex question. The model decides what "complex" means, and it will sometimes decide differently than you would.
- That it **reliably picks the right methods.** It's very good at this. It isn't perfect, and it has no way to tell you when it got the choice wrong.
- That **depth and tone stay consistent** between chats, or between two runs of the same question. Two identical questions can produce noticeably different shapes of answer.
- That it **won't drift in a long conversation.** The further a conversation goes, the more the immediate context outweighs the standing instruction. This is the most common real-world failure: it works beautifully for twenty messages and then quietly stops feeling special.
- That it **never invents facts.** The instruction says not to. That measurably reduces it. It does not eliminate it, and no instruction can.

## Language to use on screen

**Say:**
- "Your instruction is delivered in every new chat."
- "ChatGPT will *usually* pick the right methods."
- "This makes it think more carefully. It doesn't make it correct."
- "Delivery: guaranteed. Obedience: very likely — not certain."

**Don't say:**
- "This forces ChatGPT to…" — nothing here forces anything.
- "This unlocks…" — nothing is locked.
- "This upgrades your ChatGPT" — the model is identical.
- "Now ChatGPT will always…" — it won't always do anything.
- "This makes ChatGPT smarter" — it makes its *output* better by directing effort that was already there.

## The honest one-line summary

> The plumbing is guaranteed. The behaviour is very likely. Anyone who tells you the behaviour
> is guaranteed is describing software that doesn't exist.
