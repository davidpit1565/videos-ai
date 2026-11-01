import { redirect } from "next/navigation";

/** The email list was removed from the site (1.11.2026, David). Old links to /join still land somewhere. */
export default function Join() {
  redirect("/");
}
