import { execFileSync } from "node:child_process";
import { readFileSync, unlinkSync } from "node:fs";

const target = "src/api/generated.ts";
const temp = "src/api/generated.ts.check";

function run() {
  execFileSync("npx", ["openapi-typescript", "../openapi.json", "--output", temp], {
    stdio: "inherit",
    shell: process.platform === "win32",
  });
}

let failed = true;
try {
  run();
  const committed = readFileSync(target, "utf8");
  const regenerated = readFileSync(temp, "utf8");
  if (committed !== regenerated) {
    console.error("frontend/src/api/generated.ts is stale.");
    console.error("Run `just gen-types` (or npm run types:generate) and commit the regenerated file.");
  } else {
    failed = false;
  }
} finally {
  try {
    unlinkSync(temp);
  } catch {
    // nothing to clean up
  }
}
process.exit(failed ? 1 : 0);
