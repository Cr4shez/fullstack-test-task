import { BaseTable } from "@/shared/ui/BaseTable";
import { AlertItem } from "../types"; // Assuming your interface name
import { formatDate, getLevelVariant } from "@/shared/lib";
import { Badge } from "react-bootstrap";

interface Props {
  alerts: AlertItem[];
  isLoading: boolean;
}

export const AlertTable = ({ alerts, isLoading }: Props) => {
  const headers = ["ID", "File ID", "Уровень", "Сообщение", "Создан"];

  return (
    <BaseTable
      headers={headers}
      data={alerts}
      isLoading={isLoading}
      emptyText="Алертов пока нет"
      renderRow={(item: AlertItem) => (
        <tr key={item.id}>
          <td>{item.id}</td>
          <td className="small">{item.file_id}</td>
          <td>
            <Badge bg={getLevelVariant(item.level)}>
              {item.level}
            </Badge>
          </td>
          <td>{item.message}</td>
          <td>{formatDate(item.created_at)}</td>
        </tr>
      )}
    />
  );
};
