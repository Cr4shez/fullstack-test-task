import { API_ENDPOINTS } from "@/shared/config";
import { useState } from "react";
import { Modal, Form, Button } from "react-bootstrap";

interface Props {
  show: boolean;
  onClose: () => void;
  onSuccess: () => void;
  onError: (message: string) => void;
}

export const UploadModal = ({ show, onClose, onSuccess, onError }: Props) => {
  const [title, setTitle] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !selectedFile) {
      onError("Укажите название и выберите файл");
      return
    }

    setIsSubmitting(true);
    const formData = new FormData();
    formData.append("title", title.trim());
    formData.append("file", selectedFile);

    try {
      const response = await fetch(API_ENDPOINTS.FILES.upload_file, {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        onError("Не удалось загрузить файл");
        return
      }
      onSuccess();
    } catch (error) {
      onError(error instanceof Error ? error.message : "Произошла ошибка");
      return
    } finally {
      setIsSubmitting(false)
    }
    onClose();
    cleanUp();
  };

  let cleanUp = () => {
    setIsSubmitting(false)
    setSelectedFile(null)
    setTitle("")
  }

  return (
    <Modal show={show} onHide={onClose}>
      <Form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Добавить файл</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Название</Form.Label>
            <Form.Control
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="Например, Договор с подрядчиком"
            />
          </Form.Group>
          <Form.Group>
            <Form.Label>Файл</Form.Label>
            <Form.Control
              type="file"
              onChange={(event) =>
                setSelectedFile((event.target as HTMLInputElement).files?.[0] ?? null)
              }
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="outline-secondary" onClick={() => onClose()}>
            Отмена
          </Button>
          <Button type="submit" variant="primary" disabled={isSubmitting}>
            {isSubmitting ? "Загрузка..." : "Сохранить"}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};
