#!/usr/bin/env node
// v0 probe: prints the suite's identity env and logs what the fresh stack offers.
const BASE = process.env.BASE_URL || 'http://localhost';
const log = (...m) => console.error('[ci-identities]', ...m);

async function get(path) {
  try {
    const r = await fetch(`${BASE}${path}`, { redirect: 'manual' });
    const text = await r.text();
    return `${r.status} ${text.slice(0, 300).replace(/\s+/g, ' ')}`;
  } catch (e) {
    return `ERR ${e.message}`;
  }
}

for (const p of [
  '/identity/v1/auth-methods?surface=configurator',
  '/identity/v1/session?surface=configurator',
  '/identity/v1/tenant-contexts/pg',
  '/identity/v1/tenant-contexts/pg-citya',
  '/identity/v1/tenant-contexts/citya',
  '/auth/realms/digit/.well-known/openid-configuration',
  '/configurator/login',
  '/digit-ui/globalConfigs.js',
]) log(p, '→', await get(p));

console.log('IDENTITY_TEST_OTP_CODE=123456');
