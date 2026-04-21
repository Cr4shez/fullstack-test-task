import { Pagination as BSPagination } from "react-bootstrap";

interface Props {
  currentPage: number;
  totalPages: number;
  onChange: (page: number) => void;
  disabled?: boolean;
}

export const Pagination = ({ currentPage, totalPages, onChange, disabled }: Props) => {
  if (totalPages <= 1) return null;

  const items = [];
  for (let number = 1; number <= totalPages; number++) {
    items.push(
      <BSPagination.Item
        key={number}
        active={number === currentPage}
        onClick={() => onChange(number)}
        disabled={disabled}
      >
        {number}
      </BSPagination.Item>
    );
  }

  return (
    <div className="d-flex justify-content-center mt-3">
      <BSPagination>
        <BSPagination.Prev 
          disabled={currentPage === 1 || disabled} 
          onClick={() => onChange(currentPage - 1)} 
        />
        
        {items}

        <BSPagination.Next 
          disabled={currentPage === totalPages || disabled} 
          onClick={() => onChange(currentPage + 1)} 
        />
      </BSPagination>
    </div>
  );
};
