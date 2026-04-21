import { useState, useEffect, useCallback, useMemo } from "react";
import { AlertItem } from "./types";
import { API_ENDPOINTS } from "@/shared/config";

export const useAlerts = (_limit: number) => {
  const [data, setData] = useState<AlertItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(_limit);
  const [total, setTotal] = useState(0)

  const fetchAlerts = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ 
        page: page.toString(), 
        limit: limit.toString() 
      });
      const response = await fetch(`${API_ENDPOINTS.ALERTS.list}?${params}`);
      if (!response.ok) throw new Error("Failed to fetch alerts");
      
      const result = await response.json();
      setData(result.items);
      setTotal(result.total)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, [page, limit]);

  useEffect(() => {
    fetchAlerts();
  }, [fetchAlerts]);

  const totalPages = useMemo(() => {
    if (!total || !limit) return 1;
    return Math.ceil(total / limit);
  }, [total, limit]);


  return { data, loading, error, page, setPage, setLimit, total, totalPages, refresh: fetchAlerts };
};

