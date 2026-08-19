export type Channel = "ig" | "tiktok" | "yt" | "ytlong";
export const CHANNELS: Channel[] = ["ig", "tiktok", "yt", "ytlong"];
export const CHANNEL_HE: Record<Channel, string> = {
  ig: "אינסטגרם", tiktok: "טיקטוק", yt: "Shorts", ytlong: "יוטיוב ארוך",
};

export type Status = "idea" | "script" | "voice" | "render" | "testing" | "live";
export type Format = "reel" | "long" | "both";

export const STATUS_ORDER: Status[] = ["idea", "script", "voice", "render", "testing", "live"];
export const STATUS_HE: Record<Status, string> = {
  idea: "רעיון", script: "תסריט", voice: "קריינות",
  render: "רנדר", testing: "בדיקה", live: "פורסם",
};

export type Episode = {
  id: string;
  number: number;
  title: string;
  format: Format;
  status: Status;
  topic: string;
  tested: boolean;
  publishedAt: string | null;
  /** Instagram media id — how metrics get attached to this episode */
  igMediaId: string | null;
  ytVideoId: string | null;
  notes: string;
  /** pulled from Instagram; null until the episode is live and a token exists */
  views: number | null;
  likes: number | null;
  saves: number | null;
  comments: number | null;
  shares: number | null;
  /** how many subscribers this episode brought — entered by hand, since no API attributes it */
  subsAttributed: number | null;
  /** planned publish date, YYYY-MM-DD. The week view is built from this. */
  publishOn?: string | null;
  /** where it goes out. One build, several platforms, no extra work. */
  channels?: Channel[];
};

export type Snapshot = {
  id: string;
  date: string;
  subscribers: number | null;
  igFollowers: number | null;
  ytSubs: number | null;
  note: string;
};

export type RevenueLine = {
  id: string;
  name: string;
  status: Status;
  mrrEur: number;
  needsAudience: string;
  nextStep: string;
};

/** Something that changed, recorded automatically so he never has to notice it himself. */
export type ActivityEvent = {
  id: string;
  at: string;
  source: "instagram" | "beehiiv" | "youtube" | "studio";
  label: string;
  value: number | null;
  delta: number | null;
};

export type Task = { id: string; text: string; note: string; done: boolean };
export type Idea = { id: string; text: string };

export type State = {
  version: 1;
  episodes: Episode[];
  snapshots: Snapshot[];
  revenue: RevenueLine[];
  tasks: Task[];
  ideas: Idea[];
  /** optional so states saved before the feed existed still load */
  activity?: ActivityEvent[];
  updatedAt: string;
};

export const uid = () =>
  (globalThis.crypto?.randomUUID?.() ?? String(Date.now() + Math.random())).slice(0, 12);

/** Engagement rate is the number that actually predicts reach. */
export function engagement(e: Episode): number | null {
  if (!e.views) return null;
  const acts = (e.likes ?? 0) + (e.saves ?? 0) + (e.comments ?? 0) + (e.shares ?? 0);
  return acts / e.views;
}

/** Saves-per-view is the signal for a "paste this" video: did anyone keep it? */
export function saveRate(e: Episode): number | null {
  if (!e.views || e.saves == null) return null;
  return e.saves / e.views;
}

/** Sunday to Friday. Saturday is off — his rule, and the schedule respects it. */
export function weekDays(from: Date): string[] {
  const d = new Date(from);
  d.setDate(d.getDate() - ((d.getDay() + 7) % 7));   // back to Sunday
  const out: string[] = [];
  for (let i = 0; i < 6; i++) {
    const x = new Date(d);
    x.setDate(d.getDate() + i);
    out.push(x.toISOString().slice(0, 10));
  }
  return out;
}

export const DAY_HE = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"];
