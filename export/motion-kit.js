// Reusable motion functions for the five recipes in channel/motion-recipes.md — each one
// was built and verified as an isolated comparison demo, approved by him one at a time,
// before being turned into this shared module. Include with <script src="../export/
// motion-kit.js"> in a reel build, then call these from the build's own render() loop
// (the same t-driven, deterministic pattern every reel.html already uses — no GSAP
// dependency, matching the vanilla render loop the reel templates already run on).
//
// Every function is pure math driven by a single time value passed in each frame — never
// real time, never Math.random — so renders stay frame-accurate under FRAMES=1 capture.

(function (global) {
  "use strict";

  function clamp01(x) { return Math.min(1, Math.max(0, x)); }
  // power3.out — the smooth, no-overshoot settle. Never use a bouncy back.out/cubic-bezier
  // overshoot here: per hyperframes-animation's spring-pop-entrance.md, bounce is "the #1
  // instant turn-off in agent-made videos."
  function smoothIn(p) { return 1 - Math.pow(1 - p, 3); }
  function powerIn2(p) { return p * p; }
  function powerIn3(p) { return p * p * p; }

  // Deterministic PRNG (mulberry32) — the only allowed source of "randomness" in a
  // HyperFrames-style render. Same seed always produces the same sequence.
  function mulberry32(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t ^= t + Math.imul(t ^ (t >>> 7), 61 | t);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ===== Recipe 1 & 2: word-by-word text build =====
  // Wrap `text` in <span class="wd">word</span> spans (one per word, spaces preserved
  // between them) and return the list of span elements in order, ready to animate.
  function splitWords(container, text) {
    var words = text.split(/\s+/).filter(Boolean);
    container.innerHTML = words.map(function (w, i) {
      return '<span class="wd" id="' + container.id + '-w' + i + '" style="opacity:0;display:inline-block">' + w + '</span>';
    }).join(' ');
    return words.map(function (_, i) { return document.getElementById(container.id + '-w' + i); });
  }

  // Animate the words already built by splitWords() for the given frame time `t`.
  //   startAt: when word 0 begins: opts.gap between each word's start, opts.dur each word's own rise.
  function animateWords(spans, t, startAt, gap, dur, riseY) {
    riseY = riseY == null ? 14 : riseY;
    for (var i = 0; i < spans.length; i++) {
      var at = startAt + i * gap;
      var e = smoothIn(clamp01((t - at) / dur));
      spans[i].style.opacity = String(e);
      spans[i].style.transform = 'translateY(' + (riseY * (1 - e)) + 'px)';
    }
  }
  // Returns the time the last word finishes, so a caller can chain the next beat.
  function wordsEndAt(spans, startAt, gap, dur) {
    return startAt + Math.max(0, spans.length - 1) * gap + dur;
  }

  // ===== Recipe 2: per-word text highlight (fixes the line-wrap bug) =====
  // Never draw ONE box across a multi-word phrase — a phrase that line-wraps has no
  // single rectangle, and a stretched absolutely-positioned box collapses into a thin
  // sliver at the wrap point. Build one bar PER WORD instead; call this after the words
  // are in their final laid-out position (their opacity animating later doesn't move
  // layout, so this is safe to call immediately after splitWords()).
  function buildHighlightBars(container, wordEls) {
    var rect = container.getBoundingClientRect();
    return wordEls.map(function (el) {
      var r = el.getBoundingClientRect();
      var bar = document.createElement('div');
      bar.className = 'hlbar';
      bar.style.cssText = 'position:absolute;background:#FFD835;opacity:0;transform:scaleX(0);' +
        'transform-origin:left center;border-radius:5px;z-index:0;' +
        'left:' + (r.left - rect.left - 6) + 'px;' +
        'top:' + (r.top - rect.top - 4) + 'px;' +
        'width:' + (r.width + 12) + 'px;' +
        'height:' + (r.height + 8) + 'px;';
      container.insertBefore(bar, container.firstChild);
      return bar;
    });
  }
  // Bars grow AND fade in together — a bar at low scaleX with full opacity reads as a
  // stray glitch line, not a growing highlight.
  function animateHighlightBars(bars, t, startAt, dur, stagger) {
    stagger = stagger == null ? 0.06 : stagger;
    bars.forEach(function (bar, i) {
      var e = smoothIn(clamp01((t - (startAt + i * stagger)) / dur));
      bar.style.transform = 'scaleX(' + e.toFixed(3) + ')';
      bar.style.opacity = String(0.4 * Math.min(1, e / 0.35));
    });
  }

  // ===== Recipe 1 & 3: spring-pop entrance with an optional glow bloom behind it =====
  // Smooth scale-in (0->1, no overshoot), glow lands on the SAME beat, never before/after.
  function animatePop(el, t, at, dur) {
    var e = smoothIn(clamp01((t - at) / dur));
    el.style.opacity = String(e);
    el.style.transform = 'scale(' + e.toFixed(3) + ')';
    return e;
  }
  function animateGlowBloom(glowEl, t, at, dur, peakOpacity) {
    peakOpacity = peakOpacity == null ? 0.35 : Math.min(0.45, peakOpacity); // hard ceiling
    var e = smoothIn(clamp01((t - at) / dur));
    glowEl.style.opacity = String(peakOpacity * e);
    glowEl.style.transform = 'scale(' + (0.8 + 0.3 * e).toFixed(3) + ')';
  }

  // ===== Recipe 3: brief impact shake (camera-shake variant of multi-phase-camera) =====
  function impactShake(t, at, dur, amp) {
    amp = amp == null ? 6 : amp;
    var sp = t - at;
    if (sp < 0 || sp >= dur) return 0;
    return Math.sin(sp * 70) * amp * (1 - sp / dur);
  }

  // ===== Recipe 1 & 4: multi-phase camera (pull-back -> hold -> push) =====
  // Replaces a flat linear zoom with a real phase curve. `t` is the scene-relative time;
  // pushAt/pushDur should usually be timed to land ON a content beat (e.g. the climax
  // word), not a fixed clock value — see multi-phase-camera.md's "phase trigger by
  // content beat" note.
  function multiPhaseCamera(t, opts) {
    opts = opts || {};
    var settleDur = opts.settleDur == null ? 0.5 : opts.settleDur;
    var pullBack = opts.pullBack == null ? 0.95 : opts.pullBack;
    var pushAt = opts.pushAt == null ? 3.0 : opts.pushAt;
    var pushDur = opts.pushDur == null ? 0.9 : opts.pushDur;
    var pushTo = opts.pushTo == null ? 1.10 : opts.pushTo;
    if (t < settleDur) {
      return pullBack + (1 - pullBack) * smoothIn(clamp01(t / settleDur));
    } else if (t < pushAt) {
      return 1.0;
    } else {
      return 1.0 + (pushTo - 1.0) * smoothIn(clamp01((t - pushAt) / pushDur));
    }
  }

  // ===== Recipe 4: zoom-through scene transition =====
  // outEl/inEl are the two <section class="scene"> (or equivalent) elements. Call every
  // frame during the transition window; harmless to call outside it (it clamps to the
  // resting state on either side).
  function zoomThroughTransition(outEl, inEl, t, outStart, inStart, outDur, inDur) {
    if (t < outStart) {
      outEl.style.opacity = '1'; outEl.style.transform = 'scale(1)'; outEl.style.filter = 'blur(0px)';
    } else if (t < outStart + outDur) {
      var oe = powerIn3((t - outStart) / outDur);
      outEl.style.opacity = String(1 - oe);
      outEl.style.transform = 'scale(' + (1 + 1.5 * oe).toFixed(3) + ')';
      outEl.style.filter = 'blur(' + (8 * oe).toFixed(1) + 'px)';
    } else {
      outEl.style.opacity = '0';
    }
    if (t < inStart) {
      inEl.style.opacity = '0';
    } else {
      var ie = smoothIn(Math.min(1, (t - inStart) / inDur));
      inEl.style.opacity = String(ie);
      inEl.style.transform = 'scale(' + (0.5 + 0.5 * ie).toFixed(3) + ')';
      inEl.style.filter = 'blur(' + (8 * (1 - ie)).toFixed(1) + 'px)';
    }
  }
  // A brief white flash at the transition's crossover point — the "High energy" accent
  // from transitions/overview.md's energy table. Optional; skip for calmer episodes.
  function transitionFlash(flashEl, t, crossoverAt, dur) {
    dur = dur == null ? 0.16 : dur;
    var fp = t - crossoverAt;
    flashEl.style.opacity = String(fp >= 0 && fp < dur ? Math.sin((fp / dur) * Math.PI) * 0.5 : 0);
  }

  // ===== Recipe 5: fragment shatter (the one-hero-beat GPU-tier effect) =====
  // Draws `srcCanvas` (already rendered once with the false-claim content) as a grid of
  // fragments that fly apart deterministically. Returns a `render(ctx, t)` function to
  // call every frame — draws the whole badge before `holdDur`, then the exploding
  // fragments after it. `seed` fixes the PRNG so the shatter pattern never changes
  // between renders (required for FRAMES=1 frame-accurate capture).
  function buildShatter(srcCanvas, opts) {
    opts = opts || {};
    var cols = opts.cols || 8, rows = opts.rows || 4;
    var holdDur = opts.holdDur == null ? 1.4 : opts.holdDur;
    var shatterDur = opts.shatterDur == null ? 0.85 : opts.shatterDur;
    var rng = mulberry32(opts.seed == null ? 42 : opts.seed);
    var w = srcCanvas.width, h = srcCanvas.height;
    var fw = w / cols, fh = h / rows;
    var frags = [];
    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var ang = rng() * Math.PI * 2;
        var dist = 260 + rng() * 420;
        frags.push({
          sx: c * fw, sy: r * fh, sw: fw, sh: fh,
          dx: Math.cos(ang) * dist, dy: Math.sin(ang) * dist - 120,
          rot: (rng() - 0.5) * 6,
          delay: rng() * 0.35,
        });
      }
    }
    return {
      holdDur: holdDur, shatterDur: shatterDur, totalDur: holdDur + shatterDur,
      render: function (ctx, t, cx, cy) {
        if (t < holdDur) {
          ctx.drawImage(srcCanvas, 0, 0, w, h, cx - w / 2, cy - h / 2, w, h);
          return;
        }
        var sp = t - holdDur;
        frags.forEach(function (f) {
          var p = clamp01((sp - f.delay) / (shatterDur - f.delay));
          if (p <= 0) {
            ctx.drawImage(srcCanvas, f.sx, f.sy, f.sw, f.sh, cx - w / 2 + f.sx, cy - h / 2 + f.sy, f.sw, f.sh);
            return;
          }
          var e = powerIn2(p);
          var alpha = 1 - smoothIn(p);
          if (alpha <= 0.01) return;
          var x = cx - w / 2 + f.sx + f.dx * e;
          var y = cy - h / 2 + f.sy + f.dy * e;
          ctx.save();
          ctx.globalAlpha = alpha;
          ctx.translate(x + f.sw / 2, y + f.sh / 2);
          ctx.rotate(f.rot * e);
          ctx.drawImage(srcCanvas, f.sx, f.sy, f.sw, f.sh, -f.sw / 2, -f.sh / 2, f.sw, f.sh);
          ctx.restore();
        });
      },
    };
  }

  global.MotionKit = {
    clamp01: clamp01, smoothIn: smoothIn, powerIn2: powerIn2, powerIn3: powerIn3,
    mulberry32: mulberry32,
    splitWords: splitWords, animateWords: animateWords, wordsEndAt: wordsEndAt,
    buildHighlightBars: buildHighlightBars, animateHighlightBars: animateHighlightBars,
    animatePop: animatePop, animateGlowBloom: animateGlowBloom, impactShake: impactShake,
    multiPhaseCamera: multiPhaseCamera,
    zoomThroughTransition: zoomThroughTransition, transitionFlash: transitionFlash,
    buildShatter: buildShatter,
  };
})(window);
