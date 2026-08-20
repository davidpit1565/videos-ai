# הקלטה אחת, שני דברים — ה־T/K/P באנגלית וה־G בפלמית

**למה זה נחוץ:** המדידה של העיצורים בנויה אבל לא מכוילת. בהקלטות הייחוס הקיימות
שלך יש **4 עד 7** עיצורים מהסוג הזה בסך הכל — אין ממה למדוד. פה יהיו 50–60.

**כמה זמן:** ההקלטה עצמה פחות מ־3 דקות. אין צורך לעשות הכל בטייק אחד.

---

## איך להקליט (זהה למה שעשית קודם)

1. חדר שקט, טלפון או מיקרופון במרחק כף יד מהפה, לא צמוד.
2. הקלט **קובץ אחד** לכל חלק (4 קבצים בסך הכל). אם התבלבלת במילה — עצור, קח נשימה,
   וקרא את השורה מחדש. חזרות לא מפריעות, אני חותך.
3. **קרא בקול שאתה מדבר בו בסרטונים**, לא בקול "הקלטה". זה הקול שאני מודד.

⚠️ בחלק א' ובחלק ג' — **עצירה של שנייה שלמה בין מילה למילה.** זה לא סטייל, זו הדרישה
המדידתית: העיצור הזה מוגדר על ידי השקט שלפניו, ובלי השקט אין מה למדוד.

---

## חלק א — מילים בודדות, אנגלית (עצירה בין כל מילה)

```
tea      —      key      —      pea
top      —      cop      —      pop
time     —      kind     —      pipe
take     —      cake     —      pace
two      —      cool     —      pool
turn     —      call     —      part
type     —      count    —      point
told     —      cost     —      paste
```

עכשיו אותו דבר עם העיצורים ה"רכים" — להשוואה:

```
day      —      go       —      bay
door     —      good     —      box
done     —      gone     —      both
```

## חלק ב — משפטים, אנגלית (קרא רגיל, בלי עצירות)

```
Two clicks, paste the prompt, and press Save.
Take the top card, count the tokens, keep the point.
Ten people told me the same thing: the tool is too complicated.
Copy this, paste it, turn it on. That is the whole trick.
Pick a task, describe it in plain terms, and check what it decided.
The price of a bad prompt is a perfect answer to the wrong question.
```

## חלק ג — מילים בודדות, פלמית (עצירה בין כל מילה)

**זה בשביל ה־G.** אני צריך למדוד את ה־G **שלך** — הפלמית הרכה — כדי לדעת בכמה
המודל סוחב אותה לכיוון ההולנדית הקשה. בלי זה אני מנחש.

```
goed     —      gaan     —      geven
graag    —      genoeg   —      gewoon
dagen    —      morgen   —      vragen
agent    —      groot    —      gebruiken
```

ואת אותם צלילים ב-`ch`:

```
acht     —      licht    —      nacht     —      echt
```

## חלק ד — משפטים, פלמית (קרא רגיל)

```
Goeiedag, ik ga graag uitleggen hoe dat gewoon werkt.
Genoeg gepraat over agenten — ik toon je de echte grens.
Elke morgen gebruik ik het, en het geeft altijd een goed antwoord.
```

---

## מה אני עושה עם זה

- **חלק א' + ב'** מכיילים את מדידת ה־T/K/P: הזמן בין הפיצוץ לתנועה. אחרי זה
  `audio/plosives.py` תעבור את הבדיקה של עצמה — או שאדע שהיא לא, ואגיד לך.
- **חלק ג' + ד'** נותנים לי את ה־G הפלמי שלך כמטרה נמדדת, ולא כתחושה.
- החלקים הבודדים (א', ג') הם הכיול; המשפטים (ב', ד') הם המציאות. צריך את שניהם:
  בכיול לבד אין דיבור רצוף, ובדיבור רצוף לבד אי אפשר לבודד את העיצור.
