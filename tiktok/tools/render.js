// Rendert eine Szene (scene.html mit window.renderFrame(t)) Bild für Bild zu MP4 (1080x1920, 30fps).
// Usage: node render.js <scene.html> <out.mp4>
//        node render.js <scene.html> --stills 1.5,8,20 <ordner>
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
(async () => {
  const [scene, ...args] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(scene) + '#render');
  await page.waitForFunction(() => window.READY === true);
  const draw = 't => window.renderFrame(window.mapTime ? window.mapTime(t) : t)';
  if (args[0] === '--stills') {
    const dir = args[2] || 'stills'; fs.mkdirSync(dir, { recursive: true });
    for (const t of args[1].split(',').map(Number)) {
      await page.evaluate(`(${draw})(${t})`);
      await page.screenshot({ path: path.join(dir, `t${t.toFixed(2).padStart(6, '0')}.png`) });
    }
    return browser.close();
  }
  const fps = 30, total = Math.round(await page.evaluate(() => window.DURATION) * fps);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', args[0]], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < total; i++) {
    const b64 = await page.evaluate(`(${draw})(${i / fps}), document.getElementById('c').toDataURL('image/jpeg', 0.95).split(',')[1]`);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await browser.close();
  console.log('wrote', args[0]);
})();
