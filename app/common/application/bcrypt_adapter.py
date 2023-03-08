from bcrypt import hashpw, gensalt, checkpw


class BcryptAdapter:
    __rounds: int = 14

    def hash(self, text: str) -> str:
        hashed_text = hashpw(
            text.encode("utf-8"),
            gensalt(self.__rounds)
        )

        return hashed_text.decode()

    def compare(self, text: str, hashed: str) -> bool:
        return checkpw(
            text.encode("utf-8"),
            hashed.encode("utf-8")
        )
