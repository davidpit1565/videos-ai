# Image and picture prompts, with the phone-UI safe area built in (15.11.2026)

Why: the "Me with Claude / Me with ChatGPT" picture was cut at the right edge and covered by Instagram's buttons and captions (see CLAUDE.md, 15.11.2026, and `channel/assets/ig-ui-overlap-picture-2026-11-15.jpg`). Numbers are measured on ONE screenshot; verify on a second phone.

## Layout block to paste into EVERY image-generator prompt (Gemini, ChatGPT images, etc.)
```
Vertical 9:16 image, 1080 x 1920 pixels.
Safe layout: all text, speech bubbles, faces and key objects must sit inside the
central area: 10% from the left and right edges, 14% from the top, and above 65% of the height.
In the vertical band between 55% and 85% of the height, keep important things
away from the right 20% of the picture.
The outer 10% on the left and right, the top 14% and the bottom 35% are only background:
no words, no faces, nothing the viewer needs. Background may continue to the edges.
One clear idea in the middle. Title text short (max 4 words), large, inside the safe area.
```

## After generating (checklist, 1 minute)
1. Overlay the safe box (x 108-972, y 269-1248; right band: keep x <= 864 for y 1056-1632) on the image and look.
2. No letter touches the box edge; nothing needed is under the right button column.
3. Post a test as a trial or story-less draft and screenshot it on the phone before the final post.
4. Caption and title text must not repeat words the picture already shows.

## Prompt skeleton (fill the slot)
`[LAYOUT BLOCK] Subject in the middle: <what happens>. Style: <Miki / photo-real / flat>. Title (4 words max): "<title>". Colours: <accent>. No extra text. No logos except <real logos named>.`
