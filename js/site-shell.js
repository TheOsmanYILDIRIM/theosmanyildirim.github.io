const slots = [...document.querySelectorAll("[data-site-shell]")];

async function loadShell(slot) {
  const kind = slot.dataset.siteShell;
  const path = kind === "header" ? "/components/inner-header.html" : "/components/inner-footer.html";
  const response = await fetch(path, { cache: "no-cache" });
  if (!response.ok) throw new Error(`Site shell yüklenemedi: ${path} (${response.status})`);
  slot.outerHTML = await response.text();
}

try {
  await Promise.all(slots.map(loadShell));
  document.documentElement.dataset.siteShellReady = "true";
} catch (error) {
  console.error(error);
  document.documentElement.dataset.siteShellError = "true";
}
