/** The Hebrew faces (and the mono used for the studio's numbers) are only needed by the
 *  private studio and its PIN page, so they load there and nowhere else: the public site
 *  is English and used to download five font families it never drew. React hoists a
 *  stylesheet <link> with `precedence` into <head> wherever it is rendered. */
export default function StudioFonts() {
  return (
    <>
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      <link
        rel="stylesheet"
        precedence="default"
        href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600;700&display=swap"
      />
    </>
  );
}
