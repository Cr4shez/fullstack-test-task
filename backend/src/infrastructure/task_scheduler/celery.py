from celery import chain

class CeleryTaskScheduler:
    def schedule_file_analysis(self, file_id: str):
        from src.tasks.file_tasks import scan_file_for_threats, extract_file_metadata, send_file_alert

        workflow = chain(
            scan_file_for_threats.s(file_id),
            extract_file_metadata.s(),
            send_file_alert.s()
        )
        workflow.apply_async()
