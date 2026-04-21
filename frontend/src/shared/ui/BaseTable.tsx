import { Table } from "react-bootstrap";

interface BaseTableProps<T> {
  headers: string[];
  data: T[];
  renderRow: (item: T, index: number) => React.ReactNode;
  isLoading?: boolean;
  emptyText?: string
}

export const BaseTable = <T,>({ headers, data, renderRow, isLoading, emptyText }: BaseTableProps<T>) => {
  return (
    <Table hover responsive striped className="align-middle">
      <thead>
        <tr>
          {headers.map((header) => (
            <th key={header}>{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {isLoading ? (
          <tr>
            <td colSpan={headers.length} className="text-center py-4">Загрузка...</td>
          </tr>
        ) : data.length === 0 ? (
          <tr>
            <td colSpan={headers.length} className="text-center py-4 text-muted">{emptyText}</td>
          </tr>
        ) : (
          data.map((item, index) => renderRow(item, index))
        )}
      </tbody>
    </Table>
  );
};
