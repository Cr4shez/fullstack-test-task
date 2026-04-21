"use client";

import { useState } from "react";
import {
  Alert,
  Badge,
  Button,
  Card,
  Col,
  Container,
  Row,
} from "react-bootstrap";

import { FileTable, useFiles } from "@/entities/files";
import { AlertTable, useAlerts } from "@/entities/alerts";
import { DEFAULT_PAGE_SIZE } from "@/shared/config";
import { UploadModal } from "@/features/upload_file/UploadModal";
import { Pagination } from "@/shared/ui/Pagination";

export const DashboardPage = () => {
  const [filePageSize] = useState(DEFAULT_PAGE_SIZE);
  const [alertPageSize] = useState(DEFAULT_PAGE_SIZE);

  const [uploadError, setUploadError] = useState<string | null>(null);
  const { 
    data: files, 
    loading: isFilesLoading, 
    error: fileError,
    refresh: fetchFiles,
    page: filesPage,
    total: filesTotal,
    totalPages: filesTotalPages,
    setPage: filesSetPage,
  } = useFiles(filePageSize);

  const { 
    data: alerts, 
    loading: isAlertsLoading,
    error: alertError,
    refresh: fetchAlerts,
    page: alertsPage,
    total: alertsTotal,
    totalPages: alertsTotalPages,
    setPage: alertsSetPage,
  } = useAlerts(alertPageSize);

  const [showModal, setShowModal] = useState(false);

  const loadData = () => {
    fetchFiles();
    fetchAlerts();
  };

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>

          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                  <h1 className="h3 mb-2">Управление файлами</h1>
                  <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                  </p>
                </div>
                <div className="d-flex gap-2">
                  <Button variant="outline-secondary" onClick={loadData}>
                    Обновить
                  </Button>
                  <Button variant="primary" onClick={() => setShowModal(true)}>
                    Добавить файл
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>
        
        <div className="d-flex flex-column gap-2 mb-4">
        {[fileError, alertError, uploadError].filter(Boolean).map((err, i) => (
            <Alert key={i} variant="danger" className="m-0 shadow-sm">
            {err}
            </Alert>
        ))}
        </div>


          <Card className="shadow-sm border-0 mb-4">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Файлы</h2>
                <Badge bg="secondary">{filesTotal}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <div className="table-responsive">
                <FileTable files={files} isLoading={isFilesLoading} />
              </div>
              <Pagination 
                currentPage={filesPage} 
                totalPages={filesTotalPages} 
                onChange={filesSetPage} 
                disabled={isFilesLoading}
              />
            </Card.Body>
            
          </Card>

          <Card className="shadow-sm border-0">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Алерты</h2>
                <Badge bg="secondary">{alertsTotal}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <div className="table-responsive">
                <AlertTable alerts={alerts} isLoading={isAlertsLoading} />
              </div>

              <Pagination 
                currentPage={alertsPage} 
                totalPages={alertsTotalPages} 
                onChange={alertsSetPage} 
                disabled={isAlertsLoading}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <UploadModal 
        show={showModal}
        onClose={() => setShowModal(false)}
        onSuccess={() => loadData()}
        onError={(message) => setUploadError(message)}
      >
      </UploadModal>
    </Container>
  );
};
