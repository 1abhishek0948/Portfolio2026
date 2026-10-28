(function () {
  "use strict";

  var document = window.document;
  var article = document.querySelector(".article-body");
  var progressBar = document.querySelector(".reading-progress");
  var rail = document.querySelector(".sticky-rail");
  var tocList = document.getElementById("toc-list");
  var reducingMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function setText(el, text) {
    if (el) {
      el.textContent = text;
    }
  }

  /* ---------- Reading time (from actual rendered text) ---------- */
  function computeReadingTime() {
    var slots = document.querySelectorAll("[data-reading-time]");
    if (!article || !slots.length) {
      return;
    }
    var words = article.textContent.trim().split(/\s+/).length;
    var minutes = Math.max(1, Math.round(words / 210));
    slots.forEach(function (slot) {
      setText(slot.querySelector("[data-reading-minutes]"), String(minutes));
      slot.removeAttribute("hidden");
    });
  }

  /* ---------- Reading progress ---------- */
  var ticking = false;

  function updateProgress() {
    ticking = false;
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
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(updateProgress);
    }
  }

  /* ---------- Table of contents ---------- */
  function buildToc() {
    if (!rail || !tocList || !article) {
      return;
    }
    var headings = Array.prototype.slice.call(
      article.querySelectorAll("h2[id]")
    );
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

    var links = tocList.querySelectorAll("a");

    function setActive() {
      var fromTop =
        window.scrollY +
        (window.innerHeight * 0.4);
      var firstVisible = -1;
      headings.forEach(function (heading, index) {
        if (heading.getBoundingClientRect().top + window.scrollY <= fromTop) {
          firstVisible = index;
        }
      });
      links.forEach(function (link, index) {
        if (index === firstVisible) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });
    }

    if (!reducingMotion.matches && "IntersectionObserver" in window) {
      var visibility = headings.map(function () {
        return false;
      });
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            visibility[headings.indexOf(entry.target)] = entry.isIntersecting;
          });
          var firstVisible = visibility.findIndex(Boolean);
          links.forEach(function (link, index) {
            if (index === firstVisible) {
              link.setAttribute("aria-current", "location");
            } else {
              link.removeAttribute("aria-current");
            }
          });
        },
        { rootMargin: "-5% 0px -60% 0px", threshold: 0 }
      );
      headings.forEach(function (heading) {
        observer.observe(heading);
      });
    } else {
      window.addEventListener("scroll", setActive, { passive: true });
      setActive();
    }
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
    } catch (error) {
      /* clipboard unavailable — keep silent */
    }
    document.body.removeChild(input);
  }

  function bindShare() {
    var buttons = document.querySelectorAll("[data-share]");
    if (!buttons.length) {
      return;
    }
    var title = document.title;
    var canonical =
      document.querySelector('link[rel="canonical"]') &&
      document.querySelector('link[rel="canonical"]').href;

    buttons.forEach(function (button) {
      var mode = button.getAttribute("data-share");
      var originalLabel = button.querySelector("[data-share-label]");
      var resetTimer = null;

      function flashCopied() {
        button.setAttribute("data-state", "copied");
        if (originalLabel) {
          originalLabel.textContent = "Link copied";
        }
        window.clearTimeout(resetTimer);
        resetTimer = window.setTimeout(function () {
          button.removeAttribute("data-state");
          if (originalLabel) {
            originalLabel.textContent =
              button.getAttribute("data-original-label") || originalLabel.textContent;
          }
        }, 1800);
      }

      button.addEventListener("click", function () {
        if (mode === "share" && navigator.share) {
          navigator.share({ title: title, url: canonical }).catch(function () {
            copyToClipboard(canonical, flashCopied);
          });
        } else {
          copyToClipboard(canonical, flashCopied);
        }
      });

      if (originalLabel) {
        button.setAttribute("data-original-label", originalLabel.textContent);
      }
    });
  }

  /* ---------- Boot ---------- */
  function init() {
    computeReadingTime();
    buildToc();
    bindShare();
    updateProgress();
    if (progressBar) {
      window.addEventListener("scroll", onScroll, { passive: true });
      window.addEventListener("resize", onScroll, { passive: true });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
