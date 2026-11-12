// يعمل بـ: node tests/crypto.test.js
const assert = require("assert");
const crypto = require("crypto");

// اختبار توافق MD5+SHA (تحقق من صحة الخوارزميات الأساسية)
function md5hex(s) {
  return crypto.createHash("md5").update(s).digest("hex");
}

assert.strictEqual(md5hex("test").length, 32);
assert.strictEqual(md5hex("hello"), "5d41402abc4b2a76b9719d911017c592");

// اختبار AES ECB
function aesEncryptBase64(plain, key) {
  const c = crypto.createCipheriv("aes-128-ecb", Buffer.from(key), null);
  return Buffer.concat([c.update(plain), c.final()]).toString("base64");
}
const enc = aesEncryptBase64("hello", "abcdefgh12345678");
assert.ok(enc.length > 0);

console.log("✅ كل اختبارات JS نجحت");
