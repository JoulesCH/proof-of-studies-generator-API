
import time
import io
import zipfile


def zip_files(bytes_pdfs, datos, tipo_constancia, semestre_actual) -> bytes:
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for i, individualFile, dato in zip(range(len(bytes_pdfs)), bytes_pdfs, datos):
            data_zip = zipfile.ZipInfo(f'{dato["registro"]}_{tipo_constancia}_{semestre_actual}.pdf')
            data_zip.date_time = time.localtime(time.time())[:6]
            data_zip.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data_zip, individualFile)
    memory_file.seek(0)

    return memory_file