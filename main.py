import pdf2docx
import watchdog.observers
import watchdog.events

pdf_path = './pdf/Faktur Dinasty - INV_2024_00440.pdf'
docx_path = './docx/testing.docx'


class CustomFileHandler(watchdog.events.FileSystemEventHandler):
    def dispatch(self, event: watchdog.events.FileSystemEvent) -> None:
        print(event)
        return super().dispatch(event)


def main():
    observer = watchdog.observers.Observer()
    handler = CustomFileHandler()

    # pdf2docx.parse(pdf_file=pdf_path, docx_file=docx_path)
    observer.schedule(event_handler=handler, path="./pdf")
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
