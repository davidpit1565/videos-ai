# מעבר מ-Vercel ל-Netlify (חינם) — מדריך לחיצות

נכתב 6.10.2026, אחרי ש-Vercel השהה את כל הצוות (חריגה ממכסות Hobby). **שום ערך סודי לא נכתב
כאן, ולא צריך לשלוח אותו אף פעם בצ'אט.** אתה מעתיק ערכים בעצמך ממקום למקום.

## לפני שמתחילים
- **לא נבדק בפועל:** ההגדרות כאן לא רצו מול Netlify אמיתי. הבנייה המקומית של הסטודיו עברה
  (`npm run build`), וזה כל מה שנבדק. אם משהו לא נראה כמו כאן, תעצור ותגיד.
- המכסה החינמית של Netlify, לפי מקורות חיצוניים (לא אומתו): 300 קרדיטים בחודש, והאתר
  נעצר כשהם נגמרים. כל פריסה עולה קרדיטים, ולכן לא לדחוף commit בלי סיבה.

## שלב 1 — סודות למשימות היומיות (GitHub)
1. פתח את המאגר ב-GitHub → **Settings** (הגדרות) → **Secrets and variables** → **Actions**.
2. לשונית **Secrets** → **New repository secret**. שם: `CRON_SECRET`. ערך: העתק מ-Vercel
   (Project → Settings → Environment Variables → `CRON_SECRET` → העין). **Add secret**.
3. לשונית **Variables** → **New repository variable**. שם: `SITE_URL`, ערך:
   `https://www.actually-works.com`. **Add variable**.

## שלב 2 — האתר ב-Netlify
1. היכנס ל-netlify.com → **Sign up** → **GitHub** (הרשאה לחשבון שלך).
2. **Add new site** → **Import an existing project** → **GitHub** → בחר `videos-ai`.
3. **Base directory** (תיקיית בסיס): `studio`. פקודת הבנייה (`npm run build`) כבר מגיעה מהקובץ.
4. **Add environment variables** (להוסיף משתני סביבה). את הערכים להעתיק מ-Vercel, אחד אחד:
   `POSTGRES_URL`, `STUDIO_PIN`, `CRON_SECRET`, `NEXT_PUBLIC_SITE_URL`, `ANTHROPIC_API_KEY`,
   `BEEHIIV_API_KEY`, `BEEHIIV_PUBLICATION_ID`, `IG_ACCESS_TOKEN`, `IG_USER_ID`,
   `FB_PAGE_ID`, `FB_PAGE_ACCESS_TOKEN`, `FB_BUSINESS_PAGE_ID`, `FB_BUSINESS_PAGE_ACCESS_TOKEN`,
   `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_API_KEY`, `YOUTUBE_CHANNEL_ID`,
   `YOUTUBE_HANDLE`, `D_ID_API_KEY`, `HF_API_KEY`, `HF_SECRET`, `CLAUDE_USAGE_SECRET`,
   `JARVIS_STUDIO_SECRET`, `INSTAGRAM_INSIGHTS_ENABLED`,
   `INSTAGRAM_INSIGHTS_SNAPSHOT_DEDUPE_WINDOW`, `PUBLISH_REMINDER_CHECKPOINT_HOURS`.
   (אם משתנה לא קיים ב-Vercel, מדלגים עליו. אופציונלי: אלה שאתה לא משתמש בהם.)
5. **Deploy**. ההמתנה כמה דקות. בסוף תקבל כתובת `משהו.netlify.app`.
6. פתח את הכתובת. אמור להופיע האתר, ואם נכנסים ל-`/studio` מתבקש ה-PIN.

## שלב 3 — הדומיין (הכי רגיש)
הדומיין `actually-works.com` רשום ב-Vercel ונשאר שם (אין צורך להעביר אותו). רק מצביעים אותו
לכתובת החדשה:
1. ב-Netlify: **Domain management** → **Add a domain** → `www.actually-works.com`. Netlify
   יציג לך בדיוק איזה רשומות DNS להגדיר. **תעתיק אותן כמו שהן.**
2. ב-Vercel: **Domains** → `actually-works.com` → **DNS Records** → עדכן את הרשומה של `www`
   (CNAME) לפי מה ש-Netlify הציג.
3. אם Vercel לא מאפשר לערוך בזמן ההשהיה, תעצור ותגיד לי מה כתוב. אל תנסה לעקוף.
4. אופציונלי: לקבלת HTTPS אוטומטי ב-Netlify → **HTTPS** → **Verify DNS** (לוקח כמה דקות).

## שלב 4 — בדיקה
- פתח `https://www.actually-works.com`. אמור להיות האתר.
- ב-GitHub → **Actions** → `studio-cron` → **Run workflow** עם `/api/health-check`. אמור לצאת ירוק.

## אם משהו משתבש
תחזור ל-Vercel: ברגע שהמכסות מתאפסות או שדרגת, הדומיין חוזר להצביע לשם. אין פעולה בלתי הפיכה
כאן.
