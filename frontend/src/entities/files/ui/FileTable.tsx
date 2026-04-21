// src/entities/file/ui/FilesTable.tsx
import { BaseTable } from "@/shared/ui/BaseTable";
import { FileItem } from "../types";
import { formatDate, formatSize, getStatusVariant } from "@/shared/lib/";
import { Badge, Button } from "react-bootstrap";
import { API_ENDPOINTS } from "@/shared/config";

interface Props {
  files: FileItem[];
  isLoading: boolean;
}

export const FileTable = ({ files, isLoading }: Props) => {
  const headers = ["Название", "Файл", "MIME", "Размер", "Статус", "Проверка", "Создан", "Скачать"];

  return (
    <BaseTable
      headers={headers}
      data={files}
      isLoading={isLoading}
      emptyText="Файлы пока не загружены"
      renderRow={(file: FileItem) => (
        <tr key={file.id}>
          <td>
            <div className="fw-semibold">{file.title}</div>
            <div className="small text-secondary">{file.id}</div>
          </td>
          <td>{file.original_name}</td>
          <td>{file.mime_type}</td>
          <td>{formatSize(file.size)}</td>
          <td>
            <Badge bg={getStatusVariant(file.processing_status)}>
              {file.processing_status}
            </Badge>
          </td>
          <td>
            <div className="d-flex flex-column gap-1">
              <Badge bg={file.requires_attention ? "warning" : "success"}>
                {file.scan_status ?? "pending"}
              </Badge>
              <span className="small text-secondary">
                {file.scan_details ?? "Ожидает обработки"}
              </span>
            </div>
          </td>
          <td>{formatDate(file.created_at)}</td>
          <td className="text-end">
            <Button
              as="a"
              href={API_ENDPOINTS.FILES.download(file.id)}
              variant="outline-primary"
              size="sm"
              target="_blank"
              rel="noopener noreferrer"
              download
            >
              Скачать
            </Button>
          </td>
        </tr>
      )}
    />
  );
};
