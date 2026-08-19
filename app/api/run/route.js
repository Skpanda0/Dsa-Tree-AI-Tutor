import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { mkdtemp, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import crypto from "node:crypto";

const execFileAsync = promisify(execFile);
const TIMEOUT_MS = 5000;
const MAX_CODE_LENGTH = 50_000;

const commands = {
  javascript: {
    executable: process.execPath,
    args: (file) => [file]
  },
  python: {
    executable: process.platform === "win32" ? "python" : "python3",
    args: (file) => [file]
  },
  java: null
};

function javaClassName() {
  return `Main_${crypto.randomBytes(6).toString("hex")}`;
}

export async function POST(request) {
  let workDir;

  try {
    const body = await request.json();
    const language = body.language;
    const code = typeof body.code === "string" ? body.code : "";

    if (!["javascript", "python", "java"].includes(language)) {
      return Response.json(
        { ok: false, stderr: "Unsupported language." },
        { status: 400 }
      );
    }

    if (!code.trim()) {
      return Response.json(
        { ok: false, stderr: "Code cannot be empty." },
        { status: 400 }
      );
    }

    if (code.length > MAX_CODE_LENGTH) {
      return Response.json(
        { ok: false, stderr: `Code is too large. Maximum is ${MAX_CODE_LENGTH} characters.` },
        { status: 400 }
      );
    }

    workDir = await mkdtemp(path.join(tmpdir(), "nextjs-code-runner-"));

    let executable;
    let args;
    let sourceFile;

    if (language === "javascript") {
      sourceFile = path.join(workDir, "main.js");
      await writeFile(sourceFile, code, "utf8");
      executable = commands.javascript.executable;
      args = commands.javascript.args(sourceFile);
    } else if (language === "python") {
      sourceFile = path.join(workDir, "main.py");
      await writeFile(sourceFile, code, "utf8");
      executable = commands.python.executable;
      args = commands.python.args(sourceFile);
    } else {
      const className = javaClassName();
      sourceFile = path.join(workDir, `${className}.java`);

      // Java requires the public class name to match the filename.
      const transformedCode = code
        .replace(/\bpublic\s+class\s+Main\b/, `public class ${className}`)
        .replace(/\bclass\s+Main\b/, `class ${className}`);

      await writeFile(sourceFile, transformedCode, "utf8");

      try {
        const compile = await execFileAsync(
          "javac",
          [sourceFile],
          {
            cwd: workDir,
            timeout: TIMEOUT_MS,
            maxBuffer: 1024 * 1024,
            windowsHide: true
          }
        );

        if (compile.stderr) {
          return Response.json({
            ok: false,
            stdout: compile.stdout || "",
            stderr: compile.stderr,
            exitCode: 1
          });
        }
      } catch (error) {
        return Response.json({
          ok: false,
          stdout: error?.stdout || "",
          stderr: error?.stderr || error?.message || "Java compilation failed.",
          exitCode: 1
        });
      }

      executable = "java";
      args = ["-cp", workDir, className];
    }

    const { stdout, stderr } = await execFileAsync(
      executable,
      args,
      {
        cwd: workDir,
        timeout: TIMEOUT_MS,
        maxBuffer: 1024 * 1024,
        windowsHide: true
      }
    );

    return Response.json({
      ok: true,
      stdout: stdout || "",
      stderr: stderr || "",
      exitCode: 0
    });
  } catch (error) {
    const timedOut = error?.code === "ETIMEDOUT" || error?.signal === "SIGTERM";

    return Response.json({
      ok: false,
      stdout: error?.stdout || "",
      stderr: timedOut
        ? "Execution timed out after 5 seconds."
        : (error?.stderr || error?.message || "Code execution failed."),
      exitCode: typeof error?.code === "number" ? error.code : 1,
      timedOut
    });
  } finally {
    if (workDir) {
      await rm(workDir, { recursive: true, force: true }).catch(() => {});
    }
  }
}