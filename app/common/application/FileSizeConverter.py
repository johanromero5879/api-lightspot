class FileSizeConverter:
    KILOBYTES = float(1024)
    MEGABYTES = float(KILOBYTES ** 2)

    @classmethod
    def bytes_to_megabytes(cls, b: float) -> float:
        return b / cls.MEGABYTES
