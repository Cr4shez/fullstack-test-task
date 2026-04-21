import { components } from "@/shared/api/schema";
import { PaginatedResponse } from "@/shared/api/types";

export type AlertItem = components["schemas"]["AlertResponse"]
export type PaginatedAlertItem = PaginatedResponse<AlertItem>
