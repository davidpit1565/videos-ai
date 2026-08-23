# יום ראשון — מכאן ישר לעבודה

הכל מעודכן ומאומת. אין כאן הסברים והיסטוריה — רק מה עובד, מה נשאר, ואיפה.

---

## הכתובות

| מה | כתובת |
|---|---|
| האתר הציבורי | `actually-works-studio.vercel.app` |
| הסטודיו (עם קוד) | `actually-works-studio.vercel.app/studio` |
| **רנדרים — לצפות ולאשר** | `actually-works-studio.vercel.app/renders` |
| עמוד פרק 01 | `actually-works-studio.vercel.app/e/1` |
| בדיקת חיבורים | `actually-works-studio.vercel.app/api/connections` |
| הריפו | `github.com/davidpit1565/videos-ai` |

**הקוד לסטודיו:** ‏Vercel → actually-works-studio → Settings → Environment Variables →
`STUDIO_PIN` → שלוש נקודות → Edit.

הכתובות הארוכות של Vercel (`...-9riyu0djm-...`) הן פריסות קפואות. תשתמש רק בקצרות.

---

## מה עובד ומאומת

| | |
|---|---|
| אינסטגרם | ✅ מחובר · `david_pitchkhadze` · 86 עוקבים · נמשך חי |
| Beehiiv API | ✅ מחובר |
| מסד נתונים | ✅ מסונכרן בין המק לטלפון |
| הסוכן בסטודיו | ✅ מפתח קיים |
| האתר הציבורי | ✅ 5 דפים, לא קופצים לסטודיו, הסטודיו נעול |
| ניווט וחיפוש | ✅ ‏Episodes · Prompts · Search · About |
| עדכון אוטומטי | ✅ הסטודיו מושך מספרים בכל פתיחה |
| טופס הרשמה | ✅ שומר אצלנו ומעביר ל-Beehiiv |
| בדיקת עיצורים | ✅ אוטומטית בבנייה, כולל על הקובץ המוגמר |

---

## שלך — שלושה דברים, בסדר הזה

### 1. מייל ברוכים־הבאים (‏5 דקות)

`app.beehiiv.com` → **Settings** → **Emails** → גלול עד **Preset Emails** → **Welcome Email**

**Subject:**

```
You're in. Here's the first setup.
```

**גוף המייל:**

```
You just gave me your email, so I'll be straight about what happens now.

One email a week. One AI setup in each: the exact screen, the exact paste,
and the part that breaks. Nothing else — no course, no launch, no funnel.

Start with this one. It's the setup most people should have made first:

  One paste, and ChatGPT stops giving you the obvious
  actually-works-studio.vercel.app/e/1

It takes about two minutes. The page has the five clicks, the prompt in
full, and — this is the part other tutorials skip — what it will NOT do.

Two things worth saying out loud:

I'm David. I'm 18, I'm in Flanders, and this is not my day job. Every setup
I publish, I ran first. If something only half works, the episode says
which half.

And if a setup here breaks for you, reply to this email and tell me. That
is genuinely more useful to me than a like, and it's how the next episode
gets better.

— David
Actually Works

Unsubscribe in one click, any time. Nothing is sold to anyone.
```

→ **Save** → חזור לאותו מסך → **הדלק** את `Enable a welcome email that is sent to new
subscribers`

**המתג הוא השלב הקריטי.** בלעדיו הכל נראה תקין ושום דבר לא נשלח.

### 2. מעבר לתוכנית `Launch` — חינם

**Settings** → **Billing** → **Change plan** → **Launch** ($0)

אתה על `Max trial`, יום 3 מ-14. `Max` הוא $96 לחודש. `Launch` חינם לתמיד, עד 2,500
נרשמים, וכולל את ה-API ואת מייל הברוכים־הבאים. יש לך נרשם אחד. **המעבר לא מוריד כלום.**

אם הוא מציע הנחה כדי שתישאר — תסרב.

### 3. לפרסם את פרק 01

רק אחרי שתאשר את הסרטון. השלבים בקובץ `publish/SETUP.md`, ואז בסטודיו:
**פרקים** → הפרק → סימון `live` + מזהה המדיה.

---

## תזכורת שביקשת — על המודל

**סשן חדש, לא המשך של הקודם.** הדף הזה קיים בדיוק בשביל זה. סשן שרץ ימים קורא את כל
ההיסטוריה בכל תור — ב-21.8 זה היה 194 מיליון טוקן מול 572 אלף שנכתבו בפועל, פי 340.

**ובאמצע העבודה:** ברגע שקטע הופך למכני — 18 סקריפטים לפי תבנית, פרסום, תיקוני טקסט,
עדכון מסמכים — **תעבור ל-Sonnet 5 לאותו קטע.** זה בערך 2.5x זול וההפרש לא נראה שם.
זה רשום גם ב-`CLAUDE.md`, כך שכל סשן אמור להגיד לך את זה לבד לפני שמתחילים.

`Opus` נשאר לדיבוג, להחלטות, ולכל מה שטעות בו עולה לך יום.

`/fast` לא חוסך — הוא Opus עם פלט מהיר, לא מודל קטן יותר.

---

## שלי

| | מצב |
|---|---|
| הסרטון | בבנייה. לא נשלח עד שהמילה `3` נמדדת בטווח **בקובץ המוגמר** — ראה "מהלילה" למטה |
| רשימת 20 פרקים | ✅ `channel/slate-20.md` |
| פרסום אוטומטי לאינסטגרם | לא התחיל |
| ריענון אוטומטי של טוקן אינסטגרם | לא התחיל |
| ה-G הפלמית | לא התחיל |

---

## מהלילה (23.8) — שני התיקונים שביקשת

### 1. `line12-candidates.wav` — תוקן, PR נפרד

**[PR #50](https://github.com/davidpit1565/videos-ai/pull/50)** — draft.

הסיבה: `line_doctor.py` תמיד כתב `-c:a aac` בלי קשר לסיומת ש-`--out` ביקש. כש-`--out`
היה `audio/voice/line12-candidates.wav`, ffmpeg כתב סטרים AAC גולמי לתוך מעטפת WAV —
זה עובר בשקט בכתיבה, אבל ל-WAV אין framing תקין ל-AAC, אז כל דבר שמנסה לקרוא את
הקובץ שוב (בדיוק מה שהסטודיו עושה בהמרה ל-m4a לניגון) נשבר עם מאות שגיאות דקודר.
שחזרתי את זה מקומית עם קובץ סינתטי לפני שתיקנתי — אותה שגיאה בדיוק. עכשיו הקודק
נבחר לפי הסיומת של `--out` (`aac`/`.m4a`, `pcm_s16le`/`.wav`), וסיומת לא מוכרת
נדחית מראש.

**הקובץ הפגום עצמו** לא בריפו (ב-`.gitignore`, `audio/voice/*.wav`) — צריך להריץ
מחדש את הפקודה של שורה 12 כדי לקבל קובץ מועמדים תקין.

### 2. reel-01 (v22) — שני משלושה נסגרו, השלישי בעבודה

**[PR #51](https://github.com/davidpit1565/videos-ai/pull/51)** — draft, **עדיין לא עובר check.sh במלואו, אל תשלח**.

- **חפיפות טקסט (עד 247px):** תוקן ומאומת (0 חפיפות). הסיבה האמיתית — לא היישור,
  אלא ש-`export/karaoke.py` (הכלי שהופך כתובית למשפט-שלם ל-2-3 מילים בקצב הדיבור)
  **מעולם לא רץ על ה-build הזה**. הכתוביות היו עדיין משפט שלם מה-`CUES`, בדיוק התקלה
  שה-docstring של karaoke.py מתאר. אחרי שהרצתי אותו נשארה חפיפה גיאומטרית אחת (שורת
  "Data controls" בתפריט ה-Settings פשוט ארוכה מדי) — הורדתי אותה, 5 שורות תפריט
  מספיקות.
- **שורות 5-9 חלשות + S חד בשורה 14:** תוקן ומאומת ("nothing flagged"). הכלי כבר
  קיים — `audio/voice_doctor.py --repair` — פשוט לא רץ.
- **המילה "three":** **חקרתי, לא הנחתי.** `build_voice.py` בודק את ה-burst של המילה
  על הטייק *לפני* שהוא מואץ ב-rubberband (עד 20%, כי שורה 7 נאמרת ב-1.8 הברות/שנייה
  מול רצפה של 4.6) — וההאצה לא נבדקת שוב. מדדתי: "three" בקובץ הסופי הוא +22.6..28.8
  dB (burst נקי; הטווח התקין +4..+13 dB), ומתיחה נוספת של המילה המבודדת רק מחמירה
  את זה. הוספתי שתי הגנות קבועות: (א) `build_voice.py` בודק את המילה שוב מיד אחרי
  ההאצה, ואם היא נשברה — משאיר את הטייק האיטי במקום לשלוח את המהיר השבור; (ב)
  `voice_doctor.py`, שזה מה ש-`check.sh` בפועל מריץ, עכשיו מודד את המילה על **הקובץ
  שבאמת נשלח**, אז גם אם מישהו יתעלם מקוד היציאה של build_voice.py, השער הזה יתפוס
  את זה — בדיוק מה שרשמת ידנית בשורה למעלה, עכשיו אוטומטי בכל `check.sh`.

  **מה שלא נגמר הלילה:** לתקן את הטייק עצמו דורש להריץ מחדש TTS אמיתי (`chatterbox-tts`
  + `torch`, כמה ג'יגה של משקלים). זה לא היה זמין בסביבת העבודה המרוחקת הזאת בהתחלה —
  התקנתי את זה תוך כדי (ffmpeg, numpy/scipy/librosa, faster-whisper, playwright, ולבסוף
  torch+chatterbox-tts) והרצתי בנייה מלאה מחדש; אם היא הספיקה להיגמר לפני שאתה קורא
  את זה, התוצאה כבר ב-PR #51 כ-commit נוסף. אם לא — יש קובץ build_voice.py מחוזק
  שממתין רק להרצה חוזרת:

  ```
  python3 audio/build_voice.py --cues video/reel-01-v22.html --out audio/voice/ep01-v24.wav \
    --exaggeration 0.50 --cfg 0.30 --closes 4,8,13,15
  ```

  ואז `export/karaoke.py` + `export/retime.py` + רנדר + `check.sh` מלא, לפני שמסמנים
  משהו כמוכן.

---

## הרשימה, בקצרה

`channel/slate-20.md` — מדורגת לפי מדידת ביקוש אמיתית (‏160 סרטונים, 8 נושאים).

- **‏13 מ-20 לא צריכים שום דבר שאין לנו.** אפשר להתחיל מיד.
- **‏03 ו-04** (n8n, ומכירה לעסק) הם 60% מהביקוש שנמדד וגם קו ההכנסה הראשון.
- **‏14** — "מאפס עד 100, לבד, בקול שלך" — הפרק שאף אחד אחר לא יכול לעשות.
- **‏04 חוסם על לקוח אמיתי אחד.** בלי זה זו תיאוריה, ומספרים מומצאים אסורים.

---

## מה שצריך ממך כדי להתקדם מעבר לזה

**חשבון n8n** (שכבה חינמית) — פותח את פרקים 03 ו-08, הביקוש הגבוה במדידה.
**חמישה שמות של עסקים** — כשהסרטונים רצים, לא לפני.
