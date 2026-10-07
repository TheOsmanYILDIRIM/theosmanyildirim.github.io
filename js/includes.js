const includeNodes = [...document.querySelectorAll("[data-include]")];

async function loadInclude(node) {
  const path = node.dataset.include;
  const response = await fetch(path, { cache: "no-cache" });

  if (!response.ok) {
    throw new Error(`Include yüklenemedi: ${path} (${response.status})`);
  }

  node.outerHTML = await response.text();
}

try {
  await Promise.all(includeNodes.map(loadInclude));

  document.documentElement.dataset.portfolioReady = "true";

  if (location.hash) {
    requestAnimationFrame(() => {
      document.querySelector(location.hash)?.scrollIntoView();
    });
  }

  document.dispatchEvent(new CustomEvent("portfolio:ready"));
} catch (error) {
  console.error(error);
  document.documentElement.dataset.includeError = "true";
}
