import os
import pdf2docx
import watchdog.observers
import watchdog.events


def checkRequiredDir():
    if not os.path.exists("./docx"):
        os.mkdir("./docx")
    if not os.path.exists("./pdf"):
        os.mkdir("./pdf")


def convertPdf2Docx(src_path: str, dist_path: str):
    pdf2docx.parse(pdf_file=src_path, docx_file=dist_path)


class CustomFileHandler(watchdog.events.FileSystemEventHandler):
    def dispatch(self, event) -> None:
        if event.event_type == "created" or event.event_type == "modified":
            filename = os.path.splitext(os.path.basename(event.src_path))[0]
            dist_path = os.path.join('./docx/', f'{filename}.docx')
            convertPdf2Docx(src_path=event.src_path, dist_path=dist_path)
        return super().dispatch(event)


def main():
    observer = watchdog.observers.Observer()
    handler = CustomFileHandler()

    checkRequiredDir()

    observer.schedule(event_handler=handler, path=os.path.normpath("./pdf"))
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
