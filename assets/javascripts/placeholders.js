(() => {
  function highlightPlaceholders(root = document) {
    root.querySelectorAll("code").forEach((code) => {
      if (code.dataset.placeholdersHighlighted === "true") {
        return;
      }

      const walker = document.createTreeWalker(code, NodeFilter.SHOW_TEXT);
      const textNodes = [];

      while (walker.nextNode()) {
        textNodes.push(walker.currentNode);
      }

      textNodes.forEach((node) => {
        if (node.parentElement?.closest(".tutorial-placeholder")) {
          return;
        }

        const text = node.nodeValue ?? "";
        const matches = [...text.matchAll(/<[A-Z][A-Z0-9_-]*>/g)];

        if (matches.length === 0) {
          return;
        }

        const fragment = document.createDocumentFragment();
        let offset = 0;

        matches.forEach((match) => {
          fragment.append(text.slice(offset, match.index));

          const placeholder = document.createElement("span");
          placeholder.className = "tutorial-placeholder";
          placeholder.title = "Replace this placeholder";
          placeholder.textContent = match[0];
          fragment.append(placeholder);

          offset = match.index + match[0].length;
        });

        fragment.append(text.slice(offset));
        node.replaceWith(fragment);
      });

      code.dataset.placeholdersHighlighted = "true";
    });
  }

  const start = () => highlightPlaceholders(document);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(() => highlightPlaceholders(document));
  }
})();
