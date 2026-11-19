import React, { useEffect, useState } from "react";
import Head from "@docusaurus/Head";
import Layout from "@theme/Layout";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";

/**
 * Permalink used by the Tangerine software, never to be renamed:
 *
 *     <site>/go?action=release_note&v=1.8.5
 *
 * The software only knows this URL. Where the documentation really lives is
 * decided HERE, so pages can move or the site can migrate without breaking
 * links shipped in old releases.
 *
 * Parameters (once shipped, never remove one or change its meaning; if an old
 * format must change, keep handling it as well, an extra `if` is enough):
 *   action  what to do, see resolve() below. No / unknown action: no redirect.
 *   v       software version "1.8.5" (optional, used by many actions)
 *   lang    "en" | "fr" (optional, default: browser language)
 *
 * Add an action in 2 steps:
 *   1. write a method in GoLink: it reads ITS parameters and returns the URL
 *   2. add a `case` for it in resolve()
 *
 * Client-side redirect: GitHub Pages is static, no server-side redirect.
 * The page is not in any sidebar/navbar, and excluded from the sitemap.
 */

/**
 * Everything about ONE permalink: reads its parameters, knows the layout of
 * the documentation, and turns them into the real URL. No React, no window:
 * everything it needs is given to the constructor.
 */
class GoLink {
  constructor({ search, root, locale, defaultLocale, browserLanguage, translatedPages }) {
    this.params = new URLSearchParams(search);
    this.root = root; // site root without locale, e.g. "/tangerine-docs/"
    this.translatedPages = translatedPages;
    // /fr/go explicitly asks for French; plain /go has no preference.
    this.fallbackLang = locale !== defaultLocale ? locale : browserLanguage;
  }

  // --- Shared parameters ---------------------------------------------------

  get action() {
    return this.params.get("action");
  }

  /** Version given in ?v=: only "X.Y.Z" (e.g. "1.8.5") is valid, anything else counts as no version (null). */
  get version() {
    const v = this.params.get("v") ?? "";
    return /^\d+\.\d+\.\d+$/.test(v) ? v : null;
  }

  get lang() {
    return (this.params.get("lang") ?? this.fallbackLang ?? "").slice(0, 2);
  }

  // --- Helper shared by all actions -----------------------------------------

  /** URL of a doc page ("/usage/release_notes"), in French if asked AND translated. */
  pageUrl(page, anchor = "") {
    const french = this.lang === "fr" && this.translatedPages.includes(page);
    return `${this.root}${french ? "fr/" : ""}${page.slice(1)}${anchor}`;
  }

  // --- Actions: one method each, returns a URL ---------------------------

  /** Release notes, on the section of the version if there is one. */
  releaseNote() {
    const version = this.version;
    const anchor = version ? `#v${version.replace(/\./g, "-")}` : "";
    return this.pageUrl("/usage/release_notes", anchor);
  }

  // --- Entry point ---------------------------------------------------------

  /** URL to redirect to, or null (no / unknown action: do nothing). */
  resolve() {
    switch (this.action) {
      case "release_note":
        return this.releaseNote();
      default:
        return null;
    }
  }
}

export default function Go() {
  const { siteConfig, i18n } = useDocusaurusContext();
  const [nothingToDo, setNothingToDo] = useState(false);

  // On a non-default locale, baseUrl is "/tangerine-docs/fr/": strip the
  // locale to get the site root.
  const { currentLocale, defaultLocale } = i18n;
  const root =
    currentLocale !== defaultLocale
      ? siteConfig.baseUrl.replace(new RegExp(`${currentLocale}/$`), "")
      : siteConfig.baseUrl;

  // The parameters only exist in the visitor's browser (the page is built
  // statically beforehand): so the redirect must run client-side, after load.
  useEffect(() => {
    const url = new GoLink({
      search: window.location.search,
      root,
      locale: currentLocale,
      defaultLocale,
      browserLanguage: navigator.language,
      translatedPages: siteConfig.customFields.translatedPages,
    }).resolve();

    if (url) {
      window.location.replace(url);
    } else {
      setNothingToDo(true);
    }
  }, []);

  return (
    <Layout title="Redirecting…" noFooter>
      <Head>
        <meta name="robots" content="noindex, nofollow" />
      </Head>
      <main className="container margin-vert--xl">
        {nothingToDo ? (
          <p>
            Nothing to redirect. <a href={root}>Go to the documentation</a>.
          </p>
        ) : (
          <p>Redirecting to the documentation…</p>
        )}
      </main>
    </Layout>
  );
}
