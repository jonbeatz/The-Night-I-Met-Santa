#!/usr/bin/env node
/** Sync MCP env from THIS repo's .env.local (bootstrap copies to scripts/) */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ENV_LOCAL = path.join(REPO_ROOT, '.env.local');
const GLOBAL_MCP = path.join(os.homedir(), '.cursor', 'mcp.json');
const PROJECT_MCP = path.join(REPO_ROOT, '.cursor', 'mcp.json');

function parseEnvFile(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`.env.local not found: ${filePath}`);
  }
  const env = {};
  for (const line of fs.readFileSync(filePath, 'utf8').split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    let value = trimmed.slice(eq + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    env[key] = value;
  }
  return env;
}

function setNestedEnv(config, serverName, envUpdates) {
  const server = config.mcpServers?.[serverName];
  if (!server) return false;
  server.env = server.env || {};
  let changed = false;
  for (const [key, value] of Object.entries(envUpdates)) {
    if (!value) continue;
    if (server.env[key] !== value) {
      server.env[key] = value;
      changed = true;
    }
  }
  return changed;
}

function main() {
  const env = parseEnvFile(ENV_LOCAL);
  console.log(`[sync:mcp-env] Repo: ${REPO_ROOT}`);

  if (!fs.existsSync(GLOBAL_MCP)) {
    console.warn('WARN: Global MCP config not found');
    process.exit(1);
  }

  const globalConfig = JSON.parse(fs.readFileSync(GLOBAL_MCP, 'utf8'));

  if (env.GITHUB_PERSONAL_ACCESS_TOKEN && globalConfig.mcpServers?.github) {
    setNestedEnv(globalConfig, 'github', {
      GITHUB_PERSONAL_ACCESS_TOKEN: env.GITHUB_PERSONAL_ACCESS_TOKEN,
    });
    console.log('OK: github -> global');
  }

  if (env.TAVILY_API_KEY && globalConfig.mcpServers?.tavily) {
    setNestedEnv(globalConfig, 'tavily', { TAVILY_API_KEY: env.TAVILY_API_KEY });
    console.log('OK: tavily -> global');
  }

  const hostingerServers = Object.keys(globalConfig.mcpServers || {}).filter((n) =>
    n.startsWith('hostinger-'),
  );
  if (env.HOSTINGER_API_TOKEN && hostingerServers.length) {
    for (const name of hostingerServers) {
      setNestedEnv(globalConfig, name, { HOSTINGER_API_TOKEN: env.HOSTINGER_API_TOKEN });
    }
    console.log(`OK: hostinger (${hostingerServers.length} servers) -> global`);
  }

  fs.writeFileSync(GLOBAL_MCP, `${JSON.stringify(globalConfig, null, 2)}\n`, 'utf8');
  console.log('Next: Reload MCP in Cursor (Settings -> MCP -> refresh).');
}

try {
  main();
} catch (err) {
  console.error(`FAIL: ${err.message}`);
  process.exit(1);
}
