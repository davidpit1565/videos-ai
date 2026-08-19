import { State, uid } from "./types";

/** The pipeline as it stands, so the app is useful on first open rather than empty. */
export function seed(): State {
  const ep = (
    number: number, title: string, format: "reel" | "long" | "both",
    status: State["episodes"][0]["status"], topic: string, notes: string,
  ) => ({
    id: uid(), number, title, format, status, topic,
    tested: false, publishedAt: null, igMediaId: null, ytVideoId: null, notes,
    views: null, likes: null, saves: null, comments: null, shares: null, subsAttributed: null,
  });
  return {
    version: 1,
    episodes: [
      ep(1, "Paste this once — the Universal AI Engine", "both", "testing",
         "ChatGPT · Custom Instructions", "בנוי ומוכן · ביקוש נמוך במדידה — מפרסמים בשביל הנרשמים"),
      ep(2, "What an AI agent actually is", "both", "voice",
         "Agents · יסודות", "ביקוש: חציון 125 אלף · הריל בנוי, הקריינות בתור"),
      ep(3, "Your first n8n agent: email → summary → Telegram", "long", "idea",
         "n8n", "ביקוש: חציון 233 אלף — הגבוה במדידה · הפרק הארוך והמלא"),
      ep(4, "The AI setup I'd sell to a business", "both", "idea",
         "Agents · לעסקים", "המילה sell הופיעה פי 5 ברביע העליון · הפרק שמביא פניות"),
      ep(5, "I gave an agent my inbox for a week", "both", "idea",
         "Lindy / ChatGPT Agent", "פורמט תוצאות · עובד כשיש קהל שסומך"),
      ep(6, "The 5 things agents still can't do", "both", "idea",
         "Agents · מגבלות", "פרק חתימה · מבדל ממי שמבטיח הכל"),
    ],
    snapshots: [{
      id: uid(), date: new Date().toISOString().slice(0, 10),
      subscribers: 0, igFollowers: 86, ytSubs: 0, note: "נקודת ההתחלה",
    }],
    revenue: [
      { id: uid(), name: "שירות — בניית מערכות AI לעסקים", status: "idea", mrrEur: 0,
        needsAudience: "לא", nextStep: "שורה בביו + קישור ליומן" },
      { id: uid(), name: "ניוזלטר — ספונסרים", status: "idea", mrrEur: 0,
        needsAudience: "~5,000 נרשמים", nextStep: "לפרסם את הפרק הראשון" },
      { id: uid(), name: "אפיליאייט — כלי AI", status: "idea", mrrEur: 0,
        needsAudience: "קטן", nextStep: "להירשם ל-n8n ו-Make" },
      { id: uid(), name: "מוצר דיגיטלי — חבילת workflows", status: "idea", mrrEur: 0,
        needsAudience: "~3,000", nextStep: "לבנות מהסרטונים הנשמרים ביותר" },
    ],
    tasks: [
      { id: uid(), text: "להסב את חשבון האינסטגרם ל-Creator ולשנות את השם", note: "~15 דקות · חוסם הכל", done: false },
      { id: uid(), text: "לאשר את פרק 01 ולפרסם", note: "הצעד היחיד שבאמת קובע", done: false },
      { id: uid(), text: "להזמין מיקרופון USB", note: "~300 ₪ · משדרג כל פרק עתידי", done: false },
      { id: uid(), text: "לבדוק בעצמי את הסטאפ של פרק 02", note: "~1 שעה · זה המוצר", done: false },
      { id: uid(), text: "לענות על כל תגובה והודעה", note: "יומי · משם מגיעים הלקוחות", done: false },
    ],
    ideas: [
      { id: uid(), text: "Claude Code למי שלא מתכנת — חציון 159 אלף במדידה" },
      { id: uid(), text: "לבנות ולמכור אוטומציה לעסק מקומי — צעד אחר צעד" },
      { id: uid(), text: "Zapier מול Make מול n8n — לבחור אחד בשלוש דקות" },
      { id: uid(), text: "סוכן מחקר בלי קוד — Perplexity + n8n" },
      { id: uid(), text: "אוטומטתי שבוע עם 4 סוכנים — מה שרד" },
    ],
    updatedAt: new Date().toISOString(),
  };
}
