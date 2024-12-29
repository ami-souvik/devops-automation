export function useEnvars() {
    return JSON.parse(JSON.stringify(import.meta.env))
}