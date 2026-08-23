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
| אינסטגרם | ❌ חסום — `API access blocked` (OAuthException 200) בצד מטא, לא טוקן שפג. צריך לבדוק ב-`developers.facebook.com/apps` (מחשב, לא טלפון — יש checkpoint לופ בדפדפן מובייל) אם יש נר/התראת policy violation בדשבורד. עדיין לא נבדק — ניסיון בטלפון נכשל בלופ אישור |
| Beehiiv API | ✅ מחובר · 6 נרשמים |
| מסד נתונים | ✅ מסונכרן בין המק לטלפון |
| כרטיס שימוש בקלוד בסטודיו | ✅ עובד — הבארים (session/weekly %) נשמרים ומוצגים נכון. הנב בר בתחתית הסטודיו תוקן עם `100lvh` (לא JS) אחרי שני ניסיונות כושלים — ראה היסטוריה ב-`shell.tsx` אם זה קופץ שוב |
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
| reel-01 (v22) | ❌ נכשל בשער. שלוש תקלות אמיתיות: (1) חפיפת טקסט על המסך — עד 247px ב-18s, כמה נקודות נוספות ב-`video/reel-01-v22.html`; (2) שורות 5-9 חלשות מדי ברמה, שורה 14 עם S חד; (3) **המילה "three" עדיין שונה במיקס הסופי ממה שנמדד בטייק** (`audio/reel01-narration-v22.wav`) — חשוד ב-time-stretch או trim, לא נבדק לעומק. פרטים מלאים ב-`studio/public/reels/reel-01.gate.txt` |
| line12 candidates ("not a list") | ❌ `audio/voice/line12-candidates.wav` קיים עם 4 אופציות (seed/exag/cfg), אבל ה-WAV פגום בפועל — ffmpeg זורק מאות שגיאות דקודר AAC בהמרה ל-m4a. לא נבדק למה ה-WAV פגום (איך `line_doctor` כתב אותו) |
| רשימת 20 פרקים | ✅ `channel/slate-20.md` |
| פרסום אוטומטי לאינסטגרם | לא התחיל |
| ריענון אוטומטי של טוקן אינסטגרם | לא התחיל |
| ה-G הפלמית | לא התחיל |

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
