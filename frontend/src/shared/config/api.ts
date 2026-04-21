export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const API_V1 = `${API_URL}/api/v1`;

export const API_ENDPOINTS = {
    FILES: {
        list: `${API_V1}/files/`,
        upload_file: `${API_V1}/files/`,
        
        get: (id: string | number) => `${API_V1}/files/${id}/`,
        download: (id: string | number) => `${API_V1}/files/${id}/download/`,
    },
    ALERTS: {
        list: `${API_V1}/alerts/`
    }
} as const;
