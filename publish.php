<?php
/**
 * ContentHub — Publish API
 * --------------------------
 * Endpoint your VPS AI bots POST new content to.
 * Each post is validated, assigned an id, and appended to content.json.
 *
 * Usage from your bot:
 *   POST /publish.php?key=YOUR_SECRET_KEY
 *   Content-Type: application/json
 *   {
 *     "type": "blog" | "news" | "facts",
 *     "title": "…",                    // required for blog & news
 *     "excerpt": "…",                  // optional short summary
 *     "body": "…",                     // required for blog & news
 *     "tag": "Technology",             // optional category label
 *     "author": "Bot Name",            // optional
 *     "fact": "…",                     // required when type = facts
 *     "category": "Nature"             // optional for facts
 *   }
 *
 * Response: 200 {"ok":true,"id":"n1042","total":42}
 * Errors:    400 (bad payload) | 401 (bad key) | 500 (write failure)
 */

// ---------- Config ----------
// CHANGE THIS to a long random string known only to your bots.
$SECRET_KEY = 'CHANGE_ME_to_a_long_random_secret';
$FILE = __DIR__ . '/content.json';
$MAX_ITEMS = 200;          // keep the file lean
$MAX_BODY   = 60000;       // max chars per article body
$MAX_TITLE  = 200;
$MAX_FACT   = 2000;

header('Content-Type: application/json; charset=utf-8');

function fail($code, $msg) {
  http_response_code($code);
  echo json_encode(['ok' => false, 'error' => $msg]);
  exit;
}

// 1) Auth
if (!isset($_GET['key']) || !hash_equals($SECRET_KEY, $_GET['key'])) {
  fail(401, 'Unauthorized. Pass ?key=YOUR_SECRET_KEY.');
}

// 2) Read + parse JSON body
$raw = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!is_array($data)) fail(400, 'Invalid JSON body.');

$type = $data['type'] ?? '';
if (!in_array($type, ['blog', 'news', 'facts'], true)) fail(400, "type must be blog, news or facts.");

// 3) Validate per type
$item = ['id' => '', 'date' => date('Y-m-d'), 'read' => '3 min'];
$item['tag'] = substr((string)($data['tag'] ?? 'General'), 0, 60);
$item['author'] = substr((string)($data['author'] ?? 'Content Bot'), 0, 80);

if ($type === 'facts') {
  $fact = trim((string)($data['fact'] ?? ''));
  if ($fact === '') fail(400, 'facts require a "fact" field.');
  if (mb_strlen($fact) > $MAX_FACT) fail(400, 'fact too long.');
  $item['fact'] = $fact;
  $item['category'] = substr((string)($data['category'] ?? 'General'), 0, 60);
} else {
  $title = trim((string)($data['title'] ?? ''));
  if ($title === '') fail(400, 'blog/news require a "title" field.');
  $body = trim((string)($data['body'] ?? ''));
  if ($body === '') fail(400, 'blog/news require a "body" field.');
  if (mb_strlen($title) > $MAX_TITLE) fail(400, 'title too long.');
  if (mb_strlen($body)  > $MAX_BODY)  fail(400, 'body too long.');
  $item['title']   = $title;
  $item['body']    = $body;
  $item['excerpt'] = substr(trim((string)($data['excerpt'] ?? $body)), 0, 240);
  if (!empty($data['read'])) $item['read'] = substr((string)$data['read'], 0, 20);
}

// 4) Load existing feed
$feed = file_exists($FILE) ? json_decode(file_get_contents($FILE), true) : null;
if (!is_array($feed) || !isset($feed[$type])) {
  $feed = ['updated' => '', 'blog' => [], 'news' => [], 'facts' => []];
}

// 5) Unique id + prepend (newest first)
$prefix = $type === 'facts' ? 'f' : ($type === 'news' ? 'n' : 'b');
$seq = count($feed[$type]) + 1;
$item['id'] = $prefix . $seq;
array_unshift($feed[$type], $item);

// 6) Cap size
if (count($feed[$type]) > $MAX_ITEMS) {
  $feed[$type] = array_slice($feed[$type], 0, $MAX_ITEMS);
}

// 7) Write atomically
$feed['updated'] = gmdate('c');
$tmp = $FILE . '.tmp';
if (file_put_contents($tmp, json_encode($feed, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) === false) {
  fail(500, 'Could not write feed.');
}
if (!rename($tmp, $FILE)) fail(500, 'Could not replace feed.');

echo json_encode(['ok' => true, 'id' => $item['id'], 'total' => count($feed[$type])]);