// project-backup.mjs — The-Night-I-Met-Santa (book-tuned tiers)
//
// Three tiers (this project only — does not change other Hermes profiles):
//   QUICK / LIGHT / STANDARD  — daily restore (locks + current dials + DTP + Output)
//   FULL                      — milestone / gift snapshot (all mocks + Images + Xtraz; skip old dial batches)
//   ARCHIVE                   — deep freeze (includes old Media/generated dial batches; still skip reinstallable deps)
//
// Folder naming: the-night-i-met-santa-project-v{N}-{letter}
// Backups go to: G:\Hermes_Project_BackUpz\The-Night-I-Met-Santa\
//
// Usage:
//   node scripts/project-backup.mjs [--quick|--light|--standard|--full|--archive] [--yes] [--dry-run] [--note "..."]
//
// npm:
//   backup:quick / backup:light  -> QUICK + --yes
//   backup:full                  -> FULL + --yes
//   backup:archive               -> ARCHIVE + --yes
//   backup / backup:project      -> interactive tier pick

import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";

const REPO_ROOT = "D:\\Hermes\\projects\\The-Night-I-Met-Santa";
const DEFAULT_BACKUP_ROOT = "G:\\Hermes_Project_BackUpz\\The-Night-I-Met-Santa";
const BACKUP_FOLDER_BASE = "the-night-i-met-santa-project";
const BACKUP_FOLDER_PATTERN = new RegExp(
  `^${BACKUP_FOLDER_BASE.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}-v(\\d+)-([a-z])$`,
  "i",
);
const DEFAULT_START_VERSION = 1;
const NOTES_REL_PATH = path.join(".cursor", "BackUp-Notez.md");
const NOTES_FOOTER = "\n*Backup created — The-Night-I-Met-Santa project.*\n";

/** Reinstallable / website junk — always skip on every tier (leaf names; robocopy matches any depth) */
const ALWAYS_XD = [
  "node_modules",
  ".next",
  "out",
  "logs",
  "test-results",
  "__pycache__",
  ".venv",
  "venv",
];

/**
 * Old dial / rejected full-book batches (~1.5GB+).
 * Skip on QUICK + FULL. Include on ARCHIVE only.
 * Leaf directory names only — robocopy /XD relative paths from repo root are unreliable.
 */
const OLD_GENERATED_XD = [
  "test-batch",
  "test-batch-v2",
  "test-batch-v3",
  "test-book-v1",
  "test-book-v2",
  "test-covers-v3",
  "new-test-book-v1",
  "new-test-book-v2",
  "new-test-book-v3",
  "jack-likeness",
  "beat-gap-dial-01",
  "cover-d-santa-peek",
  "unify-eyes-met-test",
  "openrouter-cover-pj-test",
  "dedication-smoke",
  "model-compare-beat01",
  "style-match-santa-g0",
  "gemini-api-smoke",
];

/** Extra skips for daily QUICK only (leaf names) */
const QUICK_EXTRA_XD = [
  "_archive",
  "Lulu-Templates",
  // Keep mocks + approved + Output + working Adobe — do NOT skip Output/
];

const TIER_META = {
  QUICK: {
    label: "Quick (daily)",
    aliases: ["quick", "light", "standard", "s"],
    xd: () => [...ALWAYS_XD, ...OLD_GENERATED_XD, ...QUICK_EXTRA_XD],
    summary:
      "Locks + current mocks + DTP + Output flipbooks. Skips old dial batches, _archive, Lulu vendor zips, node_modules/.venv.",
  },
  FULL: {
    label: "Full (milestone)",
    aliases: ["full", "f", "milestone"],
    xd: () => [...ALWAYS_XD, ...OLD_GENERATED_XD],
    summary:
      "Gift snapshot: all mocks/Images/Xtraz + Output. Skips old rejected dial batches + reinstallable deps. Use before proof / End Project.",
  },
  ARCHIVE: {
    label: "Archive (deep)",
    aliases: ["archive", "a", "deep"],
    xd: () => [...ALWAYS_XD],
    summary:
      "Deep freeze including old Media/generated dial batches. Still skips node_modules/.venv. Rare — history also lives in older G: letters.",
  },
};

// ---- args -------------------------------------------------------------------
const rawArgs = process.argv.slice(2);
const noteFlagIndex = rawArgs.findIndex((a) => a === "--note" || a === "-n");
const userNoteFromCli = noteFlagIndex !== -1 ? (rawArgs[noteFlagIndex + 1] || "").trim() : "";
const args = noteFlagIndex === -1 ? rawArgs : rawArgs.filter((_, i) => i !== noteFlagIndex && i !== noteFlagIndex + 1);

const skipConfirm = args.includes("--yes") || args.includes("-y");
const isDryRun = args.includes("--dry-run");
const customName = args.find((a) => !a.startsWith("-") && !a.startsWith("--")) || null;

function resolveTierFromArgs() {
  if (args.includes("--archive") || args.includes("-a")) return "ARCHIVE";
  if (args.includes("--full") || args.includes("-f")) return "FULL";
  if (
    args.includes("--quick") ||
    args.includes("--light") ||
    args.includes("--standard") ||
    args.includes("-s") ||
    args.includes("-q") ||
    args.includes("-l")
  ) {
    return "QUICK";
  }
  return null; // interactive
}

// ---- helpers ----------------------------------------------------------------
function getProjectVersion() {
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(REPO_ROOT, "package.json"), "utf8"));
    if (pkg.version) return pkg.version;
  } catch {
    /* fallback */
  }
  return "unknown";
}

const formatBackupFolderName = (version, letter) => `${BACKUP_FOLDER_BASE}-v${version}-${letter}`;

function parseBackupFolder(name) {
  const m = name.match(BACKUP_FOLDER_PATTERN);
  return m ? { version: Number(m[1]), letter: m[2].toLowerCase() } : null;
}

function compareBackupFolders(a, b) {
  const pa = parseBackupFolder(a);
  const pb = parseBackupFolder(b);
  if (!pa || !pb) return a.localeCompare(b, undefined, { sensitivity: "base" });
  if (pa.version !== pb.version) return pa.version - pb.version;
  return pa.letter.localeCompare(pb.letter);
}

function listSequentialBackupFolders(backupRoot) {
  if (!fs.existsSync(backupRoot)) return [];
  return fs
    .readdirSync(backupRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory() && BACKUP_FOLDER_PATTERN.test(d.name))
    .map((d) => d.name)
    .sort(compareBackupFolders);
}

function suggestNextBackupFolder(backupRoot) {
  const existing = listSequentialBackupFolders(backupRoot);
  if (existing.length === 0) return formatBackupFolderName(DEFAULT_START_VERSION, "a");
  const { version, letter } = parseBackupFolder(existing[existing.length - 1]);
  if (letter < "z") return formatBackupFolderName(version, String.fromCharCode(letter.charCodeAt(0) + 1));
  return formatBackupFolderName(version + 1, "a");
}

const escapeTableCell = (text) => String(text).replace(/\|/g, "\\|").replace(/\r?\n/g, " ").trim();

function getGitInfo(repoRoot) {
  try {
    const run = (c) => execSync(c, { cwd: repoRoot, encoding: "utf8" }).trim();
    return {
      branch: run("git branch --show-current"),
      commit: run("git rev-parse --short HEAD"),
      message: run("git log -1 --pretty=%B").split("\n")[0],
    };
  } catch {
    return { branch: "unknown", commit: "unknown", message: "unknown" };
  }
}

function getExcludeDirs(tier) {
  return TIER_META[tier].xd();
}

function formatExcluded(tier) {
  const list = getExcludeDirs(tier);
  if (list.length === 0) return "None";
  const preview = list.slice(0, 8).map((d) => `${d}/`).join(", ");
  return list.length > 8 ? `${preview}, … (+${list.length - 8} more)` : preview;
}

function verifyBackupContents(backupPath, tier) {
  const errors = [];
  const warnings = [];
  const checks = [
    { path: "package.json", type: "file", required: true },
    { path: "TRUTH.md", type: "file", required: true },
    { path: "AGENTS.md", type: "file", required: true },
    { path: ".env.local", type: "file", required: false, label: ".env.local (secrets)" },
    { path: ".cursor", type: "dir", required: true },
    { path: "scripts", type: "dir", required: true },
    { path: "Media/approved/characters/santa-G0-v2.png", type: "file", required: false, label: "santa-G0-v2 lock" },
    { path: "Media/approved/style-refs/style-lock-v2.png", type: "file", required: false, label: "style-lock-v2" },
    { path: "Media/generated/mocks/_FLOW-CURRENT.json", type: "file", required: false, label: "FLOW-CURRENT SoT" },
    { path: "Xtraz/Adobe-Photoshop", type: "dir", required: false, label: "Photoshop working" },
    { path: "Output", type: "dir", required: false, label: "Output (flipbooks) — must NOT be skipped" },
  ];

  for (const check of checks) {
    const targetPath = path.join(backupPath, check.path);
    if (!fs.existsSync(targetPath)) {
      (check.required ? errors : warnings).push(
        `Missing ${check.required ? "required" : "optional"} ${check.type}: ${check.label || check.path}`,
      );
    } else {
      const stat = fs.statSync(targetPath);
      if (check.type === "file" && !stat.isFile()) errors.push(`Expected file, found directory: ${check.path}`);
      else if (check.type === "dir" && !stat.isDirectory()) errors.push(`Expected directory, found file: ${check.path}`);
    }
  }

  // Book-specific: warn if Output was emptied by an accidental skip
  const outputDir = path.join(backupPath, "Output");
  if (fs.existsSync(outputDir)) {
    const pdfs = fs.readdirSync(outputDir).filter((f) => f.toLowerCase().endsWith(".pdf"));
    if (pdfs.length === 0) warnings.push("Output/ present but no flipbook PDFs found");
  }

  return { success: errors.length === 0, errors, warnings, checkedItemsCount: checks.length, tier };
}

function buildNoteEntry({ timestamp, tier, userNotes, gitInfo, backupFolder, projectVersion, verification }) {
  const typeLabel = TIER_META[tier].label;
  let entry = `## [${timestamp}] - ${typeLabel} Backup\n\n`;
  entry += userNotes?.trim() ? `**My Notes:** ${userNotes.trim()}\n\n---\n\n` : `---\n\n`;
  entry += `| Field | Value |\n|-------|-------|\n`;
  entry += `| **Folder** | ${escapeTableCell(backupFolder)} |\n`;
  entry += `| **Version** | ${escapeTableCell(projectVersion)} |\n`;
  entry += `| **Branch** | ${escapeTableCell(gitInfo.branch)} |\n`;
  entry += `| **Commit** | ${escapeTableCell(gitInfo.commit)} |\n`;
  entry += `| **Message** | ${escapeTableCell(gitInfo.message)} |\n`;
  entry += `| **Tier** | ${escapeTableCell(tier)} — ${escapeTableCell(typeLabel)} |\n`;
  entry += `| **Excluded** | ${escapeTableCell(formatExcluded(tier))} |\n`;
  entry += `| **Included (secrets)** | ${escapeTableCell(".env.local")} |\n`;
  if (verification) {
    const v = verification.success
      ? `Verified (${verification.checkedItemsCount}/${verification.checkedItemsCount} items intact)`
      : `Failed (${verification.errors.length} errors, see terminal)`;
    entry += `| **Verification** | ${escapeTableCell(v)} |\n`;
  }
  entry += `\n---\n\n`;
  return entry;
}

function readExistingNotesBody(backupPath) {
  const notesPath = path.join(backupPath, NOTES_REL_PATH);
  if (!fs.existsSync(notesPath)) return "";
  let content = fs.readFileSync(notesPath, "utf8");
  const footerIdx = content.indexOf("\n*Backup created —");
  if (footerIdx !== -1) content = content.slice(0, footerIdx);
  const trimmed = content.trimEnd();
  return trimmed ? `${trimmed}\n\n` : "";
}

function prependBackupNote(backupPath, entry, preservedTail = "") {
  const notesPath = path.join(backupPath, NOTES_REL_PATH);
  fs.mkdirSync(path.dirname(notesPath), { recursive: true });
  let tail = preservedTail || (fs.existsSync(notesPath) ? fs.readFileSync(notesPath, "utf8") : "");
  if (!tail.includes("*Backup created —")) tail += NOTES_FOOTER;
  fs.writeFileSync(notesPath, entry + tail, "utf8");
  return notesPath;
}

function quoteXdArg(dir) {
  // Robocopy: quote paths that contain spaces
  return dir.includes(" ") ? `"${dir}"` : dir;
}

function buildRobocopyCmd(dest, tier) {
  const xd = getExcludeDirs(tier);
  let cmd = `robocopy "${REPO_ROOT}" "${dest}" /MIR /NFL /NDL /NJH /NP /R:1 /W:1`;
  if (xd.length > 0) {
    cmd += ` /XD ${xd.map(quoteXdArg).join(" ")}`;
  }
  return cmd;
}

const askQuestion = (rl, q) => new Promise((resolve) => rl.question(q, resolve));

async function resolveBackupPlan(rl) {
  const interactive = process.stdin.isTTY;
  let backupFolder = customName || "";
  let tier = resolveTierFromArgs();

  console.log(`
+--------------------------------------------------------------+
|  Backup System — The-Night-I-Met-Santa (book tiers)          |
+--------------------------------------------------------------+

Source: ${REPO_ROOT}
`);

  const existingSeq = listSequentialBackupFolders(DEFAULT_BACKUP_ROOT);
  if (existingSeq.length > 0) console.log(`Existing backups (${existingSeq.length}): ${existingSeq.join(", ")}`);

  if (!tier) {
    if (interactive) {
      console.log(`
Tiers:
  1) QUICK / LIGHT  — ${TIER_META.QUICK.summary}
  2) FULL           — ${TIER_META.FULL.summary}
  3) ARCHIVE        — ${TIER_META.ARCHIVE.summary}
`);
      const pick = (await askQuestion(rl, "Choose tier [1=quick, 2=full, 3=archive] (default 1): ")).trim();
      if (pick === "2" || /^f/i.test(pick)) tier = "FULL";
      else if (pick === "3" || /^a/i.test(pick)) tier = "ARCHIVE";
      else tier = "QUICK";
    } else {
      console.log("\nNon-interactive: pass --quick | --full | --archive (and --yes). Defaulting is not applied.");
      return null;
    }
  }

  const suggestedFolder = customName || suggestNextBackupFolder(DEFAULT_BACKUP_ROOT);
  if (interactive && !backupFolder) {
    const folderAnswer = await askQuestion(rl, `Backup folder name [${suggestedFolder}]: `);
    backupFolder = folderAnswer.trim() || suggestedFolder;
  } else {
    backupFolder = backupFolder || suggestedFolder;
  }

  const fullBackupPath = path.join(DEFAULT_BACKUP_ROOT, backupFolder);

  console.log(`
----------------------------------------------------------------
 Source:      ${REPO_ROOT}
 Destination: ${fullBackupPath}
 Tier:        ${tier} — ${TIER_META[tier].label}
 Skips:       ${formatExcluded(tier)}
 Note:        ${TIER_META[tier].summary}
----------------------------------------------------------------
`);

  if (interactive && !skipConfirm) {
    const confirm = await askQuestion(rl, "Proceed with backup? (y/n): ");
    if (confirm.trim().toLowerCase() !== "y") {
      console.log("\nBackup cancelled.");
      return null;
    }
  } else if (!interactive && !skipConfirm) {
    console.log("\nNon-interactive session: add --yes to run, or run from a terminal for prompts.");
    return null;
  }

  let userNotes = userNoteFromCli;
  if (interactive && !userNotes) {
    userNotes = (await askQuestion(rl, "\nAdd a short note about this backup (optional, Enter to skip): ")).trim();
  }

  return { fullBackupPath, backupFolder, tier, userNotes };
}

function printSuccess(fullBackupPath, tier, backupFolder, notesPath, verification) {
  console.log(`
----------------------------------------------------------------
Backup complete!
Location: ${fullBackupPath}
Tier:     ${tier} — ${TIER_META[tier].label}
Notes:    ${notesPath}
`);
  if (verification) {
    if (verification.success) {
      console.log(`[VERIFY] SUCCESS: all ${verification.checkedItemsCount} critical elements present.`);
    } else {
      console.log(`[VERIFY] FAILURE: ${verification.errors.length} missing/corrupted!`);
      for (const err of verification.errors) console.log(`   - ${err}`);
    }
    for (const warn of verification.warnings) console.log(`   Warning: ${warn}`);
  }
  console.log(`Folder: ${backupFolder}`);
}

async function main() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    const plan = await resolveBackupPlan(rl);
    if (!plan) return;
    const { fullBackupPath, backupFolder, tier, userNotes } = plan;

    if (isDryRun) {
      console.log("\n[dry-run] Backup plan (no files copied):");
      console.log(`  Destination: ${fullBackupPath}`);
      console.log(`  Tier:        ${tier}`);
      console.log(`  /XD list:`);
      for (const d of getExcludeDirs(tier)) console.log(`    - ${d}`);
      console.log(`\n  Robocopy:\n  ${buildRobocopyCmd(fullBackupPath, tier)}`);
      return;
    }

    const driveRoot = path.parse(fullBackupPath).root;
    if (!fs.existsSync(driveRoot)) {
      console.error(`Backup drive ${driveRoot} not found.`);
      process.exit(1);
    }

    fs.mkdirSync(fullBackupPath, { recursive: true });

    const cmd = buildRobocopyCmd(fullBackupPath, tier);
    console.log(`${TIER_META[tier].label} skips:\n  ${formatExcluded(tier)}\n`);
    console.log("Creating backup...\n");

    const now = new Date();
    const p2 = (n) => String(n).padStart(2, "0");
    const timestamp = `${now.getFullYear()}-${p2(now.getMonth() + 1)}-${p2(now.getDate())} ${p2(now.getHours())}:${p2(now.getMinutes())}:${p2(now.getSeconds())}`;
    const gitInfo = getGitInfo(REPO_ROOT);
    const projectVersion = getProjectVersion();

    let robocopyOk = false;
    try {
      // cmd.exe avoids PowerShell `\t` path escapes corrupting robocopy /XD
      execSync(cmd, { stdio: "inherit", shell: "cmd.exe" });
      robocopyOk = true;
    } catch (error) {
      if ([0, 1, 2, 3, 4, 5, 6, 7].includes(error.status)) robocopyOk = true;
      else {
        console.error(`\nBackup failed: ${error.message}`);
        process.exit(1);
      }
    }

    if (robocopyOk) {
      const verification = verifyBackupContents(fullBackupPath, tier);
      const noteEntry = buildNoteEntry({
        timestamp,
        tier,
        userNotes,
        gitInfo,
        backupFolder,
        projectVersion,
        verification,
      });
      const preserved = readExistingNotesBody(fullBackupPath);
      const notesPath = prependBackupNote(fullBackupPath, noteEntry, preserved);
      printSuccess(fullBackupPath, tier, backupFolder, notesPath, verification);
    }
  } finally {
    rl.close();
  }
}

main();
