import locale

from app.common.application import PDFBuilder, get_datetime_now
from app.flash.domain import FlashQuery, FlashOut, FLASH_DATE_FORMAT


async def generate_flash_report(
    flashes: list[FlashOut],
    query: FlashQuery,
    utc_offset: str = "+00:00",
    pdf_builder: PDFBuilder = PDFBuilder()
):
    total_flashes = len(flashes)

    created_at = get_datetime_now(utc_offset)
    created_at = created_at.strftime("%Y/%m/%d %I:%M%p %Z")

    header = f"Creado en {created_at}"
    title = "Reporte de ocurrencias de flashes"
    content = set_content(query, utc_offset, total_flashes)
    table_data = set_table_data(flashes)
    footer = "Datos entregados por la <a href='http://wwlln.net/'>WWLLN</a>"

    pdf_data = pdf_builder \
        .set_header(header) \
        .set_title(title) \
        .add_content_by_columns(content, 230)\
        .add_table(table_data)\
        .set_footer(footer)\
        .build()

    return pdf_data


def set_content(query: FlashQuery, utc_offset: str, total_flashes: int):
    start_date = query.date_range.start_date.strftime("%Y/%m/%d")
    end_date = query.date_range.end_date.strftime("%Y/%m/%d")

    state = None
    city = None
    total = f"<strong>Total flashes: </strong>{total_flashes}"

    if query.location.state:
        state = f"<strong>Departamento: </strong>{query.location.state}"

    if query.location.city:
        city = f"<strong>Ciudad: </strong>{query.location.city}"

    content = [
        [f"<strong>Zona horaria: </strong>UTC{utc_offset}", f"<strong>País: </strong>{query.location.country}"],
        [f"<strong>Fecha inicio: </strong>{start_date}", state if state else None],
        [f"<strong>Fecha fin: </strong>{end_date}", city if city else None]
    ]

    if not state and city:
        content[1][1] = city
        content[2][1] = total
    elif not city:
        content[2][1] = total
    else:
        content.append([total])

    return content


def set_table_data(flashes: list[FlashOut]):
    data = [["No.", "Fecha", "Latitud", "Longitud", "Resid", "Estaciones"]]

    for index, flash in enumerate(flashes):
        data.append([
            index + 1,
            flash.occurrence_date.strftime(FLASH_DATE_FORMAT),
            flash.lat,
            flash.lon,
            flash.residual_fit_error,
            flash.stations
        ])

    return data
