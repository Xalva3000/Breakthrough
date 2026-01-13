from api.api_v1.books.schemas import BookBase, PageBase
import json
from pathlib import Path
from pydantic import BaseModel
import logging


logger = logging.getLogger(__name__)


class BookStorage(BaseModel):
    books: dict[str, BookBase] = {}
    file_path: Path = Path("books_data.json")

    def __init__(self, file_path: str = "books_data.json", **data):
        super().__init__(**data)
        self.file_path = Path(file_path)
        self.load_from_file()

    def create(self, new_book: BookBase):
        self.books[new_book.title] = new_book
        result = self.save_to_file()
        if result:
            return new_book
        return False

    def insert_page(self, title, page: PageBase):
        book = self.books.get(title)
        if book:
            book.pages[page.index] = page
            self.save_to_file()
        return self.books.get(title)

    def get_book(self, title):
        return self.books.get(title)

    def get_page(self, book_title, index):
        book = self.books.get(book_title)
        if book:
            return book.pages.get(index)
        return None

    def delete_book(self, title):
        del self.books[title]
        self.save_to_file()
        return True

    def delete_page(self, title, index):
        try:
            del self.books[title].pages[index]
            self.save_to_file()
        except Exception:
            return False
        else:
            return True

    def save_to_file(self) -> bool:
        """Сохранить данные в JSON файл"""
        try:
            data = {
                "books": {
                    title: book.model_dump(mode="json")
                    for title, book in self.books.items()
                }
            }
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            temp_file = self.file_path.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            temp_file.replace(self.file_path)
            logger.info(f"Данные сохранены в {self.file_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения: {e}")
            return False

    def load_from_file(self) -> bool:
        """Загрузить данные из JSON файла"""
        try:
            if not self.file_path.exists():
                logger.info(f"Файл {self.file_path} не существует, создаем новый")
                self.books = {}
                return True
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = {}
            for title, book_data in data.get("books", {}).items():
                pages_data = book_data.get("pages", {})
                if pages_data:
                    processed_pages = {}
                    for page_num_str, page_data in pages_data.items():
                        try:
                            page_num = int(page_num_str)
                            processed_pages[page_num] = PageBase(**page_data)
                        except (ValueError, TypeError) as e:
                            logger.warning(
                                f"Ошибка обработки страницы {page_num_str}: {e}"
                            )
                    book_data["pages"] = processed_pages
                try:
                    self.books[title] = BookBase(**book_data)
                except Exception as e:
                    logger.error(f"Ошибка создания книги '{title}': {e}")
            logger.info(f"Загружено {len(self.books)} книг из {self.file_path}")
            return True
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            self.books = {}
            return False
        except Exception as e:
            logger.error(f"Ошибка загрузки: {e}")
            self.books = {}
            return False


book_storage = BookStorage()
