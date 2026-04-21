import {components} from "@/shared/api/schema"
import { PaginatedResponse } from "@/shared/api/types"

export type FileItem = components["schemas"]["FileResponse"]
export type PaginatedFileItem = PaginatedResponse<FileItem>
export type FileProcessingStatus = components["schemas"]["FileProcessingStatus"]
export type FileScanStatus = components["schemas"]["FileScanStatus"]
