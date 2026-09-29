(() => {
  "use strict";

  const ADS_ID = "AW-789474599";
  const CONVERSION_BY_PHONE = Object.freeze({
    "905518652667": "AW-789474599/7yumCPfDtYodEKfaufgC",
    "905462436828": "AW-789474599/KzsWCI3ur4odEKfaufgC"
  });
  const WHATSAPP_HOSTS = new Set([
    "wa.me",
    "api.whatsapp.com",
    "web.whatsapp.com"
  ]);

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag() {
    window.dataLayer.push(arguments);
  };

  window.gtag("js", new Date());
  window.gtag("config", ADS_ID);

  if (!document.querySelector(`script[src*="googletagmanager.com/gtag/js?id=${ADS_ID}"]`)) {
    const tag = document.createElement("script");
    tag.async = true;
    tag.src = `https://www.googletagmanager.com/gtag/js?id=${ADS_ID}`;
    document.head.appendChild(tag);
  }

  function whatsappPhone(href) {
    let url;

    try {
      url = new URL(href, document.baseURI);
    } catch {
      return null;
    }

    const host = url.hostname.toLowerCase().replace(/^www\./, "");
    if (!WHATSAPP_HOSTS.has(host)) return null;

    const rawPhone = host === "wa.me"
      ? url.pathname.split("/").filter(Boolean)[0]
      : url.searchParams.get("phone");

    return rawPhone ? rawPhone.replace(/\D/g, "") : null;
  }

  document.addEventListener("click", (event) => {
    const anchor = event.target.closest?.("a[href]");
    if (!anchor) return;

    const sendTo = CONVERSION_BY_PHONE[whatsappPhone(anchor.href)];
    if (!sendTo) return;

    window.gtag("event", "conversion", { send_to: sendTo });
  });
})();
