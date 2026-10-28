/* Blog behavior: reading time, progress, table of contents, share, and hub search.
   Safe to load on both post pages and the hub; each part guards on its elements. */
(function () {
  "use strict";
  var document = window.document;

  function $(sel) {
    return document.querySelector(sel);
  }

  /* ---------- Reading time ---------- */
  function computeReadingTime() {
    var article = document.querySelector(".article-body");
    var slots = document.querySelectorAll("[data-reading-time]");
    if (!article || !slots.length) {
      return;
    }
    var words = article.textContent.trim().split(/\s+/).length;
    var minutes = Math.max(1, Math.round(words / 210));
    slots.forEach(function (slot) {
      var m = slot.querySelector("[data-reading-minutes]");
      if (m) {
        m.textContent = String(minutes);
      }
      slot.removeAttribute("hidden");
    });
  }

  /* ---------- Reading progress ---------- */
  var progressTicking = false;
  function updateProgress() {
    progressTicking = false;
    var progressBar = $(".reading-progress");
    var article = document.querySelector(".article-body");
    if (!progressBar || !article) {
      return;
    }
    var rect = article.getBoundingClientRect();
    if (rect.bottom < 0) {
      progressBar.style.setProperty("--progress", "100%");
      return;
    }
    var start = rect.top + window.scrollY;
    var visible = Math.min(
      Math.max((window.scrollY + window.innerHeight * 0.5 - start) / rect.height, 0),
      1
    );
    progressBar.style.setProperty("--progress", (visible * 100).toFixed(2) + "%");
  }
  function onScroll() {
    if (!progressTicking) {
      progressTicking = true;
      window.requestAnimationFrame(updateProgress);
    }
  }

  /* ---------- Table of contents ---------- */
  function buildToc() {
    var rail = document.querySelector(".sticky-rail");
    var tocList = document.getElementById("toc-list");
    var article = document.querySelector(".article-body");
    if (!rail || !tocList || !article) {
      return;
    }
    var headings = Array.prototype.slice.call(article.querySelectorAll("h2[id]"));
    var layout = document.querySelector(".article-layout");
    if (headings.length < 3) {
      rail.hidden = true;
      if (layout) {
        layout.classList.add("rail-hidden");
      }
      return;
    }
    rail.removeAttribute("hidden");
    var frag = document.createDocumentFragment();
    headings.forEach(function (heading) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#" + heading.id;
      a.textContent = heading.textContent;
      li.appendChild(a);
      frag.appendChild(li);
    });
    tocList.appendChild(frag);
  }

  /* ---------- Share controls ---------- */
  function copyToClipboard(text, done) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, function () {
        legacyCopy(text);
        done();
      });
    } else {
      legacyCopy(text);
      done();
    }
  }
  function legacyCopy(text) {
    var input = document.createElement("textarea");
    input.value = text;
    input.setAttribute("readonly", "");
    input.style.position = "fixed";
    input.style.opacity = "0";
    document.body.appendChild(input);
    input.select();
    try {
      document.execCommand("copy");
    } catch (error) {}
    document.body.removeChild(input);
  }
  function bindShare() {
    var buttons = document.querySelectorAll("[data-share]");
    if (!buttons.length) {
      return;
    }
    var title = document.title;
    var canonicalEl = document.querySelector('link[rel="canonical"]');
    var canonical = canonicalEl && canonicalEl.href;
    buttons.forEach(function (button) {
      var mode = button.getAttribute("data-share");
      var label = button.querySelector("[data-share-label]");
      if (label) {
        button.setAttribute("data-original-label", label.textContent);
      }
      button.addEventListener("click", function () {
        if (mode === "share" && navigator.share) {
          navigator
            .share({ title: title, url: canonical })
            .catch(function () {
              copyToClipboard(canonical, flash);
            });
        } else {
          copyToClipboard(canonical, flash);
        }
        function flash() {
          button.setAttribute("data-state", "copied");
          if (label) {
            label.textContent = "Link copied";
          }
          window.setTimeout(function () {
            button.removeAttribute("data-state");
            if (label) {
              label.textContent = button.getAttribute("data-original-label") || "Copy link";
            }
          }, 1800);
        }
      });
    });
  }

  /* ---------- Hub search ---------- */
  function initSearch() {
    var input = document.getElementById("blog-search");
    var library = document.getElementById("blog-library");
    var hint = document.getElementById("blog-search-count");
    if (!input || !library) {
      return;
    }
    var prefill = "";
    try {
      var q = new URLSearchParams(window.location.search).get("q");
      if (q) {
        prefill = q;
      }
    } catch (e) {
      prefill = "";
    }
    var rows = [];
    var allCards = Array.prototype.slice.call(library.querySelectorAll(".articles-grid .card"));
    // Build the searchable set from the JSON if present, else fall back to visible cards.
    function applyPrefill() {
      if (prefill) {
        input.value = prefill;
        input.dispatchEvent(new Event("input", { bubbles: true }));
      }
    }
    fetch("search-index.json")
      .then(function (r) {
        return r.ok ? r.json() : null;
      })
      .then(function (data) {
        if (data && data.length) {
          rows = data;
        }
        bind();
        applyPrefill();
      })
      .catch(function () {
        bind();
        applyPrefill();
      });

    function norm(s) {
      return (s || "").toLowerCase();
    }

    function slugOf(href) {
      return (href || "").replace(/.*\/blog\//, "").replace(/\/$/, "");
    }

    function bind() {
      input.addEventListener("input", function () {
        var q = norm(input.value.trim());
        var groups = Array.prototype.slice.call(library.querySelectorAll(".library-group"));
        if (!q) {
          library.classList.remove("filtered");
          allCards.forEach(function (card) {
            card.style.display = "";
          });
          groups.forEach(function (g) {
            g.style.display = "";
            g.removeAttribute("data-empty");
          });
          if (hint) {
            hint.textContent = "";
          }
          return;
        }
        library.classList.add("filtered");
        var matchSlugs = {};
        var matched = 0;
        rows.forEach(function (row) {
          if (
            norm(row.title).indexOf(q) !== -1 ||
            norm(row.kw).indexOf(q) !== -1 ||
            norm(row.cluster).indexOf(q) !== -1
          ) {
            matchSlugs[row.slug] = true;
            matched += 1;
          }
        });
        allCards.forEach(function (card) {
          card.style.display = matchSlugs[slugOf(card.getAttribute("href"))] ? "" : "none";
        });
        groups.forEach(function (g) {
          var shown = 0;
          Array.prototype.forEach.call(g.querySelectorAll(".card"), function (c) {
            if (c.style.display !== "none") {
              shown += 1;
            }
          });
          g.style.display = shown === 0 ? "none" : "";
          g.setAttribute("data-empty", shown === 0 ? "true" : "false");
        });
        if (hint) {
          hint.textContent = matched
            ? matched + " matching guide" + (matched === 1 ? "" : "s")
            : "No matches — try a shorter word.";
        }
      });
    }
  }

  function init() {
    computeReadingTime();
    buildToc();
    bindShare();
    initSearch();
    updateProgress();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
