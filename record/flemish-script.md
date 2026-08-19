# הקלטה בפלמית — 45 שניות, פעם אחת

## למה בכלל

מודל שכפול הקול תומך בהולנדית, אבל הוא אומן בעיקר על **הולנדית של הולנדה**. ההגייה שלו
תישמע כמו מישהו מאמסטרדם, לא כמו מישהו מאנטוורפן. את ההבדל הזה קהל בלגי שומע מיד, וזה
בדיוק ההבדל שאתה רוצה לנצל.

הקול שלך *כבר* יכול לדבר הולנדית — שלחתי לך דוגמה. מה שהוא לא יכול לעשות לבד זה **מבטא
פלמי**. את זה מקבלים מהקלטה אחת שלך בפלמית, שממנה נבנה פרופיל קול שני.

התוצאה: שני פרופילים שמורים — אנגלית ופלמית — ומכאן כל טקסט בכל אחת מהשפות יוצא בקול שלך
עם המבטא הנכון, בלי עוד הקלטות.

## איך להקליט

- **אותו מיקרופון ואותו מרחק כמו ההקלטה הראשונה** (זו שהתברר שהיא הטובה). בערך רוחב יד.
- חדר סגור, בלי מזגן ובלי מכונת כלים ברקע.
- דיבור **רגיל**, כמו שאתה מסביר משהו לחבר. לא קול של קריין, לא לדבר לאט במיוחד.
- לעצור שנייה בין פסקה לפסקה. אם טעית — תחזור על המשפט, אני חותך את הטוב.
- קובץ אחד, ברצף, בלי עריכה.

## מה להקריא

> תקן כל מילה שאתה לא היית אומר ככה. אתה דובר השפה — הנוסח שלך עדיף על שלי, וגם ככה
> הפרופיל ילמד את הרגיסטר שלך ולא רגיסטר של ספר.

---

Iedereen praat over AI-agenten, maar bijna niemand kan uitleggen waar de chatbot stopt.

Een chatbot antwoordt. Dat is heel de job.

Een agent doet iets. Hij plant zelf de stappen, gebruikt echte programma's, controleert
het resultaat, en begint opnieuw.

De test is simpel. Als het niks kan doen zonder jou, is het gewoon een chatbot met een
schonere naam.

En het eerlijke stuk, dat niemand erbij zegt: agenten mislukken vol zelfvertrouwen. Ze
sturen een mail naar de verkeerde persoon, heel vriendelijk. Ze stoppen halfweg en zeggen
dat het gelukt is.

Daarom laat je je eerste agent iets doen dat je kan terugdraaien.

Volgende keer bouwen we er samen een, van nul, zonder code.

---

## אחרי ההקלטה

תשלח לי את הקובץ. אני עושה איתו בדיוק מה שעשיתי עם האנגלית:

1. מודד רעש ומחליט מה לנקות ומה לא לגעת בו.
2. בוחר את עשר השניות שהמודל מותנה עליהן לפי ציון דמיון, לא לפי אוזן.
3. מריץ בדיקה על כל צליל — `python3 audio/phoneme_audit.py --lang nl` — ומתקן במה שנשמע
   שגוי דרך טבלת ההגייה.
4. שולח לך שלוש גרסאות לבחירה, ואת מה שתבחר אני נועל.
