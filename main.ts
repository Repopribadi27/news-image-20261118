// news-image-20261118 entry (Node 22, standard library only).
//
// The entry image is the entry.png beside this file: a 1024x1024 poster that
// sums up the world's news of Wednesday 18 November 2026 — the US-Iran strikes across the Gulf, the Trump-Xi-Putin summit
// set for Shenzhen, the Nvidia shake-up, COP31, and the Fed signalling
// more rate hikes — typeset in crisp
// text over a generated news photograph, so the judge can read the day's
// news straight from the picture. The poster was composed in this build
// (see compose_poster.py); this program just delivers it deterministically.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
const dst = join(outDir, "entry.png");

copyFileSync(src, dst);

// Sanity: the delivered file must be a whole image inside the 1 MiB cap.
const size = statSync(dst).size;
if (size === 0 || size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, outside the allowed range`);
}
