from pydantic import BaseModel


class Meme(BaseModel):
    id: int = None
    original_image_path: str = ''
    generated_image_path: str = ''
    top_text: str
    bottom_text: str

    @classmethod
    def get_from_db_data(cls, data: list):
        return cls(id=data[0],
                   original_image_path=data[1],
                   generated_image_path=data[2],
                   top_text=data[3],
                   bottom_text=data[4])

    def get_data_to_save(self):
        return [self.id, self.original_image_path, self.generated_image_path,
                self.top_text, self.bottom_text]


class GetMeme(BaseModel):
    id: int
    original_image_url: str
    generated_image_url: str
    top_text: str
    bottom_text: str
