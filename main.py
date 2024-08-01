import os
import time
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


def checkAllPdfConversion():
    pdf_path = os.path.normpath("./pdf")
    files = [f for f in os.listdir(
        pdf_path) if os.path.isfile(os.path.join(pdf_path, f))]
    for filepath in files:
        [filename, ext] = os.path.splitext(filepath)
        src_path = os.path.join("./pdf", f"{filename}.pdf")
        dist_path = os.path.join("./docx", f"{filename}.docx")
        if not ext == ".pdf":
            continue
        if not os.path.exists(dist_path):
            convertPdf2Docx(src_path=src_path, dist_path=dist_path)


class CustomFileHandler(watchdog.events.FileSystemEventHandler):
    def dispatch(self, event) -> None:
        if event.event_type != "created" and event.event_type != "modified":
            return super().dispatch(event)
        
        [filename, extension] = os.path.splitext(os.path.basename(event.src_path))
        dist_path =os.path.join('./docx/', f'{filename}.docx')
        
        if extension != ".pdf":
            return super().dispatch(event)

        # Wait os module can read new file
        timeout_second = 5
        start_time = time.time()
        while time.time() - start_time < timeout_second:
            if os.path.exists(event.src_path):
                break

        if not os.path.exists(event.src_path):
            raise TimeoutError(f'{event.src_path} terlalu lama diproses')

        convertPdf2Docx(src_path=event.src_path, dist_path=dist_path)
        return super().dispatch(event)


def main():
    observer = watchdog.observers.Observer()
    handler = CustomFileHandler()

    checkRequiredDir()

    observer.schedule(event_handler=handler, path=os.path.normpath("./pdf"))
    observer.start()
    print("""Dinasty Odoo pdf2docx converter
----------------------------
Cara pakai: Letakan faktur pdf yang ingin dikonversi di folder \"pdf\", program akan mekonversi
secara otomatis dan meletakan hasilnya di folder \"docx\" dengan nama file yang sama

Menutup program: Tekan \"Ctrl\"+\"c\" untuk menyelesaikan program

Siap memulai konversi!""")
    try:
        checkAllPdfConversion()
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
