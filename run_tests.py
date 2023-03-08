from dotenv import load_dotenv
import pytest

load_dotenv(dotenv_path=".env.test")

pytest.main(args=["-x", "tests"])
