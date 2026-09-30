import { copyFileSync, existsSync, mkdirSync, readdirSync, unlinkSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const modDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = path.resolve(modDir, "../..");
const clientDestDir = path.join(repoRoot, "pack/client/mods");
const serverDestDir = path.join(repoRoot, "pack/server/mods");
const vendorDir = path.join(repoRoot, "pack/vendor");
const jarPrefix = "cobblelore-legendary-";

function resolveJavaHome() {
  if (process.env.JAVA_HOME && existsSync(path.join(process.env.JAVA_HOME, "bin", "java.exe"))) {
    return process.env.JAVA_HOME;
  }
  const adoptiumRoot = "C:\\Program Files\\Eclipse Adoptium";
  if (existsSync(adoptiumRoot)) {
    for (const name of readdirSync(adoptiumRoot)) {
      if (name.startsWith("jdk-21")) {
        const candidate = path.join(adoptiumRoot, name);
        if (existsSync(path.join(candidate, "bin", "java.exe"))) {
          return candidate;
        }
      }
    }
  }
  return null;
}

function runGradle(cwd) {
  const javaHome = resolveJavaHome();
  if (!javaHome) {
    console.error("JDK 21 not found.");
    process.exit(1);
  }
  const gradlew = process.platform === "win32" ? "gradlew.bat" : "./gradlew";
  const build = spawnSync(gradlew, ["clean", "build", "--no-daemon"], {
    cwd,
    stdio: "inherit",
    shell: true,
    env: { ...process.env, JAVA_HOME: javaHome },
  });
  if (build.status !== 0) {
    process.exit(build.status ?? 1);
  }
}

function removeOldJars(destDir, prefix) {
  if (!existsSync(destDir)) {
    return;
  }
  for (const name of readdirSync(destDir)) {
    if (name.startsWith(prefix) && name.endsWith(".jar")) {
      unlinkSync(path.join(destDir, name));
    }
  }
}

function ensureLegendaryMonumentsCompileJar() {
  const clientMods = path.join(repoRoot, "pack/client/mods");
  const lmJar = existsSync(clientMods)
    ? readdirSync(clientMods).find((name) => name.startsWith("legendarymonuments") && name.endsWith(".jar"))
    : undefined;
  if (!lmJar) {
    console.error("Legendary Monuments jar missing in pack/client/mods. Run npm run build:pack first.");
    process.exit(1);
  }
  mkdirSync(path.join(modDir, "libs"), { recursive: true });
  copyFileSync(path.join(clientMods, lmJar), path.join(modDir, "libs/legendary-monuments.jar"));
}

console.log("Building cobblelore-legendary...");
ensureLegendaryMonumentsCompileJar();
runGradle(modDir);

const libsDir = path.join(modDir, "build/libs");
const jar = readdirSync(libsDir).find(
  (name) => name.startsWith(jarPrefix) && name.endsWith(".jar") && !name.includes("-sources"),
);
if (!jar) {
  console.error("No release jar in build/libs");
  process.exit(1);
}

for (const destDir of [clientDestDir, serverDestDir, vendorDir]) {
  mkdirSync(destDir, { recursive: true });
  removeOldJars(destDir, jarPrefix);
  copyFileSync(path.join(libsDir, jar), path.join(destDir, jar));
  console.log(`Copied ${jar} -> ${path.relative(repoRoot, destDir)}/`);
}
