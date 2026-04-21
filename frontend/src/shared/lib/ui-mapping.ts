export const STATUS_VARIANTS: Record<string, string> = {
  failed: "danger",
  processing: "warning",
  processed: "success",
};

export const getStatusVariant = (status: string) => STATUS_VARIANTS[status] || "secondary";

export const LEVEL_VARIANTS: Record<string, string> = {
    critical: "danger",
    warning: "warning",
    info: "success"
}

export const getLevelVariant = (level: string) => LEVEL_VARIANTS[level] || "success"
