export function readEnv(
  env: Record<string, string | undefined>,
  name: string,
  defaultVal?: string
): string {
  if (name in env) {
    return env[name]!
  }
  if (defaultVal) {
    return defaultVal
  }
  throw new Error(
    `Error reading environment variable "${name}". Variable not set on environment and no default value provided`
  )
}
