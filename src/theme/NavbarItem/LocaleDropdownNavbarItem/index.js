import React from "react";
import OriginalLocaleDropdown from "@theme-original/NavbarItem/LocaleDropdownNavbarItem";
import { useLocation } from "@docusaurus/router";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";

/**
 * Wrapper around the locale dropdown: the language switcher is only shown
 * where it makes sense, to avoid confusion while most pages are English-only.
 *
 * Visible only when the current page has a translation (see
 * `customFields.translatedPages` in docusaurus.config.js).
 *
 * On an untranslated page, the French and English versions are identical
 * (the docs plugin falls back to the English source), so a visitor under /fr/
 * loses nothing by not seeing the switcher: it reappears on translated pages.
 */
export default function LocaleDropdownNavbarItem(props) {
  const { siteConfig } = useDocusaurusContext();
  const { pathname } = useLocation();

  // `baseUrl` already contains the locale prefix on non-default locales
  // (e.g. /tangerine-docs/fr/), so this gives the page path without it.
  const baseUrl = siteConfig.baseUrl;
  const relative = pathname.startsWith(baseUrl)
    ? "/" + pathname.slice(baseUrl.length)
    : pathname;
  const page = relative.replace(/\/+$/, "") || "/";

  const translatedPages = siteConfig.customFields?.translatedPages ?? [];
  const isTranslated = translatedPages.includes(page);

  if (!isTranslated) {
    return null;
  }
  return <OriginalLocaleDropdown {...props} />;
}
