const crypto = require("crypto");

// Vos clés et tokens
// oauth_consumer_key = API Key (Twitter Developer Portal)
const oauth_consumer_key = process.env.TWITTER_API_KEY;
// oauth_consumer_secret = API Key Secret (Twitter Developer Portal)
const oauth_consumer_secret = process.env.TWITTER_API_SECRET_KEY;
// oauth_token = Access Token (Twitter Developer Portal)
const oauth_token = process.env.TWITTER_ACCESS_TOKEN;
// oauth_token_secret = Access Token Secret (Twitter Developer Portal)
const oauth_token_secret = process.env.TWITTER_ACCESS_TOKEN_SECRET;

// Paramètres de la requête
const method = "POST";
const url = "https://upload.twitter.com/1.1/media/upload.json";
const timestamp = Math.floor(Date.now() / 1000).toString();
const nonce = crypto
  .randomBytes(32)
  .toString("base64")
  .replace(/[^a-zA-Z0-9]/g, "");

// Paramètres OAuth
const parameters = {
  oauth_consumer_key,
  oauth_nonce: nonce,
  oauth_signature_method: "HMAC-SHA1",
  oauth_timestamp: timestamp,
  oauth_token,
  oauth_version: "1.0",
};

// Trier les paramètres
const sortedParams = Object.keys(parameters)
  .sort()
  .reduce((acc, key) => {
    acc[key] = parameters[key];
    return acc;
  }, {});

// Créer la chaîne de paramètres
const paramString = Object.entries(sortedParams)
  .map(
    ([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`
  )
  .join("&");

// Créer la chaîne de base pour la signature
const baseString = [
  method,
  encodeURIComponent(url),
  encodeURIComponent(paramString),
].join("&");

// Créer la clé de signature
const signingKey = `${encodeURIComponent(
  oauth_consumer_secret
)}&${encodeURIComponent(oauth_token_secret)}`;

// Générer la signature
const signature = crypto
  .createHmac("sha1", signingKey)
  .update(baseString)
  .digest("base64");

// Créer l'en-tête Authorization au format exact requis
const authHeader = `OAuth oauth_consumer_key="${oauth_consumer_key}", oauth_token="${oauth_token}", oauth_signature_method="HMAC-SHA1", oauth_timestamp="${timestamp}", oauth_nonce="${nonce}", oauth_version="1.0", oauth_signature="${encodeURIComponent(
  signature
)}"`;

// Cookie header
const cookieHeader = "guest_id=v1%3A173450663175949164;lang=en;";

console.log("Headers à utiliser dans n8n:");
console.log("\nAuthorization:");
console.log(authHeader);
console.log("\ncookie:");
console.log(cookieHeader);
