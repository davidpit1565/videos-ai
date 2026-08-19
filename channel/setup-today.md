# מה לעשות עכשיו — לפי הסדר, בלחיצות

לפני הכל, ההבדל שבלבל אותך — **יש שני חיבורים שונים לאינסטגרם, ואין ביניהם קשר:**

| | בשביל מה | מה צריך | כמה זמן |
|---|---|---|---|
| **ManyChat** | הודעות אוטומטיות: מישהו כותב `prompt` בתגובות ומקבל DM | רק להתחבר עם החשבון. **אין טוקן, אין קוד** | 15 דקות |
| **טוקן Graph API** | שה-CRM יקרא לבד צפיות, שמירות ועוקבים | אפליקציית מטא + טוקן, לפי `publish/SETUP.md` | 20 דקות |

אפשר לעשות רק את הראשון ולדחות את השני. ההודעות יעבדו, והמספרים יוזנו ביד בינתיים.

---

## 1 · אינסטגרם — שני מתגים שחייבים (5 דקות)

1. אינסטגרם → תפריט → **Settings and privacy** → **Account type and tools** →
   **Switch to professional account** → Creator. (אם זה כבר מקצועי, דלג.)
2. **זה השלב שאנשים מפספסים:** Settings and privacy → **Messages and story replies**
   → **Connected tools** → **Allow access to messages** → הדלק.
   בלי המתג הזה ManyChat מתחבר ולא מצליח לשלוח כלום, ואין שום הודעת שגיאה שמסבירה למה.

## 2 · ManyChat (15 דקות)

1. **https://manychat.com** → Get Started → הירשם.
2. **Connect Instagram** ותן את ההרשאות. אם הוא מבקש דף פייסבוק — צור דף ריק
   (facebook.com/pages/create), שם כלשהו, אף אחד לא רואה אותו. זו דרישה טכנית.
3. Automation → **+ New Automation** → Trigger: **Instagram Comments**.
4. בחר את הפוסט של פרק 01 → Keywords: `prompt`, `Prompt`, `PROMPT`, `link`.
5. Action → **Send Instagram Message**, והדבק את הטקסט של שלב 1 מתוך
   `channel/instagram-automation.md`. הוסף כפתור בשם `I followed →`.
6. הכפתור → Action → **Send Instagram Message** עם הטקסט של שלב 2 והקישור.
7. למעלה מימין → **Publish**. זה הכל, ומכאן זה עובד לבד על כל תגובה.

> חינם עד 1,000 אנשים. כשנעבור את זה נדבר על מה שאחרי.

## 3 · Beehiiv — הטופס והקישור (5 דקות)

1. **https://app.beehiiv.com** → בתפריט הצד **Grow** → **Subscribe Forms**.
2. Create Form (או Default Form) → בהגדרות הטופס:
   - **Redirect after subscribe** → הדבק:
     `https://<כתובת-הסטודיו>/p/universal-ai-engine`
   - זה מה שגורם לזה שברגע שמישהו נרשם, ה-prompt נפתח לו מעצמו.
3. **Embed** → העתק את כתובת ה-iframe (משהו כמו `https://embeds.beehiiv.com/...`).
4. Vercel → הפרויקט → Settings → Environment Variables → הוסף:
   `NEXT_PUBLIC_BEEHIIV_FORM` = הכתובת שהעתקת.
5. **API key** לספירת הנרשמים: Settings → **API** → Create New API Key → העתק →
   ב-Vercel כ-`BEEHIIV_API_KEY`.

## 4 · Vercel — המשתנים שחסרים (5 דקות)

Vercel → actually-works-studio → Settings → **Environment Variables**. Supabase כבר שם
ועובד — בדקתי. מה שחסר:

| שם | בשביל מה | איפה משיגים |
|---|---|---|
| `STUDIO_PIN` | קוד כניסה ל-CRM. **כרגע כל מי שיש לו את הקישור רואה הכל** | תבחר מספר |
| `ANTHROPIC_API_KEY` | הסוכן בתוך המערכת | console.anthropic.com → API Keys |
| `BEEHIIV_API_KEY` | מספר הנרשמים | שלב 3 למעלה |
| `NEXT_PUBLIC_BEEHIIV_FORM` | טופס ההרשמה בדף | שלב 3 למעלה |
| `IG_ACCESS_TOKEN` + `IG_USER_ID` | צפיות ושמירות לכל פרק | `publish/SETUP.md` — אפשר לדחות |

אחרי הוספה: Deployments → הפריסה העליונה → **Redeploy**. משתנה סביבה נכנס לתוקף רק
בפריסה חדשה.

## 5 · ואז — לפרסם את פרק 01

זה הצעד היחיד שמייצר נתונים. אחרי שהוא באוויר:

1. בעמוד הפרקים → **משיכת מספרים מאינסטגרם** → לקשר את הפוסט לפרק 01.
2. מכאן המערכת מודדת לבד, וב-9:10 בבוקר כל יום היא רושמת מה שזז.

---

## מה אני צריך ממך

1. **איזו גרסת קול** — מתוך חמש הגרסאות בקובץ הבדיקה. זה חוסם כל סרטון הבא.
2. **כתובת ה-embed של Beehiiv** (שלב 3.3) — אחרי זה הדף אוסף מיילים באמת.
3. **להגיד לי כשהמפתחות ב-Vercel** — אני בודק מהצד שלי שכל חיבור עלה, ומריץ משיכה ראשונה.
