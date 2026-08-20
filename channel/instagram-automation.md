# האוטומציה של האינסטגרם — מה אפשר, מה לא, ומה להקים

> **הקובץ הזה נטוש.** הוא נכתב לתוכנית ManyChat בתשלום, שירדה מהפרק: הפרומפט נכנס
> ל-caption מתחת לסרטון, ואין מילת מתיחה. הוא נשאר כאן רק בשביל תיעוד ההרשאות של
> Meta. אל תבנה עליו — כל שורה כאן שמבטיחה DM אוטומטי לא מחוברת לשום דבר.


מה שביקשת: מישהו כותב בתגובות `prompt`, מקבל הודעה, מתבקש לעקוב, מאשר שעקב, ומקבל
קישור לעמוד עם ה-prompt — וכדי לראות אותו הוא נרשם למייל. זה בדיוק הדבר הנכון לבנות,
והוא אפשרי כמעט במלואו. שלושה דברים צריך לדעת לפני שמקימים:

## מה שאי אפשר, ואין לזה דרך עקיפה

**אין שום ממשק — לא של אינסטגרם ולא של אף כלי — שיודע להגיד אם משתמש מסוים עוקב
אחריך.** לא ManyChat, לא אנחנו, אף אחד. לכן ה"עקוב אחריי" חייב להיות **על אמון**:
שולחים הודעה, מבקשים לעקוב, והוא לוחץ על כפתור "עקבתי". זה בדיוק מה שתיארת — האינטואיציה
שלך נכונה, וזה גם מה שכל החשבונות הגדולים עושים.

עוד מגבלה: הודעה פרטית בתגובה לתגובה (Private Reply) מותרת **פעם אחת לכל תגובה, בתוך
7 ימים**. אחרי זה צריך שהוא יכתוב לך, אחרת אין ערוץ.

## שלוש דרכים, מהמומלצת לפחות

### א. ManyChat — מומלץ, וזה מה שהייתי מקים היום
חינם עד 1,000 אנשים, מוקם ב-15 דקות, ואין מה לתחזק.

1. manychat.com → Sign up → Connect Instagram (צריך חשבון Professional).
2. Automation → New → Trigger: **Instagram Comment** → על הפוסט של פרק 01 →
   Keyword: `prompt` (וגם `PROMPT`, `Prompt`, `link`).
3. Action → **Send Instagram Message** עם הטקסט של שלב 1 למטה + כפתור "I followed".
4. הכפתור → Action → **Send Instagram Message** עם הטקסט של שלב 2 והקישור.
5. Publish. זה הכל.

**למה זה ולא אנחנו:** בשביל שאותו דבר יעבוד מהמערכת שלנו צריך אפליקציית Meta עם
הרשאות `instagram_manage_messages` ו-`instagram_manage_comments`, ואלה עוברות ביקורת
של Meta (App Review) — שבועות, ולפעמים סירוב. ManyChat כבר עברה את הביקורת הזאת.
זה ההבדל היחיד; מבחינת מה שהצופה רואה, אין הבדל.

### ב. אינסטגרם עצמו — הכי פשוט, פחות חכם
Professional Dashboard → Automated replies / Keywords. שולח הודעה קבועה על מילת
מפתח. אין כפתורים, אין תנאים, אין "עקבתי". אם רוצים להתחיל הערב בלי הרשמה לשום כלי —
זה עובד, ומאבד את שלב המעקב.

### ג. לבנות אצלנו — יש לזה מקום, אבל לא עכשיו
המערכת כבר פרוסה ב-Vercel ויכולה לקבל Webhook. מה שחסר זו אפליקציית Meta מאושרת.
שווה לחזור לזה כשיש 5,000+ עוקבים ומגבלת ה-1,000 של ManyChat מתחילה להכביד — ואז
המעבר הוא של יום עבודה, לא של פרויקט.

## הטקסטים — באנגלית, כי הקהל אנגלי

**שלב 1 — ההודעה הראשונה (אחרי התגובה):**
> Sent. One thing first — this list is small and I keep it that way, so it goes to
> people who actually follow the channel.
>
> If you're following, tap the button and the link is yours.
> If not, follow @actuallyworks.ai and then tap it.

כפתור: `I followed →`

**שלב 2 — הקישור:**
> Here it is: the Universal AI Engine, the exact screen, and the part that breaks.
>
> https://<הכתובת>/join?p=universal-ai-engine
>
> Drop your email on that page and it opens straight away. One email a week after
> that — one setup, tested before it's sent.

**תגובה פומבית מתחת לפוסט** — *ירד מהפרק.* היה כאן
`Comment "prompt" and I'll DM you the full text.` — מילת מתיחה שדורשת ManyChat
בתשלום. הפרומפט המלא יושב ב-caption, גלוי, בלי שאף אחד צריך לכתוב כלום.

**מי שכותב תגובה אחרת** (שאלה, ביקורת, מחמאה) — לא אוטומציה. עונים ביד, מהטמפלטים
ב-`brand/messages.md`.

## איך זה מתחבר למערכת שלנו

```
תגובה "prompt" → ManyChat → DM → כפתור "עקבתי" → DM עם קישור
   → /join?p=universal-ai-engine   (מזהה מה הוא בא לקבל, ומציג טופס Beehiiv)
   → Beehiiv רושם אותו ומפנה ל-/p/universal-ai-engine
   → העמוד עם ה-prompt המלא, כפתור העתקה, ומה שלא עובד
```

**מה שצריך להגדיר פעם אחת ב-Beehiiv:** Grow → Subscribe Forms → Embed, ובתוך הטופס
`Redirect after subscribe` → הכתובת של `/p/universal-ai-engine`. את כתובת ה-embed
מדביקים ב-Vercel כמשתנה `NEXT_PUBLIC_BEEHIIV_FORM`.

הערה לעתיד: כשיהיו כמה prompts, כל אחד צריך טופס Beehiiv נפרד (כי ההפניה מוגדרת
בטופס). זה שלוש דקות לכל prompt חדש.

## מה נמדד מזה

בכל פרק, המערכת כבר מציגה צפיות, שמירות ותגובות. מה שהאוטומציה מוסיפה זה **נרשמים
לפרק** — את זה מזינים ידנית לפי מה ש-Beehiiv מראה ביום הפרסום, כי אין API שמייחס
נרשם לסרטון מסוים. שתי שורות בטבלה, פעם בשבוע.
