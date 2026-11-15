// Renders scene.html frame-by-frame into an MP4 (1080x1920, 30fps) via ffmpeg.
// Usage: node render.js [out.mp4] [--stills t1,t2,...]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

(async () => {
  const args = process.argv.slice(2);
  const stillsIdx = args.indexOf('--stills');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'scene.html') + '#render');
  await page.waitForFunction(() => window.READY === true);

  if (stillsIdx >= 0) {
    const outDir = args[stillsIdx + 1 + 1] || path.join(__dirname, 'stills');
    fs.mkdirSync(outDir, { recursive: true });
    for (const t of args[stillsIdx + 1].split(',').map(Number)) {
      await page.evaluate(t => window.renderFrame(t), t);
      await page.screenshot({ path: path.join(outDir, `t${String(t).padStart(5, '0')}.png`) });
    }
    await browser.close(); return;
  }

  const out = args[0] || path.join(__dirname, 'video_noaudio.mp4');
  const fps = 30;
  const duration = await page.evaluate(() => window.DURATION);
  const total = Math.round(duration * fps);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < total; i++) {
    const b64 = await page.evaluate(t => { window.renderFrame(window.mapTime ? window.mapTime(t) : t); return document.getElementById('c').toDataURL('image/jpeg', 0.95).split(',')[1]; }, i / fps);
    const buf = Buffer.from(b64, 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('wrote', out);
})();
