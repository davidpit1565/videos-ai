# מייל הברוכים־הבאים

**איפה זה נכנס:** Beehiiv → `Settings` → `Emails` → גלילה למטה עד `Preset Emails` →
`Welcome Email`. (המסמך הזה אמר קודם `Settings → Publication → Welcome email`. זה לא
המסלול; הוא לא נבדק כשנכתב.)

**המתג שקובע אם זה נשלח בכלל:** `Enable a welcome email that is sent to new
subscribers`. בלי המתג הזה דלוק, מייל שנשמר לא יוצא — וזו הסיבה הראשונה ברשימת
"למה מייל הברוכים־הבאים לא נשלח" של Beehiiv עצמם.

הקוד שלנו כבר מבקש מ־Beehiiv לשלוח אותו — ב־`/api/subscribe` מועבר
`send_welcome_email: true` — אבל הבקשה מפעילה את המייל **הזה**, שצריך להתקיים
ולהיות דלוק. גם `Welcome Email` וגם `Welcome Automation` קיימים ב-Beehiiv; אנחנו
רוצים את הראשון, והוא כלול בכל התוכניות כולל `Launch` החינמית.

**חשוב לדעת:** הטקסט הזה יושב אצל Beehiiv, לא בקוד שלנו. אין לנו שרת מייל ואין
לנו איך לשלוח בלעדיו — ולכן זה לא "בונים ושוכחים", זה הדבקה חד־פעמית שלך.

---

## מה שפורסם בפועל, 23.8.2026

**מקור האמת הוא Beehiiv, לא הקובץ הזה.** הטקסט נערך שם ואפשר שיתיישן בשקט, ולכן הוא
משוכפל כאן — והשוואה בין השניים היא הדרך היחידה לדעת שהוא עוד מה שאנחנו חושבים.

### Subject line

```
You're in. Here's the first setup.
```

### Preview text

השורה שמופיעה בתיבת הדואר אחרי הנושא. היא לא חוזרת עליו — היא מרחיבה אותו.

```
Two minutes, five clicks, and the part other tutorials skip.
```

### גוף

```
You just gave me your email, so I'll be straight about what happens now.

One email a week. One AI setup in each: the exact screen, the exact paste,
and the part that breaks. Nothing else — no course, no launch, no funnel.

Start with this one. It's the setup most people should have made first:

One paste, and ChatGPT stops giving you the obvious
actually-works-studio.vercel.app/e/1

It takes about two minutes. The page has the five clicks, the prompt in
full, and — this is the part other tutorials skip — what it will NOT do.

One thing worth saying out loud: every setup here was run before it was
published. If something only half works, the episode says which half.
That's the whole difference, and it's why this list is worth an inbox.

If a setup breaks for you, reply and tell me. That's genuinely more useful
to me than a like, and it's how the next one gets better.

— David
Actually Works
```

## מה נחתך, ולמה

הגרסה הראשונה כללה פסקה שאמרה "אני בן 18, אני בפלנדריה, וזו לא העבודה שלי". היא
יצאה, ולא בגלל הגיל.

**"this is not my day job" הוא מה שהיה צריך לצאת.** הוא אומר "פרויקט צד" לקורא שאולי
יהיה הלקוח של פרק 04, הוא לא קונה שום אמון, והוא עולה באמינות. ושתי השורות ביחד
נקראו כהסתייגות — התנצלות שמקדימה כל הוכחה שמשהו עובד.

במקומן נכנס הדבר שכן מבדל: **כל הגדרה כאן הורצה לפני שפורסמה, ואם משהו עובד רק
חצי — הפרק אומר איזה חצי.** במייל ראשון מה שקונה אמון הוא מה שאתה עושה, לא מי אתה.

**הגיל נשאר, אבל בעמוד About.** מי שנכנס לשם כבר חיפש מי עומד מאחורי זה, ושם זה בא
**אחרי** ההוכחה ולא לפניה. זה גם סוגר את ההתנגדות מראש: אם לקוח יגלה את זה לבד, "הוא
הסתיר" גרוע פי כמה מ"הוא כתב את זה".

**זו שיפוט ולא מדידה.** ‏86 עוקבים ואפס נרשמים אינם מדגם. כשיהיו כמה מאות נרשמים
אפשר לבדוק את זה באמת.

## מה שהטקסט הזה מבטיח ואין לו מנגנון

השורה `One email a week` היא **הבטחה בכתב, ושום דבר לא שולח אותה.** מייל הברוכים־הבאים
קיים; **המייל השבועי לא נבנה בכלל** — אין תבנית, אין שליחה, ואין חיבור בין "פרק עלה"
ל"מייל יצא". זה קו ההכנסה של כל המודל הזה, וזה הפער הפתוח.

## שני מתגים שקובעים אם משהו נשלח

**`Welcome email`** — דלוק. בלעדיו מייל שנשמר לא יוצא.

**`Double opt in email`** — כשהוא דלוק, נרשם חדש מקבל **מייל אישור** ולא את
הברוכים־הבאים, וצריך ללחוץ קישור לפני שהוא נכנס לרשימה. זה שובר את "מיד" שביקש.
אם הוא נשאר דלוק, `Opt in redirect URL` חייב להצביע ל-`/e/1`, אחרת מי שמאשר נזרק
לדף הבית של beehiiv.

